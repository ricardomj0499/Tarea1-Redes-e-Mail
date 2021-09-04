from email import charset
import sys

from email.mime.text import MIMEText

from twisted.internet import reactor
from twisted.mail.smtp import sendmail
from twisted.python import log

# log.startLogging(sys.stdout)

host = "127.0.0.1"
sender = "testEmisor1@localhost"
recipients = ["testReceptor1@example.com"]

msg = MIMEText("""Hello, How Are you 
a
""")
msg["Subject"] = "Correo de prueba"
msg["From"] = sender
msg["To"] = ", ".join(recipients)

deferred = sendmail(host, sender, recipients, msg   , port=1234)
deferred.addBoth(lambda result: reactor.stop())

reactor.run()