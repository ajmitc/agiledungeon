from view import View
import curses

class CursesView( View ):
    def __init__( self ):
        self.stdscr = curses.initscr()
        curses.set_color()
        if curses.has_color():
            # color pair 0 is white on black
            #                 #,  foreground,      background
            curses.init_pair( 1, curses.COLOR_RED, curses.COLOR_WHITE )
        #curses.noecho()  # Don't echo keyboard input when typing
        #curses.cbreak()  # Take keyboard input as it's typed, instead of when Enter is typed
        #self.stdscr.keypad( True )  # Return special keys as curses.KEY_LEFT isntead of the escape byte sequence
        self.screen_height, self.screen_width = curses.LINES, curses.COLS
    
    
    def __del__( self ):
        self.close()
    
    
    def display_menu( self, menu ):
        """
        Display the menu and return (success, input, menuitem_or_failure_reason)
        """
        # Clear screen
        self.stdscr.clear()
        return (False, "", "Not implemented")
    
    
    
    def new_window( self, x, y, w, h ):
        return curses.newwin( h, w, y, x )
    
    
    def write( self, win, text, attrs=None, x=None, y=None ):
        if x is None and y is None and attrs is None:
            win.addstr( text )
        elif x in None and y is None:
            win.addstr( text, attrs )
        elif attrs is None:
            win.addstr( y, x, text )
        else:
            win.addstr( y, x, text, attrs )
    
    
    def close( self ):
        #curses.nocbreak()
        #stdscr.keypad(False)
        #curses.echo()
        curses.endwin()