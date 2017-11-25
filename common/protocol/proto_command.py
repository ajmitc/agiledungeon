class ProtocolCommand:
    ERROR      = "ERROR"       # ERROR|command|code|message
    REGISTER   = "REGISTER"    # REGISTER||username|password
    RREGISTER  = "RREGISTER"   # RREGISTER|success?|failure_reason|username|password
    LOGIN      = "LOGIN"       # LOGIN||username|password
    RLOGIN     = "RLOGIN"      # RLOGIN|success?|hash or reason
    GETGAMES   = "GETGAMES"    # GETGAMES|hash
    RGETGAMES  = "RGETGAMES"   # RGETGAMES|game1|game2|...
    NEWGAME    = "NEWGAME"     # NEWGAME|hash|name|visibility|invite1|invite2|...
    RNEWGAME   = "RNEWGAME"    # RNEWGAME|success?|game_id_or_error
    JOIN       = "JOIN"        # JOIN|hash|game_id
    RJOIN      = "RJOIN"       # RJOIN|success?|game_id_or_error
    DISCONNECT = "DISCONNECT"  # DISCONNECT|hash
    
    def __init__( self, cmd="" ):
        self.command = cmd
        self.hash = ""
        self.args = []
        # Command that generated the error
        self.error_command = None
        # Error code (see error.py)
        self.error_code = None
        # Human-friendly error message
        self.error_msg = None
        
        
    def parse_args( self, args ):
        """
        Should be implemented by sub-class to parse argument list
        """
    	pass
        
        
    def is_response( self ):
        return self.command in [
            self.ERROR,
            self.RREGISTER,
            self.RLOGIN,
            self.RJOIN,
        ]
    
    
    def get_response( self ):
        return ProtocolCommand( "R" + self.command )
    
    
    def get_error_response( self, code, msg ):
        resp = ProtocolCommand( self.ERROR )
        resp.error_command = self.command
        resp.error_code = code
        resp.error_msg = msg
        return resp
    
    
    def pack( self ):
        """
        Convert this Command to a string that can be transmitted between the manager and client
        """
        if self.error_code is not None:
            fields = [ self.ERROR, str(self.error_command), str(self.error_code), self.error_msg if self.error_msg is not None else "Error message not given" ]
        else:
            fields = [ self.command ]
            if not self.is_response():
                fields.append( self.hash )
            fields += [ str(arg) for arg in self.args ]
        return "|".join( fields )
    
    
        