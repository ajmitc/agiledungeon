
class Room:
    # Doors
    NORTH = "NORTH"
    SOUTH = "SOUTH"
    WEST = "WEST"
    EAST = "EAST"
    
    # Stairs
    UP = "Up"
    DOWN = "Down"
    
	def ___init__( self, name, desc="" ):
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
        
        
class RoomFactory:
    def __init__( self, rooms ):
        self.rooms = rooms
        
        
    def get( self, name ):
        for room in self.rooms:
            if room.name.lower() == name.lower():
                return room.clone()
        return None
    
    
    def get_rooms_for_level( self, dungeon_level ):
        return [ room.clone() for room in self.rooms if room.max_level >= dungeon_level >= room.min_level ]
    