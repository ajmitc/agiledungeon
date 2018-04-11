import random
import xml.etree.ElementTree as ET

class Monster:
    """
    A monster is a puzzle that must be solved 
    """
    def __init__( self, name="", desc="" ):
        self.id = 0
        self.level = 1
        self.name = name
        self.description = desc
        # Number of seconds the player has to submit a solution before the monster attacks. If the monster hits the player, the player loses some hitpoints and this timer is restarted.
        self.reaction_time = 120
        # Number of hitpoints inflicted on hero for a wrong guess or reaction_time expires
        self.attack = 1
        self.puzzle = None
        self.next_monster = None  # define monster chains
        
        
    def clone( self ):
        other = Monster( self.name, self.description )
        other.id = self.id
        other.level = self.level
        other.reaction_time = self.reaction_time
        other.attack = self.attack
        other.puzzle = self.puzzle.clone() if self.puzzle is not None else None
        other.next_monster = self.next_monster
        return other


    def to_xml( self ):
        elMonster = ET.Element( "monster" )
        elMonster.set( "id", str(self.id) )
        elMonster.set( "level", str(self.level) )
        elMonster.set( "name", self.name )
        elMonster.set( "desc", self.description )
        elMonster.set( "reactionTime", str(self.reaction_time) )
        elMonster.set( "attack", str(self.attack) )
        elMonster.set( "nextMonster", str(self.next_monster) if self.next_monster is not None else "-1" )
        elPuzzle = self.puzzle.to_xml() if self.puzzle is not None else None
        if elPuzzle is not None:
            elMonster.append( elPuzzle )
        return elMonster


    def from_xml( self, xml ):
        if xml.tag != "monster":
            return False
        self.id = int(xml.get( "id" ))
        self.level = int(xml.get( "level" ))
        self.name  = xml.get( "name" )
        self.description = xml.get( "desc" )
        self.reaction_time = int(xml.get( "reactionTime" ))
        self.attack = int(xml.get( "attack" ))
        self.next_monster = int(xml.get( "nextMonster" ))
        if self.next_monster == -1:
            self.next_monster = None
        for child in xml:
            if child.tag == "puzzle":
                self.puzzle = Puzzle()
                self.puzzle.from_xml( child )
        return True


class Puzzle:
    def __init__( self ):
        self.problem_text = None  # String or callable
        self.solution_text = None  # String or callable
        self.solution_checker = self.match_exact_solution  # Method that checks if user-supplied solution is correct
        self.keywords = []
        self.hints = []
        self.guesses = []


    def match_exact_solution( self, inp ):
        """ Case sensitive solution match """
        return inp == self.solution_text
    
    def match_inexact_solution( self, inp ):
        """ Case insensitive solution match """
        return inp.lower() == self.solution_text.lower()
    
    def match_keyword_solution( self, inp ):
        for keyword in self.keywords:
            if not inp.lower().find( keyword.lower() ):
                return False
        return True
    
    
    def clone( self ):
        other = Puzzle()
        other.problem_text = self.problem_text
        other.solution_text = self.solution_text
        other.solution_checker = self.solution_checker
        [ other.keywords.append( kw ) for kw in self.keywords ]
        [ other.hints.append( h ) for h in self.hints ]
        [ other.guesses.append( g ) for g in self.guesses ]
        return other


    def to_xml( self ):
        elPuzzle = ET.Element( "puzzle" )
        elProblem = ET.SubElement( elPuzzle, "problem" )
        elProblem.text = self.problem_text
        elSolution = ET.SubElement( elPuzzle, "solution" )
        elSolution.text = self.solution_text
        checker = "exact"
        if self.solution_checker == self.match_inexact_solution:
            checker = "inexact"
        elif self.solution_checker == self.match_keyword_solution:
            checker = "keyword"
        elSolution.set( "checker", checker )
        elKeywords = ET.SubElement( elPuzzle, "keywords" )
        for keyword in self.keywords:
            elKeyword = ET.SubElement( elKeywords, "keyword" )
            elKeyword.text = keyword
        elHints = ET.SubElement( elPuzzle, "hints" )
        for hint in self.hints:
            elHint = ET.SubElement( elHints, "hint" )
            elHint.text = hint
        elGuesses = ET.SubElement( elPuzzle, "guesses" )
        for guess in self.guesses:
            elGuess = ET.SubElement( elGuesses, "guess" )
            elGuess.text = guess
        return elPuzzle


    def from_xml( self, xml ):
        if xml.tag != "puzzle":
            return False
        elProblem = xml.find( "problem" )
        self.problem_text = elProblem.text
        elSolution = xml.find( "solution" )
        self.solution_text = elSolution.text
        checker = elSolution.get( "checker" )
        if checker == "exact":
            self.solution_checker = self.match_exact_solution
        elif checker == "inexact":
            self.solution_checker = self.match_inexact_solution
        elif checker == "keyword":
            self.solution_checker = self.match_keyword_solution
        elKeywords = xml.find( "keywords" )
        for elKeyword in elKeywords:
            self.keywords.append( elKeyword.text )
        elHints = xml.find( "hints" )
        for elHint in elHints:
            self.hints.append( elHint.text )
        elGuesses = xml.find( "guesses" )
        for elGuess in elGuesses:
            self.guesses.append( elGuess.text )
        return True

    
class MonsterFactory:
    def __init__( self, monsters ):
        self.monsters = monsters
        
        
    def get( self, name ):
        for monster in self.monsters:
            if monster.name.lower() == name.lower():
                return monster.clone()
        return None
    
    
    def get_random( self, dungeon_level ):
        pot = [ monster for monster in self.monsters if monster.level <= dungeon_level ]
        monster = random.choice( pot )
        return monster.clone()
    
