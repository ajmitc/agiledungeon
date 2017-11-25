import os

def load_properties_file( filepath ):
    print "Loading properties at %s" % filepath
    if not os.path.exists( filepath ):
        print "%s not found, creating..." % filepath
        save_properties_file( filepath, {} )
    props = {}
    fd = open( filepath, "r" )
    for line in fd.readlines():
        name, value = line.split( "=" )
        name  = name.strip()
        value = value.strip()
        if value.lower() in [ "true", "t" ]:
            value = True
        elif value.lower() in [ "false", "f" ]:
            value = False
        try:
            value = int(value)
        except:
            pass
        props[ name ] = value
        print "Set %s = %s" % (name, value)
    fd.close()
    return props


def save_properties_file( filepath, props ):
    print "Saving properties file %s" % filepath
    fd = open( filepath, 'w' )
    for key in props.keys():
        fd.write( "%s = %s\n" % (key, str(props[ key ]) ) )
    fd.close()
    return True
