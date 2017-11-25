from store import Store
import threading

class FlatFileStore( Store ):
    USER_FILE = "user.txt"
    GAME_FILE = "games.txt"
    ITEM_FILE = "items.txt"
    MONSTER_FILE = "monsters.txt"
    
    def __init__( self ):
        Store.__init__( self )
        self.users_lock = threading.RLock()
        self.items_lock = threading.RLock()
        self.games_lock = threading.RLock()
        self.monsters_lock = threading.RLock()
        
    ################################################################
    # User
    ################################################################
    def lock_users( self ):
        self.users_lock.acquire()
        
    def unlock_users( self ):
        self.users_lock.release()
    
    def load_users( self ):
        users = []
        fd = open( self.USER_FILE, "r" )
        for line in fd.readlines():
            user = self.__parse_user_line( line )
            users.append( user )
        fd.close()
        return users
    
    
    def save_users( self, users ):
        fd = open( self.USER_FILE, "w" )
        for user in users:
            self.__write_user_line( fd, user )
        fd.close()
        return True
    
    
    def __parse_user_line( self, line ):
        username, password, hash, sessionexp, lastlogin = line.split( "|" )
        user = User( username, password )
        user.hash = hash if hash != "" else None
        user.session_exp = sessionexp.strptime( "%Y-%m-%d %H:%M:%S" ) if sessionexp != "" else None
        user.last_login = lastlogin.strptime( "%Y-%m-%d %H:%M:%S" ) if lastlogin != "" else None
        return user
    

    def __write_user_line( self, fd, user ):
        fields = [
            user.username,
            user.password,
            user.hash if user.hash is not None else "",
            user.session_exp.stftime( "%Y-%m-%d %H:%M:%S" ) if user.session_exp is not None else "",
            user.last_login.strftime( "%Y-%m-%d %H:%M:%S" ) if user.last_login is not None else ""
        ]
        fd.write( "|".join( fields ) )
        
        
    ################################################################
    # Items
    ################################################################
    def lock_items( self ):
        self.items_lock.acquire()
        
    def unlock_items( self ):
        self.items_lock.release()
        
    def load_items( self ):
        items = []
        fd = open( self.ITEM_FILE, "r" )
        for line in fd.readlines():
            item = self.__parse_item_line( line )
            items.append( item )
        fd.close()
        return items
    
    
    def save_items( self, items ):
        fd = open( self.ITEM_FILE, "w" )
        for item in items:
            self.__write_item_line( fd, item )
        fd.close()
        return True
    
    
    def __parse_item_line( self, line ):
        name = line.split( "|" )
        item = Item( name )
        # TODO Finish this
        return item
    

    def __write_item_line( self, fd, item ):
        fields = [
            item.name,
            # TODO Add other item fields
        ]
        fd.write( "|".join( fields ) )
    
    
    ################################################################
    # Monsters
    ################################################################
    def lock_monsters( self ):
        self.monsters_lock.acquire()
        
    def unlock_monsters( self ):
        self.monsters_lock.release()
        
    def load_monsters( self ):
        monsters = []
        fd = open( self.MONSTER_FILE, "r" )
        for line in fd.readlines():
            monster = self.__parse_monster_line( line )
            monsters.append( monster )
        fd.close()
        return monsters
    
    
    def save_monsters( self, monsters ):
        fd = open( self.MONSTER_FILE, "w" )
        for monster in monsters:
            self.__write_monster_line( fd, monster )
        fd.close()
        return True
    
    
    def __parse_monster_line( self, line ):
        name = line.split( "|" )
        monster = Monster( name )
        # TODO Finish this
        return monster
    

    def __write_monster_line( self, fd, monster ):
        fields = [
            monster.name,
            # TODO Add other monster fields
        ]
        fd.write( "|".join( fields ) )
    
    ################################################################
    # Games
    ################################################################
    def lock_games( self ):
        self.games_lock.acquire()
        
    def unlock_games( self ):
        self.games_lock.release()
        
    def load_games( self ):
        games = []
        fd = open( self.GAME_FILE, "r" )
        for line in fd.readlines():
            game = self.__parse_game_line( line )
            games.append( game )
        fd.close()
        return games
    
    
    def save_games( self, games ):
        fd = open( self.GAME_FILE, "w" )
        for game in games:
            self.__write_game_line( fd, game )
        fd.close()
        return True
    
    
    def __parse_game_line( self, line ):
        name = line.split( "|" )
        game = Game( name )
        # TODO Finish this
        return game
    

    def __write_game_line( self, fd, game ):
        fields = [
            game.id,
            game.name,
            game.visibility,
            self.__get_dungeon_fields( game.dungeon ),
            self.__get_hero_fields( game.heros )
        ]
        fd.write( "|".join( fields ) )
        
        
    def __get_dungeon_fields( self, dungeon ):
        fields = [
            str(dungeon.depth),
        ]
        # TODO Add rooms
        return ""
    
    def __get_hero_fields( self, heros ):
        # TODO Implement this
        return ""
    
    