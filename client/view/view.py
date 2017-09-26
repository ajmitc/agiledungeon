from basicterminalview import BasicTerminalView

class View:
    """
    Baseclass for supported views
    """
    def __init__( self ):
        pass
    
    def display_menu( self, menu ):
        """
        Display the menu and return (success, input, menuitem_or_failure_reason)
        """
        return (False, "", "Not implemented")
        