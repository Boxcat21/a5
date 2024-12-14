#!/usr/bin/env python3
import socket
import argparse
import random
from pathlib import Path
from typing import Tuple


# TODO feel free to use this helper or not
def send_common_info(sock: socket.socket, server_address: str, server_port: int) -> Tuple[int, int]:
    # TODO: Connect to the server and propose a base number and prime
    # TODO: You can generate these randomly, or just use a fixed set
    g = 11
    N = 31

    pkt_str = json.dumps(
        {"type": "data", "seq": seq, "id": packet_id, "payload": data[seq[0]:seq[1]]}
    ).encode()

    # TODO: Return the tuple (base, prime modulus)
    return (g, N)

# Do NOT modify this function signature, it will be used by the autograder
def dh_exchange_client(server_address: str, server_port: int) -> Tuple[int, int, int, int]:
    # TODO: Create a socket 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to the server
    s.connect((server_address, server_port))
    # TODO: Send the proposed base and modulus number to the server using send_common_info

    g, N = send_common_info(s, server_address, server_port)

    # TODO: Come up with a random secret key

    x = random.randint(0, N - 2)

    # TODO: Calculate the message the client sends using the secret integer.

    gx = pow(g, x, N)

    # TODO: Exhange messages with the server

    # send gx
    #receive gy
    gy = 0

    # TODO: Calculate the secret using your own secret key and server message

    gxy = pow(gy, x, N)

    # TODO: Return the base number, the modulus, the private key, and the shared secret

    return (g, N, x, gxy)


def main(args):
    if args.seed:
        random.seed(args.seed)
    
    dh_exchange_client(args.address, args.port)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-a",
        "--address",
        default="127.0.0.1",
        help="The address the client will connect to.",
    )
    parser.add_argument(
        "-p",
        "--port",
        default=8000,
        type=int,
        help="The port the client will connect to.",
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
