

class BasicTerminalTable( object ):
    def __init__( self, display_headers=True ):
        self.headers = []
        self.column_data = []  # [ [row0 col0, row1 col0], [row0 col1, row1 col1], ... ]
        self.row = 0
        self.col = 0
        self.display_headers = display_headers


    def add( self, v, endrow=False ):
        """ Add a value to the next column in the current row """
        while len(self.column_data) < self.col:
            self.new_col()
        while len(self.column_data[ self.col ]) < self.row:
            self.new_row()
        self.column_data[ self.col ][ self.row ] = v
        self.col += 1
        if endrow:
            self.row += 1


    def new_row( self ):
        for l in self.column_data:
            l.append( None )


    def new_col( self, header=None ):
        self.column_data.append( [ None for i in xrange(len(self.column_data[ 0 ]) if len(self.column_data) > 0 else 0) ] )
        self.headers.append( header )


    def __str__( self ):
        max_col_width = 0
        for col in xrange( len(self.column_data) ):
            for row in xrange( len(self.column_data[ col ]) ):
                v = self.column_data[ col ][ row ]
                if v is not None and len(v) > max_col_width:
                    max_col_width = len(v)

        if self.display_headers:
            for header in self.headers:
                print "{:{width}}".format( header if header is not None else "", width=max_col_width )

        for col in xrange( len(self.column_data) ):
            for row in xrange( len(self.column_data[ col ]) ):
                v = self.column_data[ col ][ row ]
                if v is not None and len(v) > max_col_width:
                    print "{:{width}}".format( v, width=max_col_width )


