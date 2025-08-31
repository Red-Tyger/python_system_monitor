"""Simple system monitoring tool using the psutil library
Shows CPU and RAM usage"""

#import the psutil library
import psutil
#import the time library
import time
#import os library
import os

def clear_screen():
    """Clears the screen using ANSI escape sequences"""
    print('\x1b[2J\x1b[H', end="")
    
def my_os():
    '''Detects OS script is running on'''
    if os.name == "posix":
        return ("Posix")
    else:
        return ("NT")
    
def byte_format(bytesvalue, suffix="B"):
    """
    Iterates through a list of prefixes to properly scale byte values for display
    e.g. 1253656 => '1.25MB'
    """
    for unit in ["","K","M","G","P","T"]:
        if bytesvalue < 1024:
            return (f"{bytesvalue:.2f}{unit}{suffix}")
        bytesvalue /= 1024

def system_performance():
    '''Looks at system and returns performance numbers as a dictionary'''
    current_os = my_os()
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    disk_used = psutil.disk_usage("/").percent
    net_io = psutil.net_io_counters()
    byte_sent = byte_format(net_io.bytes_sent)
    byte_received = byte_format(net_io.bytes_recv)
    
    return {
        "current_os" : current_os,
        "cpu_usage" : cpu_usage,
        "ram_usage" : ram_usage,
        "disk_used" : disk_used,
        "byte_sent" : byte_sent,
        "byte_received" : byte_received
    }

def performance_display(performance_metric):
    '''Accepts a dictionary of performance metrics and displays them'''
    print(f"OS Platform : {performance_metric['current_os']}")
    print(f"CPU Usage : {performance_metric['cpu_usage']}%")
    print(f"RAM Usage : {performance_metric['ram_usage']}%")
    print(f"Disk Usage : {performance_metric['disk_used']}%")
    print(f"Bytes Sent : {performance_metric['byte_sent']}")
    print(f"Bytes Received : {performance_metric['byte_received']}")
    
while True:
    #print the screen escape sequence to clear the screen between loops
    clear_screen()
    my_systemdata = system_performance()
    performance_display(my_systemdata)
    time.sleep(1)
