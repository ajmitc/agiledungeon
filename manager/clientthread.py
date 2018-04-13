import threading
from common import error
from common.protocol import protocol
from common.protocol.proto_command import ProtocolCommand, LoginRegisterCommand
from common.game import Game
from common.xml_util import parse_xml
from user.user import User

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
        done = False
        while not done:
            success, response = self.validate_user()
            self.send_command( response )
            if success:
                done = True
        if self.user is None:
            print "User is not registered and logged in, closing connection"
            self.sock.close()
            return
        self.debug( "Entering game loop" )
        while not self._stop:
            cmd = self.sock.recv( 2048 )
            print "<= %s" % cmd
            #parsed_command = protocol.parse_command( cmd )
            parsed_command = ProtocolCommand()
            parsed_command.unpack( parse_xml( xmlstring=cmd ) )
            self.handle_command( parsed_command )
        
        
    def validate_user( self ):
        self.debug( "Validating user" )
        cmd = self.sock.recv( 2048 )
        self.debug( "Received '%s'" % str(cmd) )
        #parsed_command = protocol.parse_command( cmd )
        parsed_command = ProtocolCommand()
        parsed_command.unpack( parse_xml( xmlstring=cmd ) )
        #if parsed_command is None:
            #return False, protocol.create_error_response( cmd, error.ERROR_INVALID_COMMAND, "Cannot parse '%s'" % cmd )
        if parsed_command.command == ProtocolCommand.LOGIN:
            return self.handle_login( parsed_command, False )
        elif parsed_command.command == ProtocolCommand.REGISTER:
            return self.handle_register( parsed_command, False )
        else:
            return False, protocol.create_error_response( parsed_command, error.ERROR_OUT_OF_ORDER_COMMAND, "Received unexpected command" )


    def validate_hash( self, cmd ):
        # TODO Implement this
        return True, None


    def lookup_user( self, hash ):
        ret = None
        self.store.lock_users()
        users = self.store.load_users()
        for user in users:
            if user.hash == hash:
                ret = user
                break
        self.store.unlock_users()
        return ret


    def lookup_game( self, gameid ):
        ret = None
        self.store.lock_games()
        games = self.store.load_games()
        for game in games:
            if game.id == gameid:
                ret = game
                break
        self.store.save_games( games )
        self.store.unlock_games()
        return ret


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
        elif cmd.command == ProtocolCommand.LOGIN:
            self.handle_login( cmd )
        elif cmd.command == ProtocolCommand.REGISTER:
            self.handle_register( cmd )
        elif cmd.command == ProtocolCommand.GETGAMES:
            self.handle_get_games( cmd )
        elif cmd.command == ProtocolCommand.NEWGAME:
            self.handle_newgame( cmd )
        elif cmd.command == ProtocolCommand.JOIN:
            self.handle_join( cmd )
        elif cmd.command == ProtocolCommand.CONTROL:
            self.handle_control_hero( cmd )
        elif cmd.command == ProtocolCommand.GAMEUPDATE:
            self.handle_get_game_update( cmd )
        else:
            self.debug( "Received unsupported command: '%s'" % cmd.command )
            resp = cmd.get_error_response( error.ERROR_UNSUPPORTED_COMMAND, "Unsupported command: '%s'" % cmd.command )
            self.send_command( resp )
    
    
    def handle_login( self, cmd, sendcmds=True ):
        cmd = LoginRegisterCommand( cmd )
        self.debug( "Loading users" )
        self.store.lock_users()
        users = self.store.load_users()
        for user in users:
            if user.username == cmd.username:
                self.debug( "Found matching username, checking password..." )
                success, hash_or_reason = user.login( cmd.username, cmd.password )
                resp = cmd.get_response()
                resp.args[ 'success' ] = success
                if success:
                    self.debug( "Login success" )
                    self.store.save_users( users )
                    self.user = user
                    resp.args[ 'hash' ] = hash_or_reason
                    resp.args[ 'username' ] = cmd.username
                else:
                    self.debug( "Login failed!" )
                    resp.args[ 'reason' ] = hash_or_reason
                self.store.unlock_users()
                if sendcmds:
                    self.send_command( resp )
                return success, resp
        self.store.unlock_users()
        self.debug( "Username not found" )
        resp = cmd.get_response()
        resp.args[ 'success' ] = False
        resp.args[ 'reason' ] = "Username not registered"
        if sendcmds:
            self.send_command( resp )
        return False, resp
    
    
    def handle_register( self, cmd, sendcmds=True ):
        cmd = LoginRegisterCommand( cmd )
        self.debug( "Loading users" )
        self.store.lock_users()
        users = self.store.load_users()
        for user in users:
            if user.username == cmd.username:
                self.debug( "Username already registered" )
                self.store.unlock_users()
            	resp = cmd.get_response()
                resp.args[ 'succes' ] = False
                resp.args[ 'reason' ] = "Username already registered"
                if sendcmds:
                    self.send_command( resp )
                return False, resp
        self.debug( "Creating new user: %s" % cmd.username )
        self.user = User( cmd.username, cmd.password )
        self.user.login( cmd.username, cmd.password )
        users.append( self.user )
        self.debug( "Saving users" )
        self.store.save_users( users )
        self.store.unlock_users()
        resp = cmd.get_response()
        resp.hash = user.hash
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
            resp.args[ g.name ] = g
        self.send_command( resp )


    def handle_newgame( self, cmd ):
        """
        NEWGAME|hash|game-name|game-visibility
        """
        game = Game()
        game.name = cmd.args[ 0 ]
        if cmd.args[ 1 ].lower().startswith( "priv" ):
            game.visibility = Game.VISIBILITY_PRIVATE
            game.accessible_users.append( self.user.username )
        else:
            game.visibility = Game.VISIBILITY_PUBLIC
        game.new_game()
        print "Saving New Game"
        self.store.lock_games()
        games = self.store.load_games()
        games.append( game )
        self.store.save_games( games )
        self.store.unlock_games()
        print "Game Saved"
        resp = cmd.get_response()
        resp.args[ 'success' ] = "true"
        resp.args[ 'gameid' ] = game.id
        self.send_command( resp )
    
    
    def handle_join( self, cmd ):
        """
        JOIN|hash|gameid
        """
        pass


    def handle_control_hero( self, cmd ):
        hero_type = cmd.args[ 'type' ]
        gameid = cmd.args[ 'game' ]
        # Get user's username
        user = self.lookup_user( cmd.hash )
        # Lookup game by id
        success = False
        self.store.lock_games()
        games = self.store.load_games()
        for game in games:
            if game.id == gameid:
                hero = game.heroes[ hero_type ]
                if hero.player is None:
                    hero.player = user.username
        self.store.save_games( games )
        self.store.unlock_games()
        resp = cmd.get_response()
        resp.args[ 'success' ] = success
        if success:
            resp.args[ 'type' ] = hero_type
        else:
            resp.args[ 'reason' ] = "Hero is not available"
        self.send_command( resp )


    def handle_get_game_update( self, cmd ):
        gameid = cmd.args[ 'game' ]


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
        
        
   
            
        
        
