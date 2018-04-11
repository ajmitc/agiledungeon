from uuid import uuid4
from dungeon.dungeon import Dungeon
from hero.barbarian import Barbarian
from hero.elf import Elf
from hero.dwarf import Dwarf
from hero.wizard import Wizard
from hero.hero import Hero
import xml_util
import xml.etree.ElementTree as ET

class Game( object ):
    VISIBILITY_PUBLIC = "public"
    VISIBILITY_PRIVATE = "private"
    
    ROOMS_FILENAME = "data/rooms.xml"
    MONSTERS_FILENAME = "data/monsters.xml"
    ITEMS_FILENAME = "data/items.xml"
    
    def __init__( self ):
    	self.id = str(uuid4())
        self.dungeon = Dungeon()
        self.heroes = {
            Hero.BARBARIAN: Barbarian(),
            Hero.DWARF: Dwarf(),
            Hero.ELF: Elf(),
            Hero.WIZARD: Wizard()
        }
        self.visibility = self.VISIBILITY_PUBLIC
        self.accessible_users = []  # List of usernames that can join this game (only valid if visibility == private)
        self.name = "Game"
        
        
        
    def new_game( self ):
    	self.dungeon.depth = 1
        roomfactory = xml_util.load_rooms( self.ROOMS_FILENAME )
        monsterfactory = xml_util.load_monsters( self.MONSTERS_FILENAME )
        itemfactory = xml_util.load_items( self.ITEMS_FILENAME )
        self.dungeon.build( roomfactory, monsterfactory, itemfactory )
        print "Resetting Heroes"
        for hero in self.heroes.values():
        	hero.reset( itemfactory )


    def to_xml( self ):
        elGame = ET.Element( "game" )
        elGame.set( "id", self.id )
        elGame.set( "visibility", self.visibility )
        elGame.set( "name", self.name )
        elGame.append( self.dungeon.to_xml() )
        elHeroes = ET.SubElement( elGame, "heroes" )
        for hero in self.heroes.values():
            elHeroes.append( hero.to_xml() )
        elPlayers = ET.SubElement( elGame, "players" )
        for user in self.accessible_users:
            elUser = ET.SubElement( elPlayers, "player" )
            elUser.text = user
        return elGame


    def from_xml( self, xml ):
        if xml.tag != "game":
            return False
        self.id = xml.get( "id" )
        self.visibility = xml.get( "visibility" )
        self.name = xml.get( "name" )
        self.dungeon.from_xml( xml.find( "dungeon" ) )
        for elHero in xml.find( "heroes" ):
            hero = Hero()
            hero.from_xml( elHero )
            self.heroes[ hero.type ] = hero
        for elPlayer in xml.find( "players" ):
            self.accessible_users.append( elPlayer.text )
        return True


    def from_str( self, s ):
        self.id, dungeon, barbarian, dwarf, elf, wizard = s.split( ";" )
        self.dungeon.from_str( dungeon )
        self.heroes[ Hero.BARBARIAN ].from_str( barbarian )
        self.heroes[ Hero.DWARF ].from_str( dwarf )
        self.heroes[ Hero.ELF ].from_str( elf )
        self.heroes[ Hero.WIZARD ].from_str( wizard )

    
    def __str__( self ):
    	fields = [
        	self.id,
            str(self.dungeon),
            str(self.heroes[ Hero.BARBARIAN ]),
            str(self.heroes[ Hero.DWARF ]),
            str(self.heroes[ Hero.ELF ]),
            str(self.heroes[ Hero.WIZARD ])
        ]
        return ";".join( fields )

