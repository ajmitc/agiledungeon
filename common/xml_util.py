import xml.etree.ElementTree as ET
from dungeon.monster import Monster, Puzzle, MonsterFactory
from dungeon.room import Room, RoomFactory
from item.item import Item, ItemFactory

def load_rooms( filename ):
    roomsxml = parse_xml( filename )
    rooms = []
    for roomxml in roomsxml.find( "room" ):
        room = Room()
        room.name = roomxml.find( "name" ).text
        room.description = roomxml.find( "description" ).text
        room.min_level = room.find( "minLevel" ).text
        room.max_level = room.find( "maxLevel" ).text
        room.min_monsters = room.find( "minMonsters" ).text
        room.max_monsters = room.find( "maxMonsters" ).text
        rooms.append( room )
    return RoomFactory( rooms )


 def load_monsters( filename ):
    monsxml = parse_xml( filename )
    monsters = []
    for monxml in monsxml.find( "monster" ):
        mon = Monster()
        mon.id = monxml.attr( "id" )
        mon.name = monxml.attr( "name" )
        mon.level = monxml.attr( "level" )
        mon.reaction_time = int(monxml.attr( "reaction" ))
        mon.attack = int(monxml.attr( "attack" ))
        mon.description = monxml.find( "description" ).text
        mon.puzzle = Puzzle()
        mon.puzzle.problem_text = monxml.find( "problem" ).text
        mon.puzzle.solution_text = monxml.find( "solution" ).text
        keywordsxml = monxml.find( "keywords" )
        if keywordsxml is not None:
            for keyword in keywordsxml.find( "keyword" ):
                mon.puzzle.keywords.append( keyword.text )
        checker = monxml.find( "checker" ).text
        if checker == "MATCH_KEYWORDS":
            mon.puzzle.solution_checker = mon.puzzle.match_keyword_solution
        elif checker == "MATCH_INEXACT":
            mon.puzzle.solution_checker = mon.puzzle.match_inexact_solution
        hintsxml = monxml.find( "hints" )
        if hintsxml is not None:
            for hintxml in hintsxml.find( "hint" ):
                mon.puzzle.hints.append( hintxml.text )
        monsters.append( mon )
    return MonsterFactory( monsters )

        
def load_items( filename ):
    itemsxml = parse_xml( filename )
    items = []
    for itemxml in itemsxml.find( "item" ):
        item = Item()
        item.name = itemxml.attr( "name" )
        item.level = int(itemxml.attr( "level" ))
        locationsxml = itemxml.find( "equip_locations" )
        if locationsxml is not None:
            for locationxml in locationsxml.find( "equip_location" ):
                if locationxml.text.lower() in [ Hero.PRIMARY_HAND.lower(), "primary_hand" ]:
                    item.equip_location.append( Hero.PRIMARY_HAND )
                elif locationxml.text.lower() in [ Hero.SECONDARY_HAND.lower(), "secondary_hand" ]:
                    item.equip_location.append( Hero.SECONDARY_HAND )
                elif locationxml.text.lower() in [ Hero.BODY.lower(), "body" ]:
                    item.equip_location.append( Hero.BODY )
                elif locationxml.text.lower() in [ Hero.LEGS.lower(), "legs" ]:
                    item.equip_location.append( Hero.LEGS )
                elif locationxml.text.lower() in [ Hero.HEAD.lower(), "head" ]:
                    item.equip_location.append( Hero.HEAD )
                elif locationxml.text.lower() in [ Hero.RING1.lower(), "ring 1", "ring1" ]:
                    item.equip_location.append( Hero.RING1 )
                elif locationxml.text.lower() in [ Hero.RING2.lower(), "ring 2", "ring2" ]:
                    item.equip_location.append( Hero.RING2 )
                elif locationxml.text.lower() in [ "ring" ]:
                    item.equip_location.append( Hero.RING1 )
                    item.equip_location.append( Hero.RING2 )
        carriablebyxml = itemxml.find( "carriable_by" )
        if carriablebyxml is not None:
            for heroxml in carriablebyxml.find( "hero" ):
                if heroxml.text.lower() == "any":
                    item.carriable_by.append( Item.ANY )
                elif heroxml.text.lower() in [ Hero.BARBARIAN.lower(), "barbarian" ]:
                    item.carriable_by.append( Hero.BARBARIAN )
                elif heroxml.text.lower() in [ Hero.ELF.lower(), "elf" ]:
                    item.carriable_by.append( Hero.ELF )
                elif heroxml.text.lower() in [ Hero.WIZARD.lower(), "wizard" ]:
                    item.carriable_by.append( Hero.WIZARD )
                elif heroxml.text.lower() in [ Hero.DWARF.lower(), "dwarf" ]:
                    item.carriable_by.append( Hero.DWARF )
        items.append( item )
    return ItemFactory( items )
        
        
def parse_xml( filename ):
	tree = ET.parse( filename )
    root = tree.getroot()
    return root
    
    
def write_xml( xml, filename ):
	tree = ET.ElementTree( xml )
    tree.write( filename )
    
   