#!/usr/bin/env python3
import socket
import argparse
import random
from pathlib import Path
from typing import Tuple


# TODO feel free to use this helper or not
def receive_common_info() -> Tuple[int, int]:
    # TODO: Wait for a client message that sends a base number.
    # TODO: Return the tuple (base, prime modulus)
    pass

# Do NOT modify this function signature, it will be used by the autograder
def dh_exchange_server(server_address: str, server_port: int) -> Tuple[int, int, int, int]:
    # TODO: Create a server socket. can be UDP or TCP.

    # TODO: Read client's proposal for base and modulus using receive_common_info

    g, N = receive_common_info()

    # TODO: Generate your own secret key

    y = random.randint(0, N - 2)
    gy = pow(g, y, N)

    # TODO: Exchange messages with the client

    gx = 0 #receive gx
    #send gy

    # TODO: Compute the shared secret.

    gxy = pow(gx, y, N)

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
    # Parse options and process argv
    arguments = parser.parse_args()
    main(arguments)
