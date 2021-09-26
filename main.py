try:
    import usocket as socket
except:
    import socket
from machine import Pin
from led_handlers import * 

CONTENT = b"""\
HTTP/1.0 200 OK

Received command: %s, with values: %s, operation: %s
"""


# DONT CHANGE UPDATE HANDLERS FILE ONLY
def main(micropython_optimize=False):
    s = socket.socket()

    # Binding to all interfaces - server will be accessible to other hosts!
    ai = socket.getaddrinfo("0.0.0.0", 8080)
    print("Bind address info:", ai)
    addr = ai[0][-1]

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    print("Listening, connect your browser to http://<this_host>:8080/")

    while True:
        # socket stuff 
        res = s.accept()
        client_sock = res[0]
        client_addr = res[1]
        print("Client address:", client_addr)
        print("Client socket:", client_sock)

        if not micropython_optimize:
            # To read line-oriented protocol (like HTTP) from a socket (and
            # avoid short read problem), it must be wrapped in a stream (aka
            # file-like) object. That's how you do it in CPython:
            client_stream = client_sock.makefile("rwb")
        else:
            # .. but MicroPython socket objects support stream interface
            # directly, so calling .makefile() method is not required. If
            # you develop application which will run only on MicroPython,
            # especially on a resource-constrained embedded device, you
            # may take this shortcut to save resources.
            client_stream = client_sock

        print("Request:")

        while True:
            stream_line = client_stream.readline()
            if stream_line == b"" or stream_line == b"\r\n":
                break
            print(stream_line)
            stream_line_decode = stream_line.decode("utf-8")
            if stream_line_decode.startswith("GET") and not stream_line_decode.startswith("GET /fav"):
                endpoint = stream_line_decode.split()[1]
                endpoint_list = endpoint.split("/")
                endpoint_list.pop(0)
                command = endpoint_list.pop(0)
                values = endpoint_list

        # ONLY CHANGE THESE: command control handlers
        if command in HANDLER_TABLE.keys():
            handler_function = HANDLER_TABLE[command]
            handler_response = handler_function(command, values)
        else:
            handler_response = "Command not recognized"
        

        # respond to client
        client_response = CONTENT % (command, values, handler_response)
        print("\nResponse: \n"+ str(client_response))
        client_stream.write(client_response)
        client_stream.close()
        
        if not micropython_optimize:
            client_sock.close()
        print()



main(micropython_optimize=True)
