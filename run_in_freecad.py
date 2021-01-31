import sys
import sys
import socket
import traceback

from pathlib import Path

fc_home_dir = Path(__file__).parent.parent.absolute()
port = 37339

init = '''
import Web
Web.startServer("127.0.0.1", %d)
import sys
sys.path.append("%s")
''' % (port, fc_home_dir)



def run_main():
    stack = traceback.extract_stack()
    caller: traceback.FrameSummary = stack[-1]
    for frame in stack:
        if frame.filename == __file__:
            continue
        if frame.filename.startswith('<'):
            continue
        print("run_main() invoked from ", frame.filename)
        fn = frame.filename
        break

    print("Executing %s in freecad using web service(port %d)" % (fn, port))

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', port))
    try:
        sock.sendall(("""
try:
    exec(open('%s').read())
except:
    import logging
    logging.exception("FART")
    raise
""" % fn).encode())
        response = sock.recv(1024)
        print(response.decode().replace('"<string>"', f'"{fn}"', ), file=sys.stderr)
    finally:
        sock.close()
    sys.exit(0)

if 'FreeCAD' in sys.modules:
    pass
else:
    try:
        run_main()
    except ConnectionRefusedError:
        print("Can't connect! try running:\n%s" % init)
        raise