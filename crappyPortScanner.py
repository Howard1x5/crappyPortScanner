#!/usr/bin/python3

# Import required modules
import argparse
import socket
import threading
import time

# Define a function to scan a single port
def scan_port(target, port):
    # Create a new socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Set a timeout value of 1 second
    s.settimeout(1)
    # Attempt to connect to the target IP address and port number
    result = s.connect_ex((target, port))
    # If the connection was successful, print a message indicating that the port is open
    if result == 0:
        print(f"Port {port} is open")
    # Close the socket
    s.close()

# Define a function to scan a range of ports on a target IP address
def scan_target(target, start_port, end_port):
    # Print a message indicating the target IP address and port range to be scanned
    print(f"Scanning target {target} from port {start_port} to {end_port}")
    # Record the start time of the scan
    start_time = time.time()
    # Create a new thread for each port in the range, calling the scan_port function with the target IP address and port number
    for port in range(start_port, end_port + 1):
        threading.Thread(target=scan_port, args=(target, port)).start()
    # Print a message indicating that the scan has completed, along with the time taken to complete the scan
    print(f"Scan completed in {time.time() - start_time:.2f} seconds")

# Define the main function to parse command-line arguments and start the port scan
def main():
    # Create a new ArgumentParser object
    parser = argparse.ArgumentParser(description="Simple port scanner")
    # Add command-line arguments for the target IP address, start and end ports
    parser.add_argument("target", help="IP address or hostname to scan")
    parser.add_argument("--start-port", type=int, default=1, help="starting port number (default: 1)")
    parser.add_argument("--end-port", type=int, default=65535, help="ending port number (default: 65535)")
    # Parse the command-line arguments
    args = parser.parse_args()

    try:
        # Attempt to resolve the target IP address from the hostname provided
        target_ip = socket.gethostbyname(args.target)
    except socket.gaierror:
        # If an error occurs, print an error message and exit the program
        print(f"Error: Could not resolve hostname {args.target}")
        return

    # Call the scan_target function with the target IP address and port range specified in the command-line arguments
    scan_target(target_ip, args.start_port, args.end_port)

# If the script is being run as the main program, call the main function
if __name__ == "__main__":
    main()
