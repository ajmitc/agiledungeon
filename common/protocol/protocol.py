from proto_command import *

# COMMAND|HASH|ARGS*
# RESPONSE|ARGS*
# Error:
# ERROR|COMMAND|ERROR_CODE|ERROR_MESSAGE

def parse_command( cmdstr ):
    if cmdstr == "":
        return None
    cmd = ProtocolCommand()
    parts = cmdstr.split( "|" )
    cmd.command = parts[ 0 ].upper()
    if cmd.command == ProtocolCommand.ERROR:
        # [ self.ERROR, str(self.error_command), str(self.error_code), self.error_msg if self.error_msg is not None else "Error message not given" ]
        cmd.error_command = parts[ 1 ]
        cmd.error_code = int(parts[ 2 ])
        cmd.error_msg = parts[ 3: ]
    elif cmd.is_response():
        cmd.args = parts[ 1: ]
    else:
        cmd.hash = parts[ 1 ]
        cmd.args = parts[ 2: ]
    cmd.parse_args( cmd.args )
    return cmd


def create_response( cmd, error_code=None, error_message=None ):
    if error_code is not None:
        resp = cmd.get_error_response( error_code, error_message )
    else:
        resp = cmd.get_response()
    return resp


def create_error_response( cmd, code, msg ):
    cmd = ProtocolCommand( ProtocolCommand.ERROR )
    cmd.error_command = cmd
    cmd.error_code = code
    cmd.error_msg = msg
    return cmd