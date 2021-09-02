from twisted.internet import protocol, reactor, endpoints

class Echo(protocol.Protocol):
    def dataReceived(self, data):
        print(data)
        self.transport.write(data)

class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
        print("sobody has conected")
        print(addr)
        return Echo()

endpoints.serverFromString(reactor, "tcp:1234").listen(EchoFactory())
reactor.run()