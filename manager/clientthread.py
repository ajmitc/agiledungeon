import threading
from common import error
from common.protocol import protocol
from common.protocol.proto_command import ProtocolCommand

class ClientThread( threading.Thread ):
    
    def __init__( self, sock, addr, store ):
        threading.Thread.__init__( self )
        self._stop = False
        self.sock  = sock
        self.addr  = addr
        self.store = store
        self.user  = None
        
        
    def debug( self, msg ):
        print "[%s] %s" % (str(self.addr), msg)
        
        
    def run( self ):
        success, response = self.validate_user()
        if not success:
            self.send_command( response )
            self.sock.close()
            return
        while not self._stop:
            cmd = self.sock.recv( 2048 )
            parsed_command = protocol.parse_command( cmd )    
            self.handle_command( parsed_command )
        
        
    def validate_user( self ):
        self.debug( "Validating user" )
        cmd = self.sock.recv( 2048 )
        self.debug( "Received '%s'" % str(cmd) )
        parsed_command = protocol.parse_command( cmd )
        if parsed_command is None:
            return False, protocol.create_error_response( cmd, error.ERROR_INVALID_COMMAND, "Cannot parse '%s'" % cmd )
        if parsed_command.command == ProtocolCommand.LOGIN:
            return self.handle_login( parsed_command, False )
        elif parsed_command.command == ProtocolCommand.REGISTER:
            return self.handle_register( parsed_command, False )
        else:
            return False, protocol.create_error_response( parsed_command, error.ERROR_OUT_OF_ORDER_COMMAND, "Received unexpected command" )
        
    
    def handle_command( self, cmd ):
        if cmd is None:
            return
        success, response = self.validate_hash( cmd )
        if not success:
            self.send_command( response )
            return
        if cmd.command == ProtocolCommand.DISCONNECT:
            self._stop = True
            self.sock.close()
        elif parsed_command.command == ProtocolCommand.LOGIN:
            self.handle_login( parsed_command )
        elif parsed_command.command == ProtocolCommand.REGISTER:
            self.handle_register( parsed_command )
        elif cmd.command == ProtocolCommand.GETGAMES:
            self.handle_get_games( cmd )
        elif cmd.command == ProtocolCommand.JOIN:
            self.handle_join( cmd )
        else:
            resp = cmd.get_error_response( error.ERROR_UNSUPPORTED_COMMAND, "Unsupported command: '%s'" % cmd.command )
            self.send_command( resp )
    
    
    def handle_login( self, cmd, sendcmds=True ):
        self.debug( "Loading users" )
        self.store.lock_users()
        users = self.store.load_users()
        for user in users:
            if user.username == cmd.username:
                self.debug( "Found matching username, checking password..." )
                success, resp = user.login( cmd.username, cmd.password )
                if success:
                    self.debug( "Login success" )
                    self.store.save_users( users )
                else:
                    self.debug( "Login failed!" )
                self.store.unlock_users()
                if sendcmds:
                    self.send_command( resp )
                return success, resp
        self.store.unlock_users()
        self.debug( "Username not found" )
        resp = cmd.get_response()
        resp.args.append( False )
        resp.args.append( "Username not registered" )
        if sendcmds:
            self.send_command( resp )
        return False, resp
    
    
    def handle_register( self, cmd, sendcmds=True ):
        self.debug( "Loading users" )
        self.store.lock_users()
        users = self.store.load_users()
        for user in users:
            if user.username == cmd.username:
                self.debug( "Username already registered" )
                self.store.unlock_users()
            	resp = cmd.get_response()
                resp.args.append( False )
                resp.args.append( "Username already registered" )
                if sendcmds:
                    self.send_command( resp )
                return False, resp
        self.debug( "Creating new user: %s" % cmd.username )
        user = User( cmd.username, cmd.password )
        user.login( cmd.username, cmd.password )
        users.append( user )
        self.debug( "Saving users" )
        self.store.save_users( users )
        self.store.unlock_users()
        resp = cmd.get_response()
        resp.args.append( user.hash )
        if sendcmds:
            self.send_command( resp )
        return True, resp
    
    
    def handle_get_games( self, cmd ):
        """
        GETGAMES|hash
        RGETGAMES|game1|game2|...
        """
        self.debug( "Loading games" )
        self.store.lock_games()
        games = self.store.load_games()
        self.store.unlock_games()
        resp = cmd.get_response()
        for g in games:
        	resp.args.append( str(g) )
        self.send_command( resp )
    
    
    def handle_join( self, cmd ):
        """
        JOIN|hash|gameid
        """
        pass
    
    def myreceive( self ):
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == '':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return ''.join(chunks)
    
    
    def send_command( self, cmd ):
        self.debug( "Sending '%s'" % cmd.pack() )
        self.sock.send( cmd.pack() )
        
        
   
            
        
        