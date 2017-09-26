

class MenuItem:
    def __init__( self, display, callback ):
        self.display = display
        self.callback = callback



class Menu:
    def __init__( self, title=None, prompt="> " ):
        self.title = title
        self.prompt = prompt
        self.menuitems = []

