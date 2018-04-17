import random
import xml.etree.ElementTree as ET
from room import Room

class Dungeon( object ):
    MIN_ROOMS = 10
    MAX_ROOMS = 40

    ENTRANCE = "Entranece"


    def __init__( self ):
        self.rooms = []  # The first room is always the Entrance to the dungeon
        self.depth = 1
        self.current_room = None
        self.entrance = None
        
        
    def build( self, roomfactory, monsterfactory, itemfactory ):
        print "Building Dungeon"
        min_rooms = self.MIN_ROOMS
        max_rooms = self.MAX_ROOMS
        num_rooms = random.randint( min_rooms, max_rooms )
        # filter rooms appropriate for the current dungeon level
        rooms = roomfactory.get_rooms_for_level( self.depth )
        self.entrance = Room( self.ENTRANCE, "There is a staircase leading up." )
        self.entrance.stairs = Room.UP
        self.entrance.x = 0
        self.entrance.y = 0
        self.rooms.append( self.entrance )
        self.current_room = self.entrance
        self.__visit_room( self.entrance, 1, num_rooms, rooms, monsterfactory, itemfactory )
        print "Dungeon Built"

            
            
    def __visit_room( self, room, room_count, max_rooms, rooms, monsterfactory, itemfactory, visited=[] ):
        if room is None or room in visited or room_count >= max_rooms:
            return
        visited.append( room )
        for door in [ Room.NORTH, Room.SOUTH, Room.EAST, Room.WEST ]:
            if room.doors[ door ] is None:
                # There is a 80% chance we will add another room off this one if we've exceeded our MIN_ROOMS
                x = room.x if door in [ Room.NORTH, Room.SOUTH ] else (room.x - 1 if door == Room.WEST else room.x + 1)
                y = room.y if door in [ Room.WEST, Room.EAST ] else (room.y - 1 if door == Room.NORTH else room.y + 1)
                room_desc = random.choice( rooms )
                if room_count < self.MIN_ROOMS or random.random() <= 0.8:
                    new_room = self.__build_room( x, y, room_desc, monsterfactory, itemfactory )
                    room.doors[ door ] = new_room
                    self.rooms.append( new_room )
                    room_count += 1
                    if room_count == max_rooms:
                        # This is the last room, add a staircase down
                        new_room.stairs = Room.DOWN
            if room_count >= max_rooms:
                break
        for door in [ Room.NORTH, Room.SOUTH, Room.EAST, Room.WEST ]:
            self.__visit_room( room.doors[ door ], room_count, max_rooms, rooms, monsterfactory, itemfactory, visited )
        
        
    def __build_room( self, x, y, room_desc, monsterfactory, itemfactory ):
        room = room_desc.clone()
        room.x = x
        room.y = y
        # randomly choose monsters
        num_monsters = random.randint( 1, 4 )
        for i in xrange( num_monsters ):
            monster = monsterfactory.get_random( self.depth )
            room.monsters.append( monster )
        return room


    def find_room_by_id( self, id ):
        id = str(id)
        for room in self.rooms:
            if room.id == id:
                return room
        return None


    def find_room_by_name( self, name ):
        for room in self.rooms:
            if room.name == name:
                return room
        return None


    def to_xml( self ):
        elDungeon = ET.Element( "dungeon" )
        elDungeon.set( "depth", str(self.depth) )
        elDungeon.set( "currentroom", str(self.current_room.id) if self.current_room is not None else "" )
        elDungeon.set( "entrance", str(self.entrance.id) if self.entrance is not None else "" )
        elRooms = ET.SubElement( elDungeon, "rooms" )
        for room in self.rooms:
            elRoom = room.to_xml()
            elRooms.append( elRoom )
        return elDungeon


    def from_xml( self, xml ):
        if xml.tag != "dungeon":
            return False
        self.depth = int(xml.get( "depth" ))
        elRooms = xml.find( "rooms" )
        for elRoom in elRooms:
            room = Room()
            room.from_xml( elRoom )
            self.rooms.append( room )
        entranceid = xml.get( "entrance" ) if xml.get( "entrance" ) != "" else None
        currentroomid = xml.get( "currentroom" ) if xml.get( "currentroom" ) else None
        self.entrance = self.find_room_by_id( entranceid ) if entranceid is not None else None
        self.current_room = self.find_room_by_id( currentroomid ) if currentroomid is not None else None
        if self.entrance is None:
            self.entrance = self.find_room_by_name( self.ENTRANCE )
        if self.current_room is None:
            self.current_room = self.entrance
        return True


    def __str__( self ):
        pass
