#import sys


#print('Number of Arguments: ', len(sys.argv))
#print('A: ', str(sys.argv))
#print("+++++++++++++++++++this++++++++++++++++++++++")

from twisted.application import service
application = service.Application("SMTP Client Tutorial")

#print("+++++++++++++++++++this++++++++++++++++++++++")

from twisted.application import internet
from twisted.internet import protocol

smtpClientFactory = protocol.ClientFactory()
smtpClientFactory.protocol = smtp.ESMTPClient

smtpClientService = internet.TCPClient("localhost", 25, smtpClientFactory)
smtpClientService.setServiceParent(application)

