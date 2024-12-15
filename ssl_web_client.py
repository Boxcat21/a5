#!/usr/bin/env python3
import ssl
import pprint
import socket
import argparse
from typing import Dict, Any
from pathlib import Path

'''
Simple script that creates a TCP client (optionally secured by SSL). This
client connects to a host and then simply fires off a single HTTP GET request.
If using SSL/HTTPS, it should also print the certificate.
'''

def craft_http_request(host: str, path: str) -> str:
    return f"GET {path} HTTP/1.1\r\nHost: {host}\r\n\r\n"

def create_socket(host: str, port: int, use_ssl: bool) -> socket.socket | ssl.SSLSocket:
    # TODO: Create a TCP socket and wrap it in an SSL context if use_ssl is true

    try:
        # Create a standard TCP socket
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if use_ssl:
            # Create an SSL context with secure defaults
            ssl_context = ssl.create_default_context()

            # overrides for self-signed certificate REMOVE
            ssl_context.check_hostname=False
            ssl_context.verify_mode=ssl.CERT_OPTIONAL
            ssl_context.load_verify_locations(cafile="cert.pem")

            # Wrap the socket with the SSL context
            secure_socket = ssl_context.wrap_socket(tcp_socket, server_hostname=host)
            
            # Connect the SSL socket to the host and port
            secure_socket.connect((host, port))
            return secure_socket
        else:
            # Connect the plain TCP socket to the host and port            
            tcp_socket.connect((host, port))
            return tcp_socket
    except Exception as e:
        # Handle exceptions (e.g., connection errors)
        print(f"An error occurred: {e}")
        raise


def get_peer_certificate(ssl_socket: ssl.SSLSocket) -> Dict[str, Any]:

    # TODO: Get the peer certificate from the connected SSL socket.
    try:
        cert = ssl_socket.getpeercert()
        if cert is None:
            raise ValueError("no certificate sad")
        else:
            return cert
    except Exception as e:
        print(f"An error occurred while retrieving the peer certificate: {e}")
        raise

def send_http_request(s: socket.socket | ssl.SSLSocket, request_string: str) -> str:
    # TODO: Send an HTTPS request to the server using the SSL socket.
    # TODO: receive response and return it as a string

    try:
        # Send the HTTP request
        s.sendall(request_string.encode('utf-8'))

        # Receive the response
        response = s.recv(10000)
        # while True:
        #     data = s.recv(4096)
        #     if not data:
        #         break
        #     response += data
        #     break
            # print('response per iteration\n\n',response)

        # Return the response as a string
        return response.decode('utf-8')
    except Exception as e:
        print(f"An error occurred while sending the HTTP request: {e}")
        raise


def main(args):
    s = create_socket(args.host, args.port, args.ssl)

    if (args.ssl):
        cert = get_peer_certificate(s)
        pprint.pprint(cert)

    request = craft_http_request(args.host, args.document)
    response = send_http_request(s, request)

    print("========================= HTTP Response =========================")
    print(response)
    s.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--host",
        default="news.ycombinator.com",
        type=str,
        help="The url/host we connect to",
    )

    parser.add_argument(
        "-d",
        "--document",
        default="/",
        type=str,
        help="The path to the document/webpage we want to retrieve"
    )

    parser.add_argument(
        "--ssl",
        action="store_true",
    )

    parser.add_argument(
        "-p",
        "--port",
        default=80,
        type=int,
        help="The port we connect to",
    )

    # Parse options and process argv
    arguments = parser.parse_args()
    main(arguments)
