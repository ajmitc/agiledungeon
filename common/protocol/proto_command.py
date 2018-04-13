import xml.etree.ElementTree as ET
from common.xml_util import write_xml

class ProtocolCommand:
    ERROR       = "ERROR"       # ERROR|command|code|message
    REGISTER    = "REGISTER"    # REGISTER||username|password
    RREGISTER   = "RREGISTER"   # RREGISTER|success?|failure_reason|username|password
    LOGIN       = "LOGIN"       # LOGIN||username|password
    RLOGIN      = "RLOGIN"      # RLOGIN|success?|hash or reason
    GETGAMES    = "GETGAMES"    # GETGAMES|hash
    RGETGAMES   = "RGETGAMES"   # RGETGAMES|game1|game2|...
    NEWGAME     = "NEWGAME"     # NEWGAME|hash|name|visibility|invite1|invite2|...
    RNEWGAME    = "RNEWGAME"    # RNEWGAME|success?|game_id_or_error
    JOIN        = "JOIN"        # JOIN|hash|game_id
    RJOIN       = "RJOIN"       # RJOIN|success?|game_id_or_error
    CONTROL     = "CONTROL"     # Take control of hero
    RCONTROL    = "RCONTROL"    # Respond to take control of hero
    GAMEUPDATE  = "GAMEUPDATE"  # Request a game update args: game:id
    RGAMEUPDATE = "RGAMEUPDATE"
    DISCONNECT  = "DISCONNECT"  # DISCONNECT|hash
    
    def __init__( self, cmd="" ):
        self.command = cmd
        self.hash = ""
        self.args = {}
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
            self.RGETGAMES,
            self.RNEWGAME,
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
            #fields = [ self.ERROR, str(self.error_command), str(self.error_code), self.error_msg if self.error_msg is not None else "Error message not given" ]
            root = ET.Element( self.ERROR )
            root.set( "command", self.error_command )
            root.set( "code", self.error_code )
            root.text = self.error_msg
        else:
            #fields = [ self.command ]
            root = ET.Element( self.command )
            if not self.is_response():
                #fields.append( self.hash )
                root.set( "hash", self.hash )
            #fields += [ str(arg) for arg in self.args ]
            for key, value in self.args.iteritems():
                el = ET.SubElement( root, key )
                if isinstance( value, str ):
                    el.set( "type", "string" )
                    el.text = value
                elif isinstance( value, int ) or isinstance( value, long ) or isinstance( value, float ) or isinstance( value, bool ):
                    el.set( "type", type(value).__name__ )
                    el.text = str(value)
                elif callable( getattr( value, "to_xml" ) ):
                    el.set( "type", "object" )
                    el.append( value.to_xml() )
        #return "|".join( fields )
        return write_xml( root )


    def unpack( self, xml ):
        self.command = xml.tag
        if self.command == self.ERROR:
            self.error_command = xml.get( "command" )
            self.error_code = xml.get( "code" )
            self.error_msg = xml.text
        else:
            self.hash = xml.get( "hash" )
            for el in xml:
                if el.get( "type" ) == "string":
                    self.args[ el.tag ] = el.text
                elif el.get( "type" ) == "int":
                    self.args[ el.tag ] = int(el.text)
                elif el.get( "type" ) == "long":
                    self.args[ el.tag ] = long(el.text)
                elif el.get( "type" ) == "float":
                    self.args[ el.tag ] = float(el.text)
                elif el.get( "type" ) == "bool":
                    self.args[ el.tag ] = el.text.lower() in [ "t", "true", "y", "yes", "1" ]
                elif el.get( "type" ) == "object":
                    self.args[ el.tag ] = el

    
        

class LoginRegisterCommand( ProtocolCommand ):
    # REGISTER||username|password
    # LOGIN||username|password
    def __init__( self, parsed_command ):
        ProtocolCommand.__init__( self, parsed_command.command )
        self.username = parsed_command.args[ 'username' ]
        self.password = parsed_command.args[ 'password' ]


