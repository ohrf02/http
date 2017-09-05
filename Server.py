import socket
import os
import datetime


def http_server():
    """
    The main http server-loop
    :return: None
    """
    soc = socket.socket()
    soc.bind(("0.0.0.0", 8080))
    soc.listen(5)
    print "Server is up and running!!!"

    try:
        # The server's loop.
        while True:
            # Waits for connections from clients.
            (soc_client, client_address) = soc.accept()
            data = soc_client.recv(1000)

            # Checks if the client's request is an http-format.
            if data.split("\r\n")[0][:3] == "GET":
                if len(data.split("\r\n")[0].split(" ")) == 3:
                    # If the file exists in the server => send it to the client.
                    if os.path.isfile(data.split("\r\n")[0].split(" ")[1][1:]):
                        # Reads the requested file content.
                        hFile = open(data.split(" ")[1][1:], 'r')
                        file_data = hFile.read()
                        hFile.close()

                        # Sends a response to the client with the requested file's content.
                        soc_client.sendall(get_http_ok(file_data))
                    else:
                        # If the file does not exist in the server => send an error to the client(404 not found).
                        soc_client.sendall(get_http_not_found())

            # Closes the connection to the client.
            soc_client.shutdown(socket.SHUT_RDWR)
            soc_client.close()

    except socket.error, crap:
        print "ERROR: " + str(crap)


def get_http_ok(file_data):
    """
    Builds a response(200 OK) to the client in http format.
    :param file_data: The content of the requested file.
    :return: A response to the client (200 OK).
    """
    message = "HTTP/1.0 200 OK\r\n"
    message += "Date: " + str(datetime.datetime.now()) + "\r\n"
    message += "Content-Type: text/html\r\n"
    message += "Content-Length: " + str(len(file_data))
    message += "\r\n\r\n" + file_data

    return message


def get_http_not_found():
    """
    Builds an error-response(404 not found) to the client in http format.
    :return:  Am error-response to the client (404 not found).
    """
    message = "HTTP/1.0 404 Not Found\r\n"
    message += "Date: " + str(datetime.datetime.now()) + "\r\n"
    message += "Content-Type: image/png\r\n"

    # Reads the 404-error image content to send to the client.
    hFile = open("pac-404.png", "rb+")
    file_data = hFile.read()
    hFile.close()

    message += "Content-Length: " + str(len(file_data))
    message += "\r\n\r\n" + file_data

    return message


if __name__ == '__main__':
    http_server()
