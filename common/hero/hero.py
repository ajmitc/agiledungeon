from common.item.item import Item
import xml.etree.ElementTree as ET

class Hero:
    BARBARIAN = "Barbarian"
    ELF = "Elf"
    DWARF = "Dwarf"
    WIZARD = "Wizard"

    # Ordered list so loops will stay consistent
    HERO_TYPES = [
        BARBARIAN,
        DWARF,
        ELF,
        WIZARD
    ]
    
    PRIMARY_HAND = "Primary Hand"
    SECONDARY_HAND = "Secondary Hand"
    BODY = "Body"
    LEGS = "Legs"
    HEAD = "Head"
    RING1 = "Ring 1"
    RING2 = "Ring 2"
    
    def __init__( self, type="", hp=0 ):
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
        self.player = None  # (username)
        
    
    def reset( self, itemfactory ):
        self.hitpoints = self.max_hitpoints
        self.inventory = []


    def to_xml( self ):
        elHero = ET.Element( "hero" )
        elHero.set( "type", self.type )
        elHero.set( "name", self.name )
        elHero.set( "maxHitpoints", str(self.max_hitpoints) )
        elHero.set( "hitpoints", str(self.hitpoints) )
        elHero.set( "player", self.player if self.player is not None else "" )
        elInventory = ET.SubElement( elHero, "inventory" )
        for item in self.inventory:
            elInventory.append( item.to_xml() )
        elEquipment = ET.SubElement( elHero, "equipment" )
        for where, item in self.equipment.iteritems():
            if item is not None:
                elWhere = ET.SubElement( elEquipment, where.replace( " ", "_" ) )
                elWhere.append( item.to_xml() )
        return elHero


    def from_xml( self, xml ):
        if xml.tag != "hero":
            return False
        self.type = xml.get( "type" )
        self.name = xml.get( "name" )
        self.max_hitpoints = int(xml.get( "maxHitpoints" ))
        self.hitpoints = int(xml.get( "hitpoints" ))
        self.player = xml.get( "player" ) if xml.get( "player" ) != "" else None
        elInventory = xml.find( "inventory" )
        for elItem in elInventory:
            item = Item()
            item.from_xml( elItem )
            self.inventory.append( item )
        elEquipment = xml.find( "equipment" )
        for elWhere in elEquipment:
            where = elWhere.tag.replace( "_", " " )
            for elItem in elWhere:
                item = Item()
                item.from_xml( elItem )
            self.equipment[ where ] = item
        return True


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
        
