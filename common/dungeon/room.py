import xml.etree.ElementTree as ET

class Room( object ):
    # Doors
    NORTH = "NORTH"
    SOUTH = "SOUTH"
    WEST = "WEST"
    EAST = "EAST"
    
    # Stairs
    UP = "Up"
    DOWN = "Down"

    def __init__( self, name="", desc="", id="" ):
        self.id = id
        self.name = name
        self.description = desc
        self.monsters = []
        self.doors = {
            self.NORTH: None,
            self.SOUTH: None,
            self.WEST: None,
            self.EAST: None
        }
        self.stairs = None
        self.min_level = 1
        self.max_level = 10
        self.min_monsters = 0
        self.max_monsters = 5
        
    def clone( self ):
        other = Room( self.name, self.description )
        [ other.monsters.append( m ) for m in self.monsters ]
        for key in self.doors.keys():
            other.doors[ key ] = self.doors[ key ]
        other.stairs = self.stairs
        other.min_level = self.min_level
        other.max_level = self.max_level
        other.min_monsters = self.min_monsters
        other.max_monsters = self.max_monsters
        return other


    def to_xml( self ):
        elRoom = ET.Element( "room" )
        elRoom.set( 'id', self.id )
        elRoom.set( 'name', self.name )
        elRoom.set( 'desc', self.description )
        elRoom.set( "minLevel", str(self.min_level) )
        elRoom.set( "maxLevel", str(self.max_level) )
        elRoom.set( "minMonsters", str(self.min_monsters) )
        elRoom.set( "maxMonsters", str(self.max_monsters) )
        elMonsters = ET.SubElement( elRoom, "monsters" )
        for monster in self.monsters:
            elMonsters.append( monster.to_xml() )
        elDoors = ET.SubElement( elRoom, "doors" )
        for dir, room in self.doors.iteritems():
            elDoor = ET.SubElement( elDoors, "door" )
            elDoor.set( "direction", dir )
            elDoor.text = room.id
        # TODO Stairs
        return elRoom


    def from_xml( self, xml ):
        if xml.tag != "room":
            return False
        self.id = xml.get( 'id' )
        self.name = xml.get( "name" )
        self.description = xml.get( "desc" )
        self.min_level = int(xml.get( "minLevel" ))
        self.max_level = int(xml.get( "maxLevel" ))
        self.min_monsters = int(xml.get( "minMonsters" ))
        self.max_monsters = int(xml.get( "maxMonsters" ))
        elMonsters = xml.find( "monsters" )
        for elMonster in elMonsters:
            monster = Monster()
            monster.from_xml( elMonster )
            self.monsters.append( monster )
        for elDoor in xml.find( 'doors' ):
            dir = elDoor.get( "direction" )
            self.doors[ dir ] = elDoor.text
        # TODO Stairs
        return True

        
class RoomFactory:
    def __init__( self, rooms ):
        self.rooms = rooms
        
        
    def get( self, name ):
        for room in self.rooms:
            if room.name.lower() == name.lower():
                return room.clone()
        return None
    
    
    def get_rooms_for_level( self, dungeon_level ):
        rooms = []
        for room in self.rooms:
            if room.max_level >= dungeon_level >= room.min_level:
                rooms.append( room.clone() )
        return rooms
        #return [ room.clone() for room in self.rooms if room.max_level >= dungeon_level >= room.min_level ]

