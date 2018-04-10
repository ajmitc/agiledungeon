from datetime import datetime, timedelta
import uuid

class User:
    SESSION_DURATION = 86400  # Seconds
    
    def __init__( self, username="", password="" ):
        self.username    = username
        self.password    = password
        self.hash        = None
        self.last_login  = None
        self.session_exp = None
        
        
    def renew_hash( self ):
        self.hash = str(uuid.uuid4())
        self.session_exp = datetime.utcnow() + timedelta( seconds=self.SESSION_DURATION )
        
        
    def login( self, username, password ):
        if self.username == username and self.password == password:
            self.renew_hash()
            self.last_login = datetime.utcnow()
            return True, self.hash
        return False, "Invalid username or password"
    
    
    def logout( self ):
        self.hash = None
        
    
    def is_valid_hash( self, hash ):
        return self.hash == hash
        
