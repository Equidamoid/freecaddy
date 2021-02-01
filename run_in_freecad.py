import sys
import sys
import socket
import traceback
import tempfile
import os
from pathlib import Path


fc_home_dir = Path(__file__).parent.parent.absolute()
port = 37339

init = '''
import Web
Web.startServer("127.0.0.1", %d)
import sys
sys.path.append("%s")
''' % (port, fc_home_dir)

exec_template = '''
fc_home = '%s'
import sys
if not fc_home in sys.path:
    sys.path.append(fc_home)
import freecaddy.run_in_freecad
freecaddy.run_in_freecad.run_script('%s', '%s', locals=locals(), globals=globals())
'''


def run_script(path: str, error_pipe_path: str = None, globals=None, locals=None):
    print("Running script %r, error pipe %r", (path, error_pipe_path))
    old_fds = None
    if error_pipe_path:
        print("Enabling pipe redirect...")
        pipe_fd = open(error_pipe_path, 'w')
        old_fds = sys.stdout, sys.stderr
        sys.stdout = pipe_fd
        sys.stderr = pipe_fd
        print("Redirected")

    try:
        try:
            exec(open(path).read(), globals or {}, locals or {})
        except:
            import traceback
            traceback.print_exc(file=sys.stderr)
            raise
    finally:
        if error_pipe_path:
            print("fds", old_fds)
            sys.stdout, sys.stderr = old_fds
            pipe_fd.close()
    pass


def run_caller_in_freecad_web():
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

    fd, logfile = tempfile.mkstemp()
    os.close(fd)
    logfile = Path(logfile)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', port))
    try:
        sock.sendall((exec_template % (fc_home_dir, fn, logfile)).encode())
        response = sock.recv(1024)
        print("Server response: \n", response.decode().replace('"<string>"', f'"{fn}"', ), file=sys.stderr)
    finally:
        sock.close()

    out = logfile.read_text().replace('"<string>"', f'"{fn}"', )
    logfile.unlink()

    print("\n\nScript output:")
    print(out)

    sys.exit(0)


if 'FreeCAD' in sys.modules:
    pass
else:
    try:
        run_caller_in_freecad_web()
    except ConnectionRefusedError:
        print("Can't connect! try running:\n%s" % init)
        raise