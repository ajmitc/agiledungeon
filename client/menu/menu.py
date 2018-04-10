

class MenuItem:
    def __init__( self, display, callback=None, options=None ):
        self.display  = display
        self.callback = callback
        self.options  = options

    def __str__( self ):
        return self.display


class MenuItemSeparator:
    def __init__( self, display="" ):
        self.display = display

    def __str__( self ):
        return "[SEPARATOR: %s]" % self.display


class MenuHeading:
    def __init__( self, display ):
        self.display = display

    def __str__( self ):
        return "[HEADING: %s]" % self.display
        

class Menu:
    def __init__( self, title=None, prompt="> " ):
        self.title = title
        self.prompt = prompt
        self.menuitems = []
        self.exit_menu = False
        
        
    def exit( self, inp ):
        self.exit_menu = True

