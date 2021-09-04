# imports

import os

from twisted.mail import smtp, maildir # 

from twisted.internet import protocol, reactor, defer # 

from zope.interface import implementer # 

from email.header import Header

# Documentación: https://twistedmatrix.com/documents/current/api/twisted.mail.html
# SMTP usualmente se usa solamente para el envío de correo
# de recibir usualmente se encarga POP3 o IMAP

'''
Acá se implementa una interface para recibir emails
'''
@implementer(smtp.IMessage)
class MaildirMessageWriter(object):

    '''
    Inicializador de la clase, Recibe el nombre del lugar a donde se guardarán los mensajes
    '''
    def __init__(self, userDir):
        print("Init MaildirMessageWriter, función")
        if(not os.path.exists(userDir)):
            print("entro al if, está creando el path") 
            os.mkdir(userDir)

        inboxDir = os.path.join(userDir, 'Inbox')
        print("inbox dear: ", inboxDir)
        self.mailbox = maildir.MaildirMailbox(inboxDir) # Creará el inbox automaticamente

        self.lines = []


    '''
    Función llamada por cada linea del mensaje entrante
    '''
    def lineReceived(self, line):
        print("linea recibida 2 función")
        if type(line) != str:
            line = line.decode("utf-8")
        self.lines.append(line)


    '''
    Una vez todas el mensaje se lee complemante se llama
    '''
    def eomReceived(self):

        # message is complete, store it

        print("Message data complete.")

        self.lines.append('') # add a trailing newline

        messageData = '\n'.join(self.lines)
        print("messageData: ", messageData)
        return self.mailbox.appendMessage(bytes(messageData, "UTF-8"))
    

    '''
    Usada en caso de que la energía se vaya
    '''
    def connectionLost(self):

        print("Connection lost unexpectedly!")
        # Sí se pierde la conexión no guarfa las lineas
        del(self.lines)

'''

'''
@implementer(smtp.IMessageDelivery)
class LocalDelivery(object):


    def __init__(self, baseDir, validDomains):
        print("Entro a init de Local Delivery")

        if not os.path.isdir(baseDir):

            raise ValueError#, "%s is not a directory" % baseDir

        self.baseDir = baseDir
        print("base dir: ",baseDir)
        self.validDomains = validDomains


    '''
    genera un encabezado "received" que será agregado al al email entrante
    el smtp es el encargado de agregar este encabezado a los mensajes entrantes
    helo: (server name al que el ciente se dirigió, client IP Adress)
    origin: es un smtp.addres que identifica de quien viene el mensaje
    recipients: lista de smtp.addres de a quien va el mensaje
    '''
    def receivedHeader(self, helo, origin, recipients):
        print("entre a receivedHeader")
        myHostname, clientIP = helo

        headerValue = "by %s from %s with ESMTP ; %s" % (myHostname.decode(), clientIP.decode(), smtp.rfc822date().decode())

        # email.Header.Header used for automatic wrapping of long lines

        return "Received: %s" % Header(headerValue)

    '''
    acepta o rechaza los emails dependiendo de quien vienen
    '''
    '''
    User contiene información de la dirrección del recipiente e info desde donde viene el mensaje
    '''
    def validateTo(self, user):

        print("valida to to: ", user)
    
        if not user.dest.domain.decode("UTF-8") in self.validDomains:

            raise smtp.SMTPBadRcpt(user)

        print("Accepting mail for %s..." % user.dest)

        return lambda: MaildirMessageWriter(self._getAddressDir(str(user.dest)))



    def _getAddressDir(self, address):
        print("get adress dir")
        return os.path.join(self.baseDir, "%s" % address)


    '''
    validateFrom takes two arguments: a tuple with the hostname used in by the client when it said HELO and the client's IP address
    tupla (hostname usado por el cliente cuando dice "helo", y la dirección IP del cliente)
    y un smtp.adrres que identifica el enviador(sender)
    '''
    def validateFrom(self, helo, originAddress):
        print("validato from ", originAddress)
        # accept mail from anywhere. To reject an address, raise
        if not helo:
            raise smtp.SMTPBadSender(originAddress, 503, "Who are you?  Say HELO first.")
        if not originAddress.domain:
            raise smtp.SMTPBadSender(originAddress, 501, "Sender address must contain domain.")
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
        print("delivery++++: ", delivery.baseDir)
        print("delivery++++: ", delivery.validDomains)
        smtpProtocol = smtp.SMTP(delivery)

        smtpProtocol.factory = self

        return smtpProtocol


if __name__ == "__main__":
    print("He entrado al name==main")
    import sys
    d = s = p = 0
    domains = mailboxDir =  port = ''

    try:
        d = sys.argv.index('-d')
        s = sys.argv.index('-s')
        p = sys.argv.index('-p')

        domains = (sys.argv)[d+1].split(',') # Dominios que acepta
        print("domains es: ", domains)
        mailboxDir = sys.argv[s+1] # Lugar donde se guardarán los correos
        print("mailboxDir es:", mailboxDir)
        port = sys.argv[p+1] # Puerto al que escuchará el server
        print("port es:",port)
    except NameError as e:
        print(e)
    

    reactor.listenTCP(int(port), SMTPFactory(mailboxDir, domains))   

    from twisted.internet import ssl

    # SSL stuff here... and certificates...

    reactor.run( )