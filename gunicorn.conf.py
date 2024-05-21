import multiprocessing
import socket
import fcntl
import struct

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', bytes(ifname[:15], 'utf-8'))
    )[20:24])

# Determine the IP address dynamically based on the active network interface
ip_address = get_ip_address('en0')  # Assuming 'en0' is your active network interface

# Optimize the number of workers for M1 Pro MacBook
# The M1 Pro MacBook has 8 high-performance cores and 2 efficiency cores
# We'll allocate one worker per high-performance core
# You may adjust this based on your specific workload and performance requirements
workers = multiprocessing.cpu_count() *2 +1  # Leaving 2 cores for system tasks

bind = f"{ip_address}:8000"  
timeout = 300  # Increase timeout to 5 minutes for potentially longer processing times
preload = True  # Enable preload for faster startup times
loglevel = "info"  


# bind = "0.0.0.0:80"
# workers = 3
# timeout = 120