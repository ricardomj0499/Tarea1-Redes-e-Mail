# imports

import os

from twisted.mail import smtp, maildir # 

from twisted.internet import protocol, reactor, defer # 

from zope.interface import implementer # 

from email.header import Header

# Documentación: https://twistedmatrix.com/documents/current/api/twisted.mail.html

'''
Clase 
'''
@implementer(smtp.IMessage)
class MaildirMessageWriter(object):

    def __init__(self, userDir):
        print("Init MaildirMessageWriter, función")
        if(not os.path.exists(userDir)):
            print("entro al if, está creando el path") 
            os.mkdir(userDir)

        inboxDir = os.path.join(userDir, 'Inbox')
        print("inbox dear: ", inboxDir)
        self.mailbox = maildir.MaildirMailbox(inboxDir)

        self.lines = []



    def lineReceived(self, line):
        print("linea recibida 2 función")
        if type(line) != str:
            line = line.decode("utf-8")
        self.lines.append(line)



    def eomReceived(self):

        # message is complete, store it

        print("Message data complete.")

        self.lines.append('') # add a trailing newline

        messageData = '\n'.join(self.lines)
        print("messageData: ", messageData)
        return self.mailbox.appendMessage(bytes(messageData, "UTF-8"))



    def connectionLost(self):

        print("Connection lost unexpectedly!")

        # unexpected loss of connection; don't save
        del(self.lines)


@implementer(smtp.IMessageDelivery)
class LocalDelivery(object):


    def __init__(self, baseDir, validDomains):
        print("Entro a init de Local Delivery")

        if not os.path.isdir(baseDir):

            raise ValueError#, "%s is not a directory" % baseDir

        self.baseDir = baseDir
        print("base dir: ",baseDir)
        self.validDomains = validDomains



    def receivedHeader(self, helo, origin, recipients):
        print("entre a receivedHeader")
        myHostname, clientIP = helo

        headerValue = "by %s from %s with ESMTP ; %s" % (

        myHostname.decode(), clientIP.decode(), smtp.rfc822date().decode())

        # email.Header.Header used for automatic wrapping of long lines

        return "Received: %s" % Header(headerValue)



    def validateTo(self, user):

        print("valida to to: ", user)
        if not user.dest.domain.decode("UTF-8") in self.validDomains:

            raise smtp.SMTPBadRcpt(user)

        print("Accepting mail for %s..." % user.dest)

        return lambda: MaildirMessageWriter(self._getAddressDir(str(user.dest)))



    def _getAddressDir(self, address):
        print("get adress dir")
        return os.path.join(self.baseDir, "%s" % address)



    def validateFrom(self, helo, originAddress):
        print("validato from ", originAddress)
        # accept mail from anywhere. To reject an address, raise

        # smtp.SMTPBadSender here.
        return originAddress


class SMTPFactory(protocol.ServerFactory):

    def __init__(self, baseDir, validDomains):
        print()
        print("entre a init de SMTP factory")

        self.baseDir = baseDir
        if(os.path.exists(baseDir)):
            print("basedir= ", baseDir)
            print("si existe")
        else:
            print("No existe")
        self.validDomains = validDomains
        print(validDomains)



    def buildProtocol(self, addr):
        print("Building protocol")
        delivery = LocalDelivery(self.baseDir, self.validDomains)

        smtpProtocol = smtp.SMTP(delivery)

        smtpProtocol.factory = self

        return smtpProtocol


if __name__ == "__main__":

    print("He entrado al name==main")

    import sys

    mailboxDir = sys.argv[1]
    print("mailboxDir es: ", mailboxDir)

    domains = sys.argv[2].split(",")
    print("domains es: ", domains)

    reactor.listenTCP(1234, SMTPFactory(mailboxDir, domains))   

    from twisted.internet import ssl

    # SSL stuff here... and certificates...

    reactor.run( )