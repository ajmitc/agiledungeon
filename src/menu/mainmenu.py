from menu import *

class MainMenu( Menu ):
    def __init__( self ):
        Menu.__init__( self, user )
        # TODO Add menu options for existing dungeons
        self.menuitems.append( MenuItem( "Join Dungeon", self.join_dungeon ) )
        self.menuitems.append( MenuItem( "Start New Dungeon", self.start_dungeon ) )
        
    def join_dungeon( self, inp ):
        pass
    
    
    def start_dungeon( self, inp ):
        pass
    