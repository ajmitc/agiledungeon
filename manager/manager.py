from persist.flatfilestore import FlatFileStore
from clientthread import ClientThread
from common.util import *
import socket, signal

class AgileDungeonManager:
    PROPERTIES_FILE = "server.prop"
    
    def __init__( self ):
        self._stop = False
        self.props = {}
        self.store = FlatFileStore()
        self.connections = []
        self.listen_socket = None
        signal.signal( signal.SIGINT, self.handle_signal )
        
        
    def run( self ):
        print "Loading %s" % self.PROPERTIES_FILE
        self.props = load_properties_file( self.PROPERTIES_FILE )
        self.open_server_socket()
        self.accept_connections()
        
        
    def open_server_socket( self ):
        port = int(self.props[ "port" ]) if "port" in self.props.keys() else 9876
        self.listen_socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        self.listen_socket.bind( (socket.gethostname(), port) )
        self.listen_socket.listen(5)
        print "Listening on %s port %d" % (socket.gethostname(), port)
        
        
    def accept_connections( self ):
        print "Waiting for clients..."
        while not self._stop:
            (clientsocket, address) = self.listen_socket.accept()
            print "Got client at %s, starting ClientThread..." % str(address)
            ct = ClientThread( clientsocket, address, self.store )
            ct.start()
            self.connections.append( (clientsocket, address, ct) )
        
    def handle_signal( self, sig, frame ):
        self.listen_socket.close()
        for sock, addr, ct in self.connections:
            ct._stop = True
            try:
                sock.close()
            except:
                pass
    