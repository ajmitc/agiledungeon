
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
        
    
    def reset( self, all_items ):
		self.hitpoints = self.max_hitpoints
        self.inventory = []
        
        
        
    def __str__( self ):
    	inv = ",".join( [ str(i) for i in self.inventory ] )
        equip = ",".join( [ str(e) for e in self.equipment ] )
    	return "%s,%s,%d,%d,[%s],[%s]" % (self.type, self.name, self.max_hitpoints, self.hitpoints, inv, equip)
        
