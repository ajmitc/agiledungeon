from hero import Hero
from item.item import Item

class Dwarf( Hero ):
	def __init__( self ):
    	Hero.__init__( self, Hero.DWARF, 6 )
        
        
    def reset( self, itemfactory ):
        Hero.reset( self, all_items )
        self.equipment[ Hero.PRIMARY_HAND ] = itemfactory.get( Item.SHORT_SWORD )