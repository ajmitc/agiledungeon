from view import View
from client.menu.menu import *

class BasicTerminalView( View ):
    def __init__( self ):
        View.__init__( self )
        
        
    def display_menu( self, menu ):
        if menu.title is not None:
            print menu.title
        index = 0
        items = []
        for item in menu.menuitems:
            if isinstance( item, MenuItem ):
                if item.options is not None:
                    if type(item.options) is list and len(item.options) > 0:
                        print item.options[ 0 ], ")", item.display
                    else:
                        print item.options, ")", item.display
                else:
                    print (index + 1), ")", item.display
                    item.options = [ str(index) ]
                    index += 1
                items.append( item )
            elif isinstance( item, MenuHeading ):
                print "== %s ==" % item.display
            elif isinstance( item, MenuItemSeparator ):
                print item.display
        inp = raw_input( menu.prompt ).strip()
        selected_item = None
        for item in menu.menuitems:
            if isinstance( item, MenuItem ) and item.options is not None:
                if type(item.options) is list and inp in item.options:
                    selected_item = item
                    break
                elif item.options == inp:
                    selected_item = item
                    break
        if selected_item is not None:
            print "Selected item: %s" % (str(selected_item))
            return (True, inp, selected_item)
        return (False, inp, "Invalid selection")
        
    def populate_new_game_fields( self, command, existing_names ):
        done = False
        while not done:
            name = raw_input( "Name: " ).strip()
            if name == "":
                print "Name cannot be blank"
                continue
            if name.lower() in existing_names:
                print "Name already taken"
                continue
            command.args.append( name )
            done = True
        # Visibility
        done = False
        while not done:
            vis = raw_input( "Visibility [public|private]: " ).strip()
            if vis == "":
                vis = "public"
            if vis.lower() in [ "pu", "pub", "public" ]:
                vis = "public"
            elif vis.lower() in [ "pr", "priv", "private" ]:
                vis = "private"
            else:
                print "Unrecognized visibility.  Please enter public or private."
                continue
            command.args.append( vis )
            done = True
        # Invite players
        done = False
        while not done:
            player = raw_input( "Invite player (Leave blank to skip): " ).strip()
            if player != "":
                # TODO Find user and send notification
                pass
            else:
                done = True
        return command
    
