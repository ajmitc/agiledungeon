
class Store:
    """
    Baseclass for storage solutions (flat file, DB, etc)
    """
    def __init__( self ):
        pass

    
    def lock_users( self ):
        pass
    
    def unlock_users( self ):
        pass
    
    def load_users( self ):
        pass
    
    def save_users( self, users ):
        pass
    
    def lock_games( self ):
        pass
    
    def unlock_games( self ):
        pass
    
    def load_games( self ):
        pass
    
    def save_games( self, games ):
        pass
    
    def lock_items( self ):
        pass
    
    def unlock_items( self ):
        pass
    
    def load_items( self ):
        pass
    
    def save_items( self, items ):
        pass