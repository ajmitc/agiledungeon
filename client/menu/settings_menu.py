from menu import *

class SettingsMenu( Menu ):
    def __init__( self, user ):
        Menu.__init__( self, "Settings" )
        self.menuitems.append( MenuItem( "Notification Settings", self.open_notification_settings ) )
        
        
    def open_notification_settings( self, inp ):
        pass
    