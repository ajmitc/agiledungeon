import os
from uuid import uuid4
from store import Store
from manager.user.user import User
from common.game import Game
from common.item.item import Item
from common.dungeon.monster import Monster
from common.xml_util import parse_xml, write_xml
import threading
from datetime import datetime

class FlatFileStore( Store ):
    USER_FILE = "user.txt"
    GAME_DIR = "games"
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
        user.session_exp = datetime.strptime( sessionexp, "%Y-%m-%d %H:%M:%S" ) if sessionexp != "" else None
        user.last_login = datetime.strptime( lastlogin, "%Y-%m-%d %H:%M:%S" ) if lastlogin != "" else None
        return user
    

    def __write_user_line( self, fd, user ):
        fields = [
            user.username,
            user.password,
            user.hash if user.hash is not None else "",
            user.session_exp.strftime( "%Y-%m-%d %H:%M:%S" ) if user.session_exp is not None else "",
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
        for dirpath, directories, filenames in os.walk( self.GAME_DIR ):
            for fn in filenames:
                xml = parse_xml( os.path.join( dirpath, fn ) )
                game = Game()
                game.from_xml( xml )
                games.append( game )
        return games
    
    
    def save_game( self, game ):
        fn = str(uuid4())
        write_xml( game.to_xml(), os.path.join( self.GAME_DIR, fn ) )
        return True
    
    
    def __get_user_list( self, usernames ):
        return ",".join( usernames )
    
