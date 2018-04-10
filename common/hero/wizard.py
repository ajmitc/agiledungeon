from hero import Hero
from common.item.item import Item

class Wizard( Hero ):
    def __init__( self ):
        Hero.__init__( self, Hero.WIZARD, 3 )
        
        
    def reset( self, itemfactory ):
        Hero.reset( self, itemfactory )
        self.equipment[ Hero.PRIMARY_HAND ] = itemfactory.get( Item.STAFF )
