import socket
import traceback
import threading
import time
from menu.mainmenu import MainMenu
from view.basicterminalview import BasicTerminalView
from common.game import Game
from common.protocol.proto_command import ProtocolCommand
from common.protocol.protocol import parse_command
from common.util import *
import signal


class ManagerRecvThread( threading.Thread ):
    def __init__( self, callback_obj ):
        threading.Thread.__init__( self )
        self._stop = False
        self.callback_obj = callback_obj
        
    def run( self ):
        self.callback_obj.sock.settimeout( 0.5 )
        while not self._stop:
            inp = None
            try:
                inp = self.callback_obj.sock.recv( 4096 )
                self.callback_obj.handle_manager_response( inp )
            except socket.timeout:
                continue
            except Exception, e:
                traceback.print_exc()
    

class AgileDungeonClient:
    PROPERTIES_FILE = "agiledungeon.prop"
	
    def __init__( self ):
        self._stop        = False
        self.do_debug     = True
        self.sock         = None
        self.manager_host = "localhost"
        self.manager_port = 0
        self.props = {
            "manager.host": "localhost",
            "manager.port": 9876,
            "manager.username": "",
            "manager.password": ""
        }
        self.view = BasicTerminalView()
        self.recvthread = ManagerRecvThread( self )
        self.hash = None
        # if None, games have not been retrieved, if empty, games retrieved, but none found
        self.games = None
        self.resp_cond = threading.Condition()
        self.waiting_for_response = False


    def debug( self, text ):
        if self.do_debug:
            print "[DEBUG] %s" % text
        
        
    def run( self ):
        self.props = load_properties_file( self.PROPERTIES_FILE )
        self.manager_host = self.props[ "manager.host" ] if "manager.host" in self.props.keys() else "box-codeanywhere"
        self.manager_port = self.props[ "manager.port" ] if "manager.port" in self.props.keys() else 9876
        self.get_manager_connection()
        if not self.attempt_connect():
            print "Failed to connect to manager" 
            return
        # Login to manager
        self.recvthread.start()
        self.login()
        # Wait for login response -> on_login_successful()
        
        
    def on_login_successful( self ):
        # Retrieve game list
        self.get_game_list( True )
        


    def display_mainmenu( self ):
        mainmenu = MainMenu( self )
        while not self._stop and not mainmenu.exit_menu:
            success, inp, selection_or_reason = self.view.display_menu( mainmenu )
            if not success:
                print selection_or_reason
                continue
            selection_or_reason.callback( inp )
        self.debug( "Exited mainmenu loop" )
        self._stop = True
        self.recvthread._stop = True
        # Sleep to let command receiver thread to exit
        time.sleep( 0.6 )
        self.sock.close()

            

            
    def get_manager_connection( self ):
    	done = False
        while not done:
            inp = raw_input( "Manager Connection (%s:%d)> " % (self.manager_host, self.manager_port))
            if inp == "":
                done = True
                continue
            try:
                self.manager_host, self.manager_port = inp.split( ":" )
                self.manager_port = int(self.manager_port)
                done = True
            except Exception, e:
                traceback.printStackTrace()
                
        
    def attempt_connect( self ):
        attempts = 0
        while attempts < 10:
            if self.connect():
                return True
            attempts += 1
        print "Failed to connect to manager %d times" % attempts
        return False
        
        
    def connect( self ):
        if self.sock is not None:
            try:
                self.sock.close()
            except:
            	pass
            self.sock = None
        self.sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        print "Connecting to (%s, %d)" % (self.manager_host, self.manager_port)
        self.sock.connect( (self.manager_host, self.manager_port) )
        return self.sock is not None
    
    
    def login( self ):
        username = self.props[ "manager.username" ] if "manager.username" in self.props.keys() else None
        password = self.props[ "manager.password" ] if "manager.password" in self.props.keys() else None
        if username is None or password is None:
            if not self.register():
                return
        logincmd = ProtocolCommand( ProtocolCommand.LOGIN )
        logincmd.args.append( username )
        logincmd.args.append( password )
        self.send_command( logincmd )
    
    
    def register( self ):
        print "Register an account"
        done = False
        while not done:
            username = raw_input( "Username: " ).strip()
            password = raw_input( "Password: " ).strip()
            if username is "" or password is "":
                print "Username and password cannot be blank"
                continue
            done = True
        registercmd = ProtocolCommand( ProtocolCommand.REGISTER )
        registercmd.args.append( username )
        registercmd.args.append( password )
        self.send_command( registercmd )
    
    
    def handle_manager_response( self, inp ):
        if inp == "":
            return
        print "Received '%s'" % str(inp)
        resp = parse_command( inp )
        if resp is None:
            return
        if resp.command == ProtocolCommand.ERROR:
            print "Received Error: "
            print "   Command: %s" % str(resp.error_command)
            print "   Code:    %d" % resp.error_code
            print "   Message: %s" % resp.error_msg
        elif resp.command == ProtocolCommand.RLOGIN:
            success = resp.args[ 0 ].lower() == "true"
            hash_or_reason = resp.args[ 1 ]
            if not success:  # Login failed
                print "Login failed: %s" % hash_or_reason
                # TODO ask to update login credentials
                username = self.props[ "manager.username" ] if "manager.username" in self.props.keys() else None
                password = self.props[ "manager.password" ] if "manager.password" in self.props.keys() else None
                print "Properties username/password: %s/%s" % (username, password)
                if username is not None and password is not None:
                    # Register
                    registercmd = ProtocolCommand( ProtocolCommand.REGISTER )
                    registercmd.args.append( username )
                    registercmd.args.append( password )
                    print "Sending registration command: %s" % registercmd.pack()
                    self.send_command( registercmd )
                else:
                    print "Username and/or password are not set in properties file (%s).  Set manager.username and manager.password to register." % self.PROPERTIES_FILE
                    self._stop = True
                return
            self.hash = hash_or_reason
            print "Login successful"
            self.on_login_successful()
        elif resp.command == ProtocolCommand.RREGISTER:
            success = resp.args[ 0 ]
            if not success:
                print resp.args[ 1 ]
                self.register()
                return
            print "Registration success"
            self.props[ "manager.username" ] = resp.args[ 2 ]
            self.props[ "manager.password" ] = resp.args[ 3 ]
            save_properties_file( self.PROPERTIES_FILE, self.props )
            self.login()
        elif resp.command == ProtocolCommand.RGETGAMES:
            self.games = []
            for arg in resp.args:
                game = Game()
                game.from_str( arg )
            	self.games.append( game )
            self.display_mainmenu()
        elif resp.command == ProtocolCommand.RNEWGAME:
            success = resp.args[ 0 ]
            game_id_or_reason = resp.args[ 1 ]
            if not success:
                print resp.args[ 1 ]
                return
            # New Game created, ask player if he wants to start playing it
            print "New Game Created."
            self.get_game_list()
        else:
            print "WARNING: Received unsupported message from manager: %s" % inp
        if self.waiting_for_response:
            self.resp_cond.release()
            self.waiting_for_response = False
            
            
    def get_game_list( self, wait=False ):
        self.debug( "Getting game list" )
    	getGameList = ProtocolCommand( ProtocolCommand.GETGAMES )
        getGameList.hash = self.hash
        self.games = None
        if wait:
            self.waiting_for_response = True
        self.send_command( getGameList )
        if wait:
            self.resp_cond.acquire()
        
        
    def game_list_updated( self ):
    	pass
    
    
    def create_new_dungeon( self ):
        newDungeon = ProtocolCommand( ProtocolCommand.NEWGAME )
        newDungeon.hash = self.hash
        existing_names = [ game.name.lower() for game in self.games ]
        newDungeon = self.view.populate_new_game_fields( newDungeon, existing_names )
        self.send_command( newDungeon )
    
    
    def join_dungeon( self ):
        pass
        
    
    def play_dungeon( self, game ):
        pass
    
            
    def send_command( self, cmd ):
        cmdstr = cmd.pack()
        print "Sending '%s'" % cmdstr
        self.sock.send( cmdstr )
        
        
    def handler( self, signum, frame ):
        print 'Caught signal', signum
        self.recvthread._stop = True
        self.recvthread.terminate()
    
if __name__ == "__main__":
    client = AgileDungeonClient()
    signal.signal( signal.SIGINT, client.handler )
    client.run()
    
