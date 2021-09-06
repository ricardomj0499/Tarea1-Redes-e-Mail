# imports
# command
# python3 smtpserver.py -d localhost,example.com,gmail.com -s /home/ricardo/Desktop/semestre8/redes/Tarea1-Redes-e-Mail/storage/ -p 1234

import os
from sys import setdlopenflags

from twisted.mail import smtp, maildir # Twisted Mail se encarga básicamente de todo lo relacionado a servers y clientes para smtop, pop e imap
from twisted.internet import protocol, reactor, defer # eventos de Entrada y Salida asincronos
from zope.interface import implementer # Zope provee una implementación de interfaces de objetos para python
from email.header import Header # Usado principalmente para aplicaciones que ocupen control del set de caracteres usados en los encabezados

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
    def __init__(self, userDir): # user dir = carpeta storage más correo

        if(not os.path.exists(userDir)):
            os.mkdir(userDir)
            
        inboxDir = os.path.join(userDir, 'Inbox') # Carpeta Inboc donde guardará los correos

        self.mailbox = maildir.MaildirMailbox(inboxDir) # Creará el inbox automaticamente
        self.lines = []


    '''
    Función llamada por cada linea del mensaje entrante
    '''
    def lineReceived(self, line):
        if type(line) != str:
            line = line.decode("utf-8")
        self.lines.append(line)


    '''
    Una vez todas el mensaje se lee complemante se llama
    '''
    def eomReceived(self):
        print("Message data complete.") # cuando se termina de cargar el mensaje, se guarda

        self.lines.append('') # add a trailing newline

        messageData = '\n'.join(self.lines)
        print("messageData: ", messageData)

        return self.mailbox.appendMessage(bytes(messageData, "UTF-8"))
    

    '''
    Usada en caso de que la energía se vaya
    '''
    def connectionLost(self):
        print("Connection lost unexpectedly!")
        del(self.lines) # Sí se pierde la conexión no se guarda el mensaje


@implementer(smtp.IMessageDelivery)
class LocalDelivery(object):

    def __init__(self, baseDir, validDomains):
        if not os.path.isdir(baseDir):
            raise ValueError # En cas de que baseDir no sea un directorio

        self.baseDir = baseDir # es la carpeta Storage
        self.validDomains = validDomains


    '''
    genera un encabezado "received" que será agregado al al email entrante
    el smtp es el encargado de agregar este encabezado a los mensajes entrantes
    helo: (server name al que el ciente se dirigió, client IP Adress)
    origin: es un smtp.addres que identifica de quien viene el mensaje
    recipients: lista de smtp.addres de a quien va el mensaje
    '''
    def receivedHeader(self, helo, origin, recipients):
        myHostname, clientIP = helo
        headerValue = "by %s from %s with ESMTP ; %s" % (myHostname.decode(), clientIP.decode(), smtp.rfc822date().decode())

        return "Received: %s" % Header(headerValue)


    '''
    Acepta o rechaza los emails dependiendo de quien vienen
    User contiene información de la dirrección del recipiente e info desde donde viene el mensaje
    '''
    def validateTo(self, user):

        if not user.dest.domain.decode("UTF-8") in self.validDomains:
            raise smtp.SMTPBadRcpt(user)

        print("Accepting mail for %s..." % user.dest)

        return lambda: MaildirMessageWriter(self._getAddressDir(str(user.dest)))


    def _getAddressDir(self, address):
        return os.path.join(self.baseDir, "%s" % address)


    '''
    validateFrom takes two arguments: a tuple with the hostname used in by the client when it said HELO and the client's IP address
    tupla (hostname usado por el cliente cuando dice "helo", y la dirección IP del cliente)
    y un smtp.adrres que identifica el enviador(sender)
    '''
    # RicardoM # server name al que el ciente se dirigió, client IP Adress
    def validateFrom(self, helo, originAddress): 
        if not helo:
            raise smtp.SMTPBadSender(originAddress, 503, "Who are you?  Say HELO first.")
        if not originAddress.domain:
            raise smtp.SMTPBadSender(originAddress, 501, "Sender address must contain domain.")

        return originAddress


class SMTPFactory(protocol.ServerFactory):

    def __init__(self, baseDir, validDomains):

        self.baseDir = baseDir
        self.validDomains = validDomains

        print("smtp factory valid domains", validDomains)



    def buildProtocol(self, addr):
        delivery = LocalDelivery(self.baseDir, self.validDomains)
        smtpProtocol = smtp.SMTP(delivery)

        smtpProtocol.factory = self

        return smtpProtocol


if __name__ == "__main__":
    import sys
    d = s = p = 0
    domains = mailboxDir =  port = ''
    
    try:
        d = sys.argv.index('-d')
        s = sys.argv.index('-s')
        p = sys.argv.index('-p')

        domains = (sys.argv)[d+1].split(',') # Dominios que acepta
        mailboxDir = sys.argv[s+1] # Lugar donde se guardarán los correos
        port = sys.argv[p+1] # Puerto al que escuchará el server
    except NameError as e:
        print("a", e)
    

    reactor.listenTCP(int(port), SMTPFactory(mailboxDir, domains))   

    from twisted.internet import ssl

    # SSL stuff here... and certificates...

    reactor.run( )