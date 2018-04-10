from common.item.item import Item


class Hero:
    BARBARIAN = "Barbarian"
    ELF = "Elf"
    DWARF = "Dwarf"
    WIZARD = "Wizard"
    
    PRIMARY_HAND = "Primary Hand"
    SECONDARY_HAND = "Secondary Hand"
    BODY = "Body"
    LEGS = "Legs"
    HEAD = "Head"
    RING1 = "Ring 1"
    RING2 = "Ring 2"
    
    def __init__( self, type, hp ):
        self.type = type
        self.name = type
        self.max_hitpoints = hp
        self.hitpoints = hp
        self.inventory = []
        self.equipment = {
            self.PRIMARY_HAND: None,
            self.SECONDARY_HAND: None,
            self.BODY: None,
            self.LEGS: None,
            self.HEAD: None,
            self.RING1: None,
            self.RING2: None,
        }
        
    
    def reset( self, itemfactory ):
        self.hitpoints = self.max_hitpoints
        self.inventory = []
        

    def from_str( self, s ):
        self.type, self.name, self.max_hitpoints, self.hitpoints, rest = s.split( ",", 4 )
        self.max_hitpoints = int(self.max_hitpoints)
        self.hitpoints = int(self.hitpoints)
        inv, equip = rest.split( "],[" )
        inv = inv.strip( "[" ).strip()
        equip = equip.strip( "]" ).strip()
        for i in inv.split( "," ):
            item = Item()
            item.from_str( i )
            self.inventory.append( item )
        for eq in equip.split( "," ):
            w, e = eq.split( ":" )
            item = Item()
            item.from_str( e )
            self.equipment[ w ] = item


    def __str__( self ):
        inv = ",".join( [ str(i) for i in self.inventory ] )
        equip = ",".join( [ "%s:%s" % (w, str(e)) for w, e in self.equipment.iteritems() ] )
        return "%s,%s,%d,%d,[%s],[%s]" % (self.type, self.name, self.max_hitpoints, self.hitpoints, inv, equip)
        
