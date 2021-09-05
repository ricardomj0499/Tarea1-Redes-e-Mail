
from twisted.internet import protocol, defer

from twisted.mail import imap4

class IMAPFolderListProtocol(imap4.IMAP4Client):
    def serverGreeting(self, capabilities):
        print("server greeting")
        login = self.login(self.factory.username, self.factory.password)

        login.addCallback(self._loggedIn)

        login.chainDeferred(self.factory.deferred)

    def __loggedIn(self, results):
        print("logged in")
        return self.list("", "*").addCallback(self.__gotMailboxList)

    def __gotMailboxList(self, list):
        print("gotMailoxList")
        return [boxInfo[2] for boxInfo in list]



    def connectionLost(self, reason):
        print("connection lost")
        if not self.factory.deferred.called:

            # connection was lost unexpectedly!

            self.factory.deferred.errback(reason)



class IMAPFolderListFactory(protocol.ClientFactory):

    protocol = IMAPFolderListProtocol



    def __init__(self, username, password):
        print("init IMAP folder list Factort")
        self.username = username

        self.password = password

        self.deferred = defer.Deferred( )



    def clientConnectionFailed(self, connection, reason):
        print("clinet connection Failed")
        self.deferred.errback(reason)



if __name__ == "__main__":
    print("+++get in the main")
    from twisted.internet import reactor

    import sys, getpass



    def printMailboxList(list):
        print("+++get in printMailBoxList")
        list.sort( )
        print("list: ", list)
        for box in list:

            print(box)

        reactor.stop( )



    def handleError(error):
        print("+++get in habdle error")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(error)
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        
        print >> sys.stderr, "Error:", error.getErrorMessage( )

        reactor.stop( )



    if not len(sys.argv) == 3:
        print("+++ verificación largo")
        print(len(sys.argv))
        print("Usage: %s server login" % sys.argv[0])

        sys.exit(1)



    server = sys.argv[1]
    print(sys.argv[1])
    user = sys.argv[2]
    print(sys.argv[2])
    password = getpass.getpass("Password: ")

    factory = IMAPFolderListFactory(user, password)
    print("después del facotry")
    factory.deferred.addCallback(printMailboxList).addErrback(handleError)

    reactor.connectTCP(server, 1344, factory)
    print("segundo fatoru")
    reactor.run( )