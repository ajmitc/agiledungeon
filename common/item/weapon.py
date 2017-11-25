from item import Item
from hero import Hero

# Weapons allow users to get hints.  The Item level determines the number
# of hints the user may receive per monster.

class Fists( Item ):
    def __init__( self ):
        Item.__init__( self, Item.FISTS )
        self.equip_location.append( Hero.PRIMARY_HAND )

        
class ShortSword( Item ):
	def __init__( self ):
    	Item.__init__( self, Item.SHORT_SWORD )
        self.equip_location.append( Hero.PRIMARY_HAND )
        self.level = 1
        