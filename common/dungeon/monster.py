import random

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
    