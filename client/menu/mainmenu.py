from menu import *

class MainMenu( Menu ):
    def __init__( self, client ):
        Menu.__init__( self, "*****************\n* Agile Dungeon *\n*****************" )
        self.client = client
        # Add menu options for existing dungeons
        self.menuitems.append( MenuHeading( "Active Games" ) )
        if len(self.client.games) == 0:
            self.menuitems.append( MenuItemSeparator( "   None" ) )
        for game in self.client.games:
            self.menuitems.append( MenuItem( "Play %s" % game.name, self.play_dungeon ))
        self.menuitems.append( MenuItemSeparator() )
        self.menuitems.append( MenuHeading( "Create/Join Game" ) )
        self.menuitems.append( MenuItem( "Join Dungeon", self.join_dungeon, [ 'j', 'join' ] ) )
        self.menuitems.append( MenuItem( "Create New Dungeon", self.create_dungeon, [ 'n', 'new', 'create' ] ) )
        self.menuitems.append( MenuItemSeparator() )
        self.menuitems.append( MenuHeading( "Other" ) )
        self.menuitems.append( MenuItem( "My Settings", self.open_settings, [ 's', 'settings' ] ) )
        self.menuitems.append( MenuItem( "Exit", self.exit, [ 'q', 'quit' ] ) )
        
    
    def join_dungeon( self, inp ):
        self.client.join_dungeon()
    
    
    def create_dungeon( self, inp ):
        self.client.create_new_dungeon()
    
    
    def open_settings( self, inp ):
        menu = SettingsMenu( self )
        while not menu.exit_menu:
            success, inp, selection_or_reason = self.client.view.display_menu( menu )
            if not success:
                print selection_or_reason
                continue
            if selection_or_reason.callback is not None:
                selection_or_reason.callback( inp )
    
    
    def play_dungeon( self, inp ):
        # Since the active games appear first, we can use the index to select which game was selected
        try:
            inp = int(inp) - 1
        except Exception, e:
            print "Invalid selection"
            return
        game = self.client.games[ inp ]
        # Start game
        self.client.play_dungeon( game )
