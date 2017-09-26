

class BasicTerminalView( View ):
    def __init__( self ):
        View.__init__( self )
        
    def display_menu( self, menu ):
        if menu.title is not None:
            print menu.title
        for index, item in enumerate(menu.menuitems):
            print (index + 1), ") ", item.display
        inp = raw_input( menu.prompt )
        try:
            inp = int(inp) - 1
            return (True, inp, menu.menuitems[ inp ])
        except:
            pass
        return (False, inp, "Invalid selection")
        
    