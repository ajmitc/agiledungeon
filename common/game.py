from uuid import uuid4
from dungeon.dungeon import Dungeon
from hero.barbarian import Barbarian
from hero.elf import Elf
from hero.dwarf import Dwarf
from hero.wizard import Wizard
from hero.hero import Hero

class Game:
    VISIBILITY_PUBLIC = "public"
    VISIBILITY_PRIVATE = "private"
    
    ROOMS_FILENAME = "data/rooms.xml"
    MONSTERS_FILENAME = "data/monsters.xml"
    ITEMS_FILENAME = "data/items.xml"
    
    def __init__( self ):
    	self.id = str(uuid4())
        self.dungeon = Dungeon()
        self.heros = {
            Hero.BARBARIAN: Barbarian(),
            Hero.DWARF: Dwarf().
            Hero.ELF: Elf(),
            Hero.WIZARD: Wizard()
        }
        self.visibility = self.VISIBILITY_PUBLIC
        self.name = "Game"
        
        
        
    def new_game( self ):
    	self.dungeon.depth = 1
        roomfactory = xml_util.load_rooms( self.ROOMS_FILENAME )
        monsterfactory = xml_util.load_monsters( self.MONSTERS_FILENAME )
        itemfactory = xml_util.load_items( self.ITEMS_FILENAME )
        self.dungeon.build( roomfactory, monsterfactory, itemfactory )
        for hero in self.heros:
        	hero.reset( items )
    
    
    def __str__( self ):
    	fields = [
        	self.id,
            str(self.dungeon),
            str(self.heros[ Hero.BARBARIAN ]),
            str(self.heros[ Hero.DWARF ]),
            str(self.heros[ Hero.ELF ]),
            str(self.heros[ Hero.WIZARD ])
        ]
        return ";".join( fields )