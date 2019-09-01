#!/usr/bin/env python

import base64
from binascii import hexlify
import os
import socket
import sys
import threading
import traceback

import paramiko
from paramiko.py3compat import b, u, decodebytes


# setup logging
paramiko.util.log_to_file("demo_server.log")

host_key = paramiko.RSAKey(filename="test_rsa.key")
# host_key = paramiko.DSSKey(filename='test_dss.key')

#print("Read key: " + u(hexlify(host_key.get_fingerprint())))


class Server(paramiko.ServerInterface):

    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if (username == "ritlug4") and (password == "something?"):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_auth_publickey(self, username, key):
        return paramiko.AUTH_FAILED

    def check_auth_gssapi_with_mic(
        self, username, gss_authenticated=paramiko.AUTH_FAILED, cc_file=None
    ):
        return paramiko.AUTH_FAILED

    def check_auth_gssapi_keyex(
        self, username, gss_authenticated=paramiko.AUTH_FAILED, cc_file=None
    ):

        return paramiko.AUTH_FAILED

    def enable_auth_gssapi(self):
        return True

    def get_allowed_auths(self, username):
        return "gssapi-keyex,gssapi-with-mic,password,publickey"

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(
        self, channel, term, width, height, pixelwidth, pixelheight, modes
    ):
        return True


def runClient(client):
    try:
        t = paramiko.Transport(client, gss_kex=False)
        t.set_gss_host(socket.getfqdn(""))
        try:
            t.load_server_moduli()
        except:
            print("(Failed to load moduli -- gex will be unsupported.)")
            raise
        t.add_server_key(host_key)
        server = Server()
        try:
            t.start_server(server=server)
        except paramiko.SSHException:
            print("*** SSH negotiation failed.")
            sys.exit(1)

        # wait for auth
        chan = t.accept(20)
        if chan is None:
            print("*** No channel.")
            #sys.exit(1)
	    return
        print("Authenticated!")

        server.event.wait(10)
        if not server.event.is_set():
            print("*** Client never asked for a shell.")
            sys.exit(1)

        chan.send("\r\n\r\nWelcome to my nifty little SSH server!\r\n\r\n")

        chan.send(" --------------\r\n< Danger Zone! >\r\n --------------\r\n     \\\r\n      \\ __/          \\\\\r\n       \\  <-/           l'>\r\n          // **         ll\r\n          ll---ll\\      llama~\r\n          ll   ll       || ||\r\n          ^^   ^^       '' ''")

        chan.send("\r\n\r\nAnswer the following questions to proceed to the hint at the end.\r\n\r\n")
        chan.send("You won't be able to see the text that you are typing -- sorry about that.\r\n\r\n")

        chan.send("Url of the RITlug slack: ")
        f = chan.makefile("rU")
        ritlugURL = str(f.readline().strip("\r\n"))

        if ritlugURL.lower() != "rit-lug.slack.com":
            chan.send("\r\nWrong!\r\n")
            return
        chan.send("\r\nCorrect!\r\n")

        chan.send("Name of repository on RITlug github which has the most forks: ")
        ritlugRepo = str(f.readline().strip("\r\n"))

        if ritlugRepo.lower() != "teleirc":
            chan.send("\r\nWrong!\r\n")
            return
        chan.send("\r\nCorrect!\r\n")

        chan.send("URL where you can download TogerOS: ")
        tigerOSMirror = str(f.readline().strip("\r\n"))

        if "mirrors.ritlug.com" not in tigerOSMirror.lower():
            chan.send("\r\nWrong!\r\n")
            return
        chan.send("\r\nCorrect!\r\n")
        chan.send("\r\n            _../|_\r\n          ='__   _~-.\r\n               \\'  ~-`\\._\r\n                     |/~`\r\n    .    .   .    .    .    .    .\r\n._.`(._.`(_.`(._.`(._.`(._.`(._.`(._\r\n")

        chan.send("Next hint:\r\n")
        chan.send("host: localhost  --on starting vm\r\n")
        chan.send("key: ritlugFunziesPassword\r\n")
        chan.send("hint: there is a remote web-server running on port 7777\r\n")

    except Exception as e:
        print("*** Caught exception: " + str(e.__class__) + ": " + str(e))
        traceback.print_exc()
        try:
            t.close()
        except:
            pass
        #sys.exit(1)


class ClientSession (threading.Thread):
    def __init__(self, clientCon):
        self.__clientCon = clientCon
        threading.Thread.__init__(self)

    def run (self):
        runClient(self.__clientCon)
        self.__clientCon.close()





# now connect
try:

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", 3333))
except Exception as e:
    print("*** Bind failed: " + str(e))
    traceback.print_exc()
    sys.exit(1)

while(True):
    try:
        DoGSSAPIKeyExchange = True
        sock.listen(100)
        print("Listening for connection ...")
        client, addr = sock.accept()
        ClientSession(client).start()
    except Exception as e:
        print("*** Listen/accept failed: " + str(e))
        traceback.print_exc()
        sys.exit(1)

    print("Got a connection!")


