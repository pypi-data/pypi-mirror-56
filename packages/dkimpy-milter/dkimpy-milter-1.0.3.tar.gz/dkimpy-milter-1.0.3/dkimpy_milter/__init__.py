#! /usr/bin/python2
# Original dkim-milter.py code:
# Author: Stuart D. Gathman <stuart@bmsi.com>
# Copyright 2007 Business Management Systems, Inc.
# This code is under GPL.  See COPYING for details.

# dkimpy-milter: A DKIM signing/verification Milter application
# Author: Scott Kitterman <scott@kitterman.com>
# Copyright 2018 Scott Kitterman
"""    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA."""

import sys
import syslog
import Milter
import dkim
import authres
import os
import tempfile
import StringIO
import re
from Milter.utils import parse_addr, parseaddr
import dkimpy_milter.config as config
from dkimpy_milter.util import drop_privileges
from dkimpy_milter.util import setExceptHook
from dkimpy_milter.util import write_pid
from dkimpy_milter.util import read_keyfile
from dkimpy_milter.util import fold

__version__ = "1.0.1"
FWS = re.compile(r'\r?\n[ \t]+')


class dkimMilter(Milter.Base):
    "Milter to check and sign DKIM.  Each connection gets its own instance."

    def __init__(self):
        self.mailfrom = None
        self.id = Milter.uniqueID()
        # we don't want config used to change during a connection
        self.conf = milterconfig
        self.privatersa = privateRSA
        self.privateed25519 = privateEd25519
        self.fp = None
        self.fdomain = ''

    @Milter.noreply
    def connect(self, hostname, unused, hostaddr):
        self.internal_connection = False
        self.external_connection = False
        self.hello_name = None
        # sometimes people put extra space in sendmail config, so we strip
        self.receiver = self.getsymval('j').strip()
        try:
            self.AuthservID = milterconfig['AuthservID']
        except:
            self.AuthservID = self.receiver
        if hostaddr and len(hostaddr) > 0:
            ipaddr = hostaddr[0]
            if milterconfig['IntHosts']:
                if milterconfig['IntHosts'].match(ipaddr):
                    self.internal_connection = True
        else:
            ipaddr = ''
        self.connectip = ipaddr
        if milterconfig.get('MacroList') and not self.internal_connection:
            macrolist = milterconfig.get('MacroList')
            for macro in macrolist:
                macroname = macro.split('|')[0]
                macroname = '{' + macroname + '}'
                macroresult = self.getsymval(macroname)
                if ((len(macro.split('|')) == 1 and macroresult) or macroresult
                        in macro.split('|')[1:]):
                    self.internal_connection = True
        if milterconfig.get('MacroListVerify'):
            macrolist = milterconfig.get('MacroListVerify')
            for macro in macrolist:
                macroname = macro.split('|')[0]
                macroname = '{' + macroname + '}'
                macroresult = self.getsymval(macroname)
                if ((len(macro.split('|')) == 1 and macroresult) or macroresult
                        in macro.split('|')[1:]):
                    self.external_connection = True
        if self.internal_connection:
            connecttype = 'INTERNAL'
        else:
            connecttype = 'EXTERNAL'
        if milterconfig.get('Syslog') and milterconfig.get('debugLevel') >= 1:
            syslog.syslog("connect from {0} at {1} {2}"
                          .format(hostname, hostaddr, connecttype))
        return Milter.CONTINUE

    # multiple messages can be received on a single connection
    # envfrom (MAIL FROM in the SMTP protocol) seems to mark the start
    # of each message.
    @Milter.noreply
    def envfrom(self, f, *str):
        if milterconfig.get('Syslog') and milterconfig.get('debugLevel') >= 2:
            syslog.syslog("mail from: {0} {1}".format(f, str))
        self.fp = StringIO.StringIO()
        self.mailfrom = f
        t = parse_addr(f)
        if len(t) == 2:
            t[1] = t[1].lower()
        self.canon_from = '@'.join(t)
        self.has_dkim = 0
        self.author = None
        self.arheaders = []
        self.arresults = []
        return Milter.CONTINUE

    @Milter.noreply
    def header(self, name, val):
        lname = name.lower()
        if lname == 'dkim-signature':
            if (milterconfig.get('Syslog') and
                    milterconfig.get('debugLevel') >= 1):
                syslog.syslog("{0}: {1}".format(name, val))
            self.has_dkim += 1
        if lname == 'from':
            fname, self.author = parseaddr(val)
            try:
                self.fdomain = self.author.split('@')[1].lower()
            except IndexError as er:
                pass # self.author was not a proper email address
            if (milterconfig.get('Syslog') and
                    milterconfig.get('debugLevel') >= 1):
                syslog.syslog("{0}: {1}".format(name, val))
        elif lname == 'authentication-results':
            self.arheaders.append(val)
        if self.fp:
            try:
                self.fp.write("%s: %s\n" % (name, val))
            except:
                # Don't choke on header fields with garbage in them.
                pass
        return Milter.CONTINUE

    @Milter.noreply
    def eoh(self):
        if self.fp:
            self.fp.write("\n")   # terminate headers
        self.bodysize = 0
        return Milter.CONTINUE

    @Milter.noreply
    def body(self, chunk):        # copy body to temp file
        if self.fp:
            self.fp.write(chunk)  # IOError causes TEMPFAIL in milter
            self.bodysize += len(chunk)
        return Milter.CONTINUE

    def eom(self):
        if not self.fp:
            return Milter.ACCEPT  # no message collected - so no eom processing
        # Remove existing Authentication-Results headers for our authserv_id
        for i, val in enumerate(self.arheaders, 1):
            # FIXME: don't delete A-R headers from trusted MTAs
            try:
                ar = (authres.AuthenticationResultsHeader
                      .parse_value(FWS.sub('', val)))
                if ar.authserv_id == self.AuthservID:
                    self.chgheader('authentication-results', i, '')
                    if (milterconfig.get('Syslog') and
                            milterconfig.get('debugLevel') >= 1):
                        syslog.syslog('REMOVE: {0}'.format(val))
            except:
                # Don't error out on unparseable AR header fiels
                pass
        # Check and/or sign DKIM
        self.fp.seek(0)
        txt = self.fp.read()
        if milterconfig.get('Domain'):
            domain = milterconfig.get('Domain')
        else:
            domain = ''
        if ((self.fdomain in domain) and not milterconfig.get('Mode') == 'v'
                and not self.external_connection):
            self.sign_dkim(txt)
        if ((self.has_dkim) and (not self.internal_connection) and
            (milterconfig.get('Mode') == 'v' or
             milterconfig.get('Mode') == 'sv')):
            self.check_dkim(txt)
        if self.arresults:
            h = authres.AuthenticationResultsHeader(authserv_id=
                                                    self.AuthservID,
                                                    results=self.arresults)
            h = fold(str(h))
            if (milterconfig.get('Syslog') and
                    milterconfig.get('debugLevel') >= 2):
                syslog.syslog(str(h))
            name, val = str(h).split(': ', 1)
            self.addheader(name, val, 0)
        return Milter.CONTINUE

    def sign_dkim(self, txt):
        canon = milterconfig.get('Canonicalization')
        canonicalize = []
        if len(canon.split('/')) == 2:
            canonicalize.append(canon.split('/')[0])
            canonicalize.append(canon.split('/')[1])
        else:
            canonicalize.append(canon)
            canonicalize.append(canon)
            if (milterconfig.get('Syslog') and
                    milterconfig.get('debugLevel') >= 1):
                syslog.syslog('canonicalize: {0}'.format(canonicalize))
        try:
            if privateRSA:
                d = dkim.DKIM(txt)
                h = d.sign(milterconfig.get('Selector'), self.fdomain,
                           privateRSA, canonicalize=(canonicalize[0],
                                                     canonicalize[1]))
                name, val = h.split(': ', 1)
                self.addheader(name, val.strip().replace('\r\n', '\n'), 0)
                if (milterconfig.get('Syslog') and
                    (milterconfig.get('SyslogSuccess')
                     or milterconfig.get('debugLevel') >= 1)):
                    syslog.syslog('{0}: {1} DKIM-Signature field added (s={2} '
                                  'd={3})'.format(self.getsymval('i'),
                                                  d.signature_fields.get(b'a'),
                                                  d.signature_fields.get(b's'),
                                                  d.domain.lower()))
            if privateEd25519:
                d = dkim.DKIM(txt)
                h = d.sign(milterconfig.get('SelectorEd25519'), self.fdomain,
                           privateEd25519, canonicalize=(canonicalize[0],
                                                         canonicalize[1]),
                           signature_algorithm='ed25519-sha256')
                name, val = h.split(': ', 1)
                self.addheader(name, val.strip().replace('\r\n', '\n'), 0)
                if (milterconfig.get('Syslog') and
                    (milterconfig.get('SyslogSuccess')
                     or milterconfig.get('debugLevel') >= 1)):
                    syslog.syslog('{0}: {1} DKIM-Signature field added (s={2} '
                                  'd={3})'.format(self.getsymval('i'),
                                                  d.signature_fields.get(b'a'),
                                                  d.signature_fields.get(b's'),
                                                  d.domain.lower()))
        except dkim.DKIMException as x:
            if milterconfig.get('Syslog'):
                syslog.syslog('DKIM: {0}'.format(x))
        except Exception as x:
            if milterconfig.get('Syslog'):
                syslog.syslog("sign_dkim: {0}".format(x))
            raise

    def check_dkim(self, txt):
        res = False
        self.header_a = None
        for y in range(self.has_dkim):  # Verify _ALL_ the signatures
            d = dkim.DKIM(txt)
            try:
                res = d.verify(idx=y)
                if res:
                    if d.signature_fields.get(b'a') == 'ed25519-sha256':
                        self.dkim_comment = ('Good {0} signature'
                                             .format(d.signature_fields
                                                     .get(b'a')))
                    else:
                        self.dkim_comment = ('Good {0} bit {1} signature'
                                             .format(d.keysize,
                                                     d.signature_fields
                                                     .get(b'a')))
                else:
                    self.dkim_comment = ('Bad {0} bit {1} signature.'
                                         .format(d.keysize,
                                                 d.signature_fields.get(b'a')))
            except dkim.DKIMException as x:
                self.dkim_comment = str(x)
                if milterconfig.get('Syslog'):
                    syslog.syslog('DKIM: {0}'.format(x))
            except Exception as x:
                self.dkim_comment = str(x)
                if milterconfig.get('Syslog'):
                    syslog.syslog("check_dkim: Internal program fault while verifying: {0}".format(x))
            try:
                self.header_i = d.signature_fields.get(b'i')
            except TypeError as x:
                self.header_i = None
            try:
                self.header_d = d.signature_fields.get(b'd')
                self.header_a = d.signature_fields.get(b'a')
            except Exception as x:
                self.dkim_comment = str(x)
                if milterconfig.get('Syslog'):
                    syslog.syslog("check_dkim: Internal proram fuault extracting header a or d: {0}".format(x))
                self.header_d = None
            if not self.header_a:
                self.header_a = 'rsa-sha256'
            if res:
                if (milterconfig.get('Syslog') and
                        (milterconfig.get('SyslogSuccess') or
                         milterconfig.get('debugLevel') >= 1)):
                    syslog.syslog('{0}: {1} DKIM signature verified (s={2} '
                                  'd={3})'.format(self.getsymval('i'),
                                                  d.signature_fields.get(b'a'),
                                                  d.signature_fields.get(b's'),
                                                  d.domain.lower()))
                self.dkim_domain = d.domain.lower()
            else:
                if milterconfig.get('DiagnosticDirectory'):
                    fd, fname = tempfile.mkstemp(".dkim")
                    with os.fdopen(fd, "w+b") as fp:
                        fp.write(txt)
                    if milterconfig.get('Syslog'):
                        syslog.syslog('DKIM: Fail (saved as {0})'
                                      .format(fname))
                else:
                    if milterconfig.get('Syslog'):
                        if d.domain:
                            syslog.syslog('DKIM: Fail ({0})'
                                          .format(d.domain.lower()))
                        else:
                            syslog.syslog('DKIM: Fail, unextractable domain')
            if res:
                result = 'pass'
            else:
                result = 'fail'
            res = False
            if self.header_d:
                self.arresults.append(
                    authres.DKIMAuthenticationResult(result=result,
                                                 header_i=self.header_i,
                                                 header_d=self.header_d,
                                                 header_a=self.header_a,
                                                 result_comment=
                                                 self.dkim_comment)
            )
            self.header_a = None
        return


def main():
    # Ugh, but there's no easy way around this.
    global milterconfig
    global privateRSA
    global privateEd25519
    privateRSA = False
    privateEd25519 = False
    configFile = '/usr/local/etc/dkimpy-milter.conf'
    if len(sys.argv) > 1:
        if sys.argv[1] in ('-?', '--help', '-h'):
            print('usage: dkimpy-milter [<configfilename>]')
            sys.exit(1)
        configFile = sys.argv[1]
    milterconfig = config._processConfigFile(filename=configFile)
    if milterconfig.get('Syslog'):
        facility = eval("syslog.LOG_{0}"
                        .format(milterconfig.get('SyslogFacility').upper()))
        syslog.openlog(os.path.basename(sys.argv[0]), syslog.LOG_PID, facility)
        setExceptHook()
    pid = write_pid(milterconfig)
    if milterconfig.get('KeyFile'):
        privateRSA = read_keyfile(milterconfig, 'RSA')
    if milterconfig.get('KeyFileEd25519'):
        privateEd25519 = read_keyfile(milterconfig, 'Ed25519')
    Milter.factory = dkimMilter
    Milter.set_flags(Milter.CHGHDRS + Milter.ADDHDRS)
    miltername = 'dkimpy-filter'
    socketname = milterconfig.get('Socket')
    drop_privileges(milterconfig)
    sys.stdout.flush()
    if milterconfig.get('Syslog'):
        syslog.syslog('dkimpy-milter starting:{0} user:{1}'
                      .format(pid, milterconfig.get('UserID')))
    Milter.runmilter(miltername, socketname, 240)

if __name__ == "__main__":
    main()
