#!/usr/bin/env python3
import socket
import argparse
import random
import json
from pathlib import Path
from typing import Tuple


# TODO feel free to use this helper or not
def receive_common_info(client_socket: socket.socket) -> Tuple[int, int]:
    # TODO: Wait for a client message that sends a base number.
    data = client_socket.recv(1024)
    recvd = json.loads(data.decode())
    assert recvd["type"] == "Ng"
    N, g = recvd["N"], recvd["g"]

    print("Base int is", g)
    print("Modulus is", N)
    # TODO: Return the tuple (base, prime modulus)
    return g, N

# Do NOT modify this function signature, it will be used by the autograder
def dh_exchange_server(server_address: str, server_port: int) -> Tuple[int, int, int, int]:
    # TODO: Create a server socket. can be UDP or TCP.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_address, server_port))
    server_socket.listen(5)
    client_socket, addr = server_socket.accept()
    # TODO: Read client's proposal for base and modulus using receive_common_info

    g, N = receive_common_info(client_socket)

    # TODO: Generate your own secret key

    y = random.randint(0, N - 2)
    print("Secret is", y)
    gy = pow(g, y, N)

    # TODO: Exchange messages with the client

    data = client_socket.recv(1024)
    recvd = json.loads(data.decode())
    assert recvd["type"] == "gx"
    gx = recvd["gx"]
    print("Int received from peer is", gx)
    #send gy
    gy_str = json.dumps(
        {"type": "gy", "gy": gy}
    ).encode()
    client_socket.send(gy_str)

    # TODO: Compute the shared secret.

    gxy = pow(gx, y, N)
    print("Shared secret is", gxy)

    # TODO: Return the base number, prime modulus, the secret integer, and the shared secret
    return (g, N, y, gxy)

def main(args):
    if args.seed:
        random.seed(args.seed)
    dh_exchange_server(args.address, args.port)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a",
        "--address",
        default="127.0.0.1",
        help="The address the server will bind to.",
    )
    parser.add_argument(
        "-p",
        "--port",
        default=8000,
        type=int,
        help="The port the server will listen on.",
    )
    parser.add_argument(
        "--seed",
        dest="seed",
        type=int,
        help="Random seed to make the exchange deterministic.",
    )
    # Parse options and process argv
    arguments = parser.parse_args()
    main(arguments)
