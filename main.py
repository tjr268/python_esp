''' This is the main loop that runs on the board after boot.py finishes.
Currently this accepts GET requests and ignores all others. Further it 
will close stop reading lines after the headers. This means it wont even read 
data included in the request body. We get away with this because we are only
interested in the URI. 

Whenever the board receives a GET request it will parse the URI two objects
the first entry in the path serves as the desired endpoint - ie it defines
the handler function to run. Then any entries after that in the path will 
be passed to the specified handler as a list where each entry is an item 
in this list. Order is preserved, all values are treated as strings. All 
handlers are defined separately in addition to the mapping between endpoints
and handler functions. This is to ensure main.py never has to be changed 
between boards/use cases. See handlers.py for more info.

All handlers must return a (bool, string) tuple where the bool corresponds
to the success of the operation and the string is a description which will 
be sent to the client in the response body.

Note that this is not the standard way of handling HTTP requests however
it works well enough for this use case. 
'''

try:
    import usocket as socket
except:
    import socket
from machine import Pin
from handlers import * 

SUCCESS_MESSAGE = ("HTTP/1.1 200 OK\n"
         +"Content-Type: text/plain\n"
         +"Access-Control-Allow-Origin: *\n"
         +"\n")

FAIL_MESSAGE = ("HTTP/1.1 400 Bad Request\n"
         +"Content-Type: text/plain\n"
         +"Access-Control-Allow-Origin: *\n"
         +"\n")


# DONT CHANGE UPDATE HANDLERS FILE ONLY
def main():
    s = socket.socket()

    ai = socket.getaddrinfo("0.0.0.0", 8080)
    addr = ai[0][-1]

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)

    while True:
        # socket stuff 
        res = s.accept()
        client_sock = res[0]
        client_addr = res[1]
        print("Client address:", client_addr)
        print("Client socket:", client_sock)
        print("Request:")

        command = None
        while True:
            stream_line = client_sock.readline()
            # currently set to only read the headers and break before body since expecting a GET and only need URI
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


        # build response
        if command in HANDLER_TABLE.keys():
            handler_function = HANDLER_TABLE[command]
            handler_response = handler_function(values)
            if handler_response[0] == False:
                client_response = FAIL_MESSAGE + handler_response[1] + "\n"
            elif handler_response[0] == True:
                client_response = SUCCESS_MESSAGE + handler_response[1] + "\n"
        else:
            client_response = FAIL_MESSAGE + "Command not recognized\n"
        

        # respond to client
        print("\nResponse: \n"+ str(client_response))
        client_sock.write(client_response)
        client_sock.close()


main()
