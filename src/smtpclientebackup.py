from email import charset, message
import sys

from email.mime.text import MIMEText

from twisted.internet import reactor
from twisted.mail.smtp import sendmail
from twisted.python import log

# log.startLogging(sys.stdout)

import csv

if __name__ == "__main__":

    h = c = m = 0
    mailServer = csvFile = messageS = ''

    listRecipientes = []

    try:
        h = sys.argv.index('-h')
        c = sys.argv.index('-c')
        m = sys.argv.index('-m')

        mailServer = (sys.argv)[h+1] # Dominios que acepta
        print("mail", mailServer)
        csvFile = sys.argv[c+1] # Lugar donde se guardarán los correos
        print("este es csv",csvFile)
        messageS = sys.argv[m+1:] # Puerto al que escuchará el server
        print("messfa",messageS)
    except NameError as e:
        print(e)

    with open(csvFile, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            print(row[0])
            listRecipientes.append(row[0])
        print(listRecipientes)


    host = "127.0.0.1" # 
    sender = "testEmisor1@localhost" # 

    
    MSG = ' '.join([str(item) for item in messageS])
    print(MSG)
    msg = MIMEText(MSG)
    msg["Subject"] = "Correo de prueba"
    msg["From"] = sender
    msg["To"] = ", ".join(listRecipientes)

    deferred = sendmail(host, sender, listRecipientes, msg   , port=1234)
    deferred.addBoth(lambda result: reactor.stop())

    reactor.run()
