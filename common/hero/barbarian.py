from hero import Hero
from common.item.item import Item
from common.item.weapon import ShortSword

class Barbarian( Hero ):
    def __init__( self ):
        Hero.__init__( self, Hero.BARBARIAN, 8 )
        self.equipment[ Hero.PRIMARY_HAND ] = ShortSword()
        
        
    def reset( self, itemfactory ):
        Hero.reset( self, itemfactory )
        self.equipment[ Hero.PRIMARY_HAND ] = itemfactory.get( Item.SHORT_SWORD )
        
