# The MIT License
#
# Copyright (c) 2019 imuxin https://github.com/imuxin.
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# PBR Generated from 'wsgi_scripts'

import threading

from xerox.server.wsgi import initialize_admin_application

if __name__ == "__main__":
    import argparse
    import sys
    import wsgiref.simple_server as wss

    parser = argparse.ArgumentParser(
        description=initialize_admin_application.__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        usage='%(prog)s [-h] [--port PORT] [--host IP] -- [passed options]')
    parser.add_argument('--port', '-p', type=int, default=8000,
                        help='TCP port to listen on')
    parser.add_argument('--host', '-b', default='',
                        help='IP to bind the server to')
    parser.add_argument('args',
                        nargs=argparse.REMAINDER,
                        metavar='-- [passed options]',
                        help="'--' is the separator of the arguments used "
                        "to start the WSGI server and the arguments passed "
                        "to the WSGI application.")
    args = parser.parse_args()
    if args.args:
        if args.args[0] == '--':
            args.args.pop(0)
        else:
            parser.error("unrecognized arguments: %s" % ' '.join(args.args))
    sys.argv[1:] = args.args
    server = wss.make_server(args.host, args.port,
                             initialize_admin_application())

    print("*" * 80)
    print("STARTING test server "
          "xerox.server.wsgi.initialize_admin_application")
    url = "http://%s:%d/" % (server.server_name, server.server_port)
    print("Available at %s" % url)
    print("DANGER! For testing only, do not use in production")
    print("*" * 80)
    sys.stdout.flush()

    server.serve_forever()
else:
    application = None
    app_lock = threading.Lock()

    with app_lock:
        if application is None:
            application = initialize_admin_application()
