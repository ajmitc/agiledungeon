from menu import *

class SettingsMenu( Menu ):
    def __init__( self, user ):
        Menu.__init__( self, "Settings" )
        self.menuitems.append( MenuItem( "Notification Settings", self.open_notification_settings ) )
        self.menuitems.append( MenuItem( "Done", self.exit ) )
        
        
    def open_notification_settings( self, inp ):
        pass
    