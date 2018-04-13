import socket
import traceback
import threading
import time
from menu.mainmenu import MainMenu
from menu.menu import Menu, MenuItem
from view.basicterminalview import BasicTerminalView
from common.game import Game
from common.protocol.proto_command import ProtocolCommand
from common.util import *
from common.xml_util import parse_xml
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
        self.username = None
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
        logincmd.args[ 'username' ] = username
        logincmd.args[ 'password' ] = password
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
        registercmd.args[ 'username' ] = username
        registercmd.args[ 'password' ] = password
        self.send_command( registercmd )
    
    
    def handle_manager_response( self, inp ):
        if inp == "":
            return
        print "Received '%s'" % str(inp)
        #resp = parse_command( inp )
        resp = ProtocolCommand()
        resp.unpack( parse_xml( xmlstring=inp ) )
        #if resp is None:
            #return
        if resp.command == ProtocolCommand.ERROR:
            print "Received Error: "
            print "   Command: %s" % str(resp.error_command)
            print "   Code:    %d" % resp.error_code
            print "   Message: %s" % resp.error_msg
        elif resp.command == ProtocolCommand.RLOGIN:
            success = resp.args[ 'success' ]
            if not success:  # Login failed
                print "Login failed: %s" % resp.args[ 'reason' ]
                # TODO ask to update login credentials
                username = self.props[ "manager.username" ] if "manager.username" in self.props.keys() else None
                password = self.props[ "manager.password" ] if "manager.password" in self.props.keys() else None
                print "Properties username/password: %s/%s" % (username, password)
                if username is not None and password is not None:
                    # Register
                    registercmd = ProtocolCommand( ProtocolCommand.REGISTER )
                    registercmd.args[ 'username' ] = username
                    registercmd.args[ 'password' ] = password
                    print "Sending registration command: %s" % registercmd.pack()
                    self.send_command( registercmd )
                else:
                    print "Username and/or password are not set in properties file (%s).  Set manager.username and manager.password to register." % self.PROPERTIES_FILE
                    self._stop = True
                return
            self.hash = resp.args[ 'hash' ]
            self.username = resp.args[ 'username' ]
            print "Login successful"
            self.on_login_successful()
        elif resp.command == ProtocolCommand.RREGISTER:
            success = resp.args[ 'success' ]
            if not success:
                print resp.args[ 'reason' ]
                self.register()
                return
            print "Registration success"
            self.props[ "manager.username" ] = resp.args[ 'username' ]
            self.props[ "manager.password" ] = resp.args[ 'password' ]
            save_properties_file( self.PROPERTIES_FILE, self.props )
            self.login()
        elif resp.command == ProtocolCommand.RGETGAMES:
            self.games = []
            for name, xml in resp.args.iteritems():
                # There is a wrapper element that only contains the game name, parse the child
                for elGame in xml:
                    game = Game()
                    game.from_xml( elGame )
                    self.games.append( game )
            self.display_mainmenu()
        elif resp.command == ProtocolCommand.RNEWGAME:
            success = resp.args[ 'success' ]
            if not success:
                print resp.args[ 'reason' ]
                return
            # New Game created, ask player if he wants to start playing it
            print "New Game Created."
            self.get_game_list()
        elif resp.command == ProtocolCommand.RCONTROL:
            success = resp.args[ 'success' ]
            if not success:
                print resp.args[ 'reason' ]
                return
            # Player successfully took control of hero
            print "You are now controlling the %s." % resp.args[ 'type' ]
            self.get_game_update()
        elif resp.command == ProtocolCommand.RGAMEUPDATE:
            success = resp.args[ 'success' ]
            if not success:
                print resp.args[ 'reason' ]
                return
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
        print "Joining a dungeon is not yet implemented"
        self.view.pause()

    
    def play_dungeon( self, game ):
        self.current_game = game
        print "Playing %s" % game.name
        print "Entering Dungeon Floor %d" % game.dungeon.depth
        print "Room: %s" % game.dungeon.current_room.name
        print game.dungeon.current_room.description
        # Print Heroes and players controlling them
        self.view.display_hero_summary( game.heroes )
        # Choose hero to control, if none available, set as observer
        success = False
        while not success:
            uncontrolled = [ hero for hero in game.heroes if hero.player is None ]
            if len(uncontrolled) == 0:
                print "All Heroes are being controlled, you are now an Observer"
                success = True
                continue
            menu = Menu( "Select Available Hero" )
            for hero in uncontrolled:
                menu.menuitems.append( MenuItem( hero.type ) )
            success, inp, menuitem = self.view.display_menu( menu )
            if success:
                hero = game.heroes[ menuitem.display ]
                msg = ProtocolCommand( ProtocolCommand.CONTROL )
                msg.args[ 'hero' ] = hero.type
                msg.args[ 'game' ] = self.current_game.id
                msg.hash = self.hash
                self.send_command( msg )


    def get_game_update( self ):
        cmd = ProtocolCommand( ProtocolCommand.GAMEUPDATE )
        cmd.args[ 'game' ] = self.current_game.id
        cmd.hash = self.hash
        self.send_command( cmd )


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
    
