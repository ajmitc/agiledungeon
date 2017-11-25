from menu import *

class MainMenu( Menu ):
    def __init__( self, client ):
        Menu.__init__( self, "Agile Dungeon" )
        self.client = client
        # Add menu options for existing dungeons
        if len(self.client.games) > 0:
            self.menuitems.append( MenuHeading( "Active Games" ) )
        for game in self.client.games:
            self.menuitems.append( MenuItem( "Play %s" % game.name, self.play_dungeon ))
        self.menuitems.append( MenuHeading( "Create/Join Game" ) )
        self.menuitems.append( MenuItem( "Join Dungeon", self.join_dungeon ) )
        self.menuitems.append( MenuItem( "Start New Dungeon", self.start_dungeon ) )
        self.menuitems.append( MenuItem( "" ) )
        self.menuitems.append( MenuItem( "My Settings", self.open_settings ) )
        self.menuitems.append( MenuItem( "Exit", self.exit ) )
        
    
    def join_dungeon( self, inp ):
        self.client.join_dungeon()
    
    
    def start_dungeon( self, inp ):
        self.client.start_new_dungeon()
    
    
    def open_settings( self, inp ):
        menu = SettingsMenu( self )
        while not menu.exit_menu:
            success, inp, selection_or_reason = self.client.view.display_menu( menu )
            if not success:
                print selection_or_reason
                continue
            selection_or_reason.callback( inp )
    
    
    def play_dungeon( self, inp ):
        # Since the active games appear first, we can use the index to select which game was selected
        try:
            inp = int(inp)
        except Exception, e:
            print "Invalid selection"
            return
        game = self.games[ inp ]
        # Start game
        self.client.play_dungeon( game )