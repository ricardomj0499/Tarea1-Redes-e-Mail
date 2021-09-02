import sys

from email.mime.text import MIMEText

from twisted.internet import reactor
from twisted.mail.smtp import sendmail
from twisted.python import log

#
# Errata note: your ISP may block connections to port 25 from residential IP
# addresses as a spam prevention measure. If this is the case, the sendmail
# function will retry transmission a few times and then eventually give up:
#
#    SMTP Client retrying server. Retry: 5
#    SMTP Client retrying server. Retry: 4
#    SMTP Client retrying server. Retry: 3
#    SMTP Client retrying server. Retry: 2
#    SMTP Client retrying server. Retry: 1
#    Stopping factory <twisted.mail.smtp.SMTPSenderFactory instance at 0x1485ea8>
#    Main loop terminated.
#

# log.startLogging(sys.stdout)

host = "localhost"
sender = "ricardo@gmail.com"
recipients = ["ricardo@gmail.com,test@localhost,test@example.com"]

msg = MIMEText("""Violets are blue
Twisted is helping
Forge e-mails to you!
""")
msg["Subject"] = "Roses are red"
msg["From"] = '"Secret Admirer" <%s>' % (sender,)
msg["To"] = ", ".join(recipients)

deferred = sendmail(host, sender, recipients, msg.as_string().encode("UTF-8"), port=1234)
deferred.addBoth(print)

reactor.run()