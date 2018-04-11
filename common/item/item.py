import xml.etree.ElementTree as ET

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


    def to_xml( self ):
        elItem = ET.Element( "item" )
        elItem.set( "name", self.name )
        elItem.set( "level", str(self.level) )
        elItem.set( "locations", ",".join( self.equip_location ) )
        elItem.set( "carryBy", ",".join( self.carriable_by ) )
        return elItem


    def from_xml( self, xml ):
        if xml.tag != "item":
            return False
        self.name = xml.get( "name" )
        self.level = int(xml.get( "level" ))
        self.equip_location = xml.get( "locations" ).split( "," )
        self.carriable_by = xml.get( "carryBy" ).split( "," )
        return True

        
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
    
