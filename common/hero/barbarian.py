from hero import Hero
from item.item import Item

class Barbarian( Hero ):
	def __init__( self ):
    	Hero.__init__( self, Hero.BARBARIAN, 8 )
        self.equipment[ Hero.PRIMARY_HAND ] = ShortSword()
        
        
    def reset( self, itemfactory ):
        Hero.reset( self, all_items )
		self.equipment[ Hero.PRIMARY_HAND ] = itemfactory.get( Item.SHORT_SWORD )
        