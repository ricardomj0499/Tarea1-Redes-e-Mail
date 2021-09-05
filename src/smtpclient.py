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

import csv

with open('employee_birthday.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
            line_count += 1
    print(f'Processed {line_count} lines.')