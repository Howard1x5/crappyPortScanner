#!/usr/bin/python3

import argparse  # Library for parsing command-line arguments
import socket    # Library for creating network sockets
import threading # Library for threading
import time      # Library for timing the execution of code

# Function for scanning a single port
def scan_port(target, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    result = s.connect_ex((target, port))
    if result == 0:
        print(f"Port {port} is open")
    s.close()

# Function for scanning a range of ports on a given target
def scan_target(target, start_port, end_port):
    print(f"Scanning target {target} from port {start_port} to {end_port}")
    start_time = time.time()
    for port in range(start_port, end_port + 1):
        threading.Thread(target=scan_port, args=(target, port)).start()
    print(f"Scan completed in {time.time() - start_time:.2f} seconds")

# Main function
def main():
    # Create parser for command-line arguments
    parser = argparse.ArgumentParser(description="Simple port scanner")

    # Add positional argument for target IP or hostname
    parser.add_argument("-t", "--target", required=True, help="IP address or hostname to scan")

    # Add optional argument for starting port number (default: 1)
    parser.add_argument("--start-port", type=int, default=1, help="starting port number (default: 1)")

    # Add optional argument for ending port number (default: 65535)
    parser.add_argument("--end-port", type=int, default=65535, help="ending port number (default: 65535)")

    # Add optional argument for displaying help message
    parser.add_argument("-?", "--hlp", action="help", help="show this help message and exit")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Attempt to resolve the target IP address
    try:
        target_ip = socket.gethostbyname(args.target)
    except socket.gaierror:
        print(f"Error: Could not resolve hostname {args.target}")
        return

    # Scan the target for open ports
    scan_target(target_ip, args.start_port, args.end_port)

if __name__ == "__main__":
    main()
