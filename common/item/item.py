
class Item:
    # Carriable by any Hero
    ANY = "Any"
    
    # Item names
    FISTS = "Fists"
    SHORT_SWORD = "Short Sword"
    STAFF = "Staff"
    
    def __init__( self, name="Item" ):
        self.name = name
        self.level = 0
        self.equip_location = []  # List of locations this Item could be carried.  Values are OR'd.
        self.carriable_by = []
    
    
    def clone( self ):
        other = Item( self.name )
        other.level = self.level
        [ other.equip_location.append( l ) for l in self.equip_location ]
        [ other.carriable_by.append( h ) for h in self.carriable_by ]
        return other
        
        
    def __str__( self ):
        return "%s,%d,%s" % (self.name, self.level, self.equip_location)
        

class ItemFactory:
    def __init__( self, all_items ):
        self.items = all_items
    
    
    def get( self, name ):
        for item in self.items:
            if item.name.lower() == name.lower():
                return item.clone()
        return None
    
