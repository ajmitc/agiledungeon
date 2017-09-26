from menu import *

class MainMenu( Menu ):
    def __init__( self, user ):
        Menu.__init__( self, "Agile Dungeon" )
        # TODO Add menu options for existing dungeons
        self.menuitems.append( MenuItem( "Join Dungeon", self.join_dungeon ) )
        self.menuitems.append( MenuItem( "Start New Dungeon", self.start_dungeon ) )
        self.menuitems.append( MenuItem( "My Settings", self.open_settings ) )
        
    def join_dungeon( self, inp ):
        pass
    
    
    def start_dungeon( self, inp ):
        pass
    
    
    def open_settings( self, inp ):
        pass
    