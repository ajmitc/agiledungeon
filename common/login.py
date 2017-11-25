from proto_command import ProtocolCommand

class Login( ProtocolCommand ):
	def __init__( self ):
    	ProtocolCommand.__init__( self, ProtocolCommand.LOGIN )
        self.username = None
        self.password = None
        
        
    def parse_args( self, args ):
    	self.username = args[ 0 ]
        self.password = args[ 1 ]