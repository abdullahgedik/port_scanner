import socket

def validate_target(target):
    try:
        socket.gethostbyname(target)
        return True
    except socket.gaierror:
        return False
