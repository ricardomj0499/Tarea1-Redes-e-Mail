from twisted.internet import ssl
from twisted.mail import smtp, maildir
from zope.interface import implementer
from twisted.internet import protocol, reactor, defer
import os
from email.header import Header


@implementer(smtp.IMessage)
class MailMessageStorage(object):

    def __init__(self, mail_storage):
        if not os.path.exists(mail_storage): os.mkdir(mail_storage)

        inbox_storage = os.path.join(mail_storage, 'Inbox')
        self.mailbox = maildir.MaildirMailbox(inbox_storage)
        self.lines = []

    def lineReceived(self, line):
        if type(line) != str:
            line = line.decode("utf-8")
        self.lines.append(line)

    def eomReceived(self):
        # message is complete, store it

        print("Message data complete.")

        self.lines.append('') # add a trailing newline
        print(self.lines)
        messageData = '\n'.join(self.lines)
        return self.mailbox.appendMessage(bytes(messageData,"utf-8"))

    def connectionLost(self):

        print("Connection lost unexpectedly!")

        del self.lines


@implementer(smtp.IMessageDelivery)
class LocalDelivery(object):

    def __init__(self, baseDir, validDomains):

        if not os.path.isdir(baseDir):
            raise ValueError( "'%s' is not a directory" % baseDir)

        self.baseDir = baseDir

        self.validDomains = validDomains

    def receivedHeader(self, helo, origin, recipients):

         myHostname, clientIP = helo

         headerValue = "by %s from %s with ESMTP ; %s" % (myHostname.decode(), clientIP.decode(), smtp.rfc822date().decode())

         # email.Header.Header used for automatic wrapping of long lines

         return "Received: %s" % Header(headerValue)

    def validateTo(self, user):
        print(user.dest.domain)
        print(self.validDomains)
        if not user.dest.domain.decode("utf-8") in self.validDomains:

            raise smtp.SMTPBadRcpt(user)

        print("Accepting mail for %s..." % user.dest)

        return lambda: MailMessageStorage(self._getAddressDir(str(user.dest)))

    def _getAddressDir(self, address):

        return os.path.join(self.baseDir, "%s" % address)

    def validateFrom(self, helo, originAddress):

         # accept mail from anywhere. To reject an address, raise

         # smtp.SMTPBadSender here.

         return originAddress

class SMTPFactory(protocol.ServerFactory):

    def __init__(self, baseDir, validDomains):

        self.baseDir = baseDir

        self.validDomains = validDomains

    def buildProtocol(self, addr):
        delivery = LocalDelivery(self.baseDir, self.validDomains)

        smtpProtocol = smtp.SMTP(delivery)

        smtpProtocol.factory = self

        return smtpProtocol

if __name__ == "__main__":

    import sys

    mailboxDir = sys.argv[1]

    domains = sys.argv[2].split(",")

    reactor.listenTCP(1234, SMTPFactory(mailboxDir, domains))

    '''reactor.listenSSL(8000,SMTPFactory(mailboxDir, domains),
                      ssl.DefaultOpenSSLContextFactory(
                          'example.key', 'example.crt'))'''

    # SSL stuff here... and certificates...

    reactor.run( )