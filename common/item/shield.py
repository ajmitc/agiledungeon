from item import Item

# Shields protect the Hero from wrong guesses.  The level of the Shield determines the number
# of wrong guesses.  Once the number of wrong guesses is reached, the shield is broken and
# can not longer be used.

class SmallWoodenShield( Item ):
    def __init__( self ):
        Item.__init__( self, "Small Wooden Shield" )
        self.level = 1