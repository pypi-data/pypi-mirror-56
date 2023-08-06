import os
import threading
import sys
import concurrent.futures
from common.cli import CLI
from common import utils
from blowpipe.logger import Logger
from blowpipe import config
from http.server import HTTPServer, SimpleHTTPRequestHandler


class ThreadPool(object):
    def __init__(self):
        self.workers = []
        self.futures = []
        self.pool = concurrent.futures.ThreadPoolExecutor(max_workers=3)
        self.logger = Logger("ThreadPool")

    def add(self, worker):
        pool = self.pool

        self.workers.append(worker)
        self.futures.append(pool.submit(worker.execute))

    def is_running(self) -> bool:
        for f in self.futures:
            if f.running():
                return True
        return False

    def quit(self):
        self.logger.debug(".quit()")
        for worker in self.workers:
            worker.quit()

        self.pool.shutdown(wait=True)

        for worker in self.workers:
            worker.on_quit()

        self.logger.debug(".quit() complete.")


def print_logo():
    import pyfiglet

    print(pyfiglet.figlet_format("blowpipe"))


class StdOutTrapper:
    def __init__(self):
        self.messages = []

    def clear(self):
        self.messages = []

    def write(self, msg):
        self.print(msg)

    def print(self, msg):
        self.messages.append(msg)
        self.messages.append("\n")

    def flush(self):
        pass

    def to_string(self):
        result = "".join(self.messages)
        self.clear()
        return result


class Webserver:
    def __init__(self, hostname="0.0.0.0", port=8000):
        self._hostname = hostname
        self._port = port
        self._is_running = False
        self._threadpool = None
        self._httpd = None
        self._quit = False

    def start(self):
        self._threadpool = ThreadPool()
        self._threadpool.add(self)

    def stop(self):
        self._threadpool.quit()

    def execute(self):
        try:
            import http.server
            import socketserver

            handler_fn = http.server.SimpleHTTPRequestHandler
            httpd = socketserver.TCPServer((self._hostname, self._port), handler_fn)
            self._httpd = httpd
            self._is_running = True
            while not self._quit:
                httpd.handle_request()
        except Exception as e:
            print(e)
        finally:
            self._is_running = False

    def on_quit(self):
        pass

    def quit(self):
        self._quit = True
        # because I block on a request, this allows me to shut it down
        import requests

        url = "http://localhost:" + str(self._port) + "/USER_GUIDE.md"
        result = requests.get(url)
        print(url)
        print(str(result))

    def is_running(self) -> bool:
        return self._is_running


def simple_http_server(host="localhost", port=4001, path="."):

    server = HTTPServer((host, port), SimpleHTTPRequestHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.deamon = True

    cwd = os.getcwd()

    def start():
        print(
            'bp_utils.simple_http_server() starting http server at "'
            + path
            + '" on port {}'.format(server.server_port)
        )
        os.chdir(path)
        thread.start()
        print(
            'bp_utils.simple_http_server() started http server at "'
            + path
            + '" on port {}'.format(server.server_port)
        )

    def stop():
        print(
            "bp_utils.simple_http_server() stopping http server on port {}".format(
                server.server_port
            )
        )
        os.chdir(cwd)
        server.shutdown()
        server.socket.close()
        print(
            "bp_utils.simple_http_server() stopped http server on port {}".format(
                server.server_port
            )
        )

    return start, stop


def is_server_running(cfg: config.BlowpipeConfig) -> bool:
    if not utils.is_port_available("0.0.0.0", cfg.get_grpc_port()):
        # looks like something is running on that port.
        # let's see if we can connect to it as the client; if we can
        # then we will be
        from blowpipe import client_cli

        client = client_cli.BlowpipeClient(cfg)
        result, _ = client.ping()
        if result:
            return True
        else:
            return False
    else:
        return False
