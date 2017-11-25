

class MenuItem:
    def __init__( self, display, callback ):
        self.display = display
        self.callback = callback


class MenuHeading:
    def __init__( self, display ):
        self.display = display
        

class Menu:
    def __init__( self, title=None, prompt="> " ):
        self.title = title
        self.prompt = prompt
        self.menuitems = []
        self.exit_menu = False
        
        
    def exit( self, inp ):
        self.exit_menu = True

