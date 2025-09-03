"""Simple system monitoring tool using the psutil library
Shows CPU and RAM usage"""


import psutil
import time
import os
import socket
import datetime

def clear_screen():
    """Clears the screen using ANSI escape sequences"""
    print('\x1b[2J\x1b[H', end="")
    
def my_os():
    '''Detects OS script is running on'''
    if os.name == "posix":
        return "Posix"
    else:
        return "NT"

def get_hostname():
    '''retrieve hostname of computer'''
    return socket.gethostname()
    
def byte_format(bytesvalue, suffix="B"):
    """
    Iterates through a list of prefixes to properly scale byte values for display
    e.g. 1253656 => '1.25MB'
    """
    for unit in ["","K","M","G","P","T"]:
        if bytesvalue < 1024:
            return f"{bytesvalue:.2f}{unit}{suffix}"
        bytesvalue /= 1024

def system_performance():
    '''Looks at system and returns performance numbers as a dictionary'''
    current_host = get_hostname()
    current_os = my_os()
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    disk_used = psutil.disk_usage("/").percent
    net_io = psutil.net_io_counters()
    byte_sent = byte_format(net_io.bytes_sent)
    byte_received = byte_format(net_io.bytes_recv)
    
    return {
        "current_host" : current_host,
        "current_os" : current_os,
        "cpu_usage" : cpu_usage,
        "ram_usage" : ram_usage,
        "disk_used" : disk_used,
        "byte_sent" : byte_sent,
        "byte_received" : byte_received
    }

def performance_display(performance_metric):
    '''Accepts a dictionary of performance metrics and displays them'''
    print(f"Host Name : {performance_metric['current_host']}")
    print(f"OS Platform : {performance_metric['current_os']}")
    print(f"CPU Usage : {performance_metric['cpu_usage']}%")
    print(f"RAM Usage : {performance_metric['ram_usage']}%")
    print(f"Disk Usage : {performance_metric['disk_used']}%")
    print(f"Bytes Sent : {performance_metric['byte_sent']}")
    print(f"Bytes Received : {performance_metric['byte_received']}")

def write_csv_header(log_file_name, performance_metric):
    '''Check to see if file is new, and if so write a header row for the log data'''
    #Define the header row contents, based on keys in the performance dictionary
    header_row = "," .join(performance_metric.keys())
    #Check to see if log file exists and is not empty
    if not os.path.exists(log_file_name) or os.stat(log_file_name).st_size == 0:
        with open(log_file_name, "a") as log_file:
            log_file.write(f"timestamp,{header_row}\n")

def log_data(performance_metric):
    '''logs host performance data to a daily CSV file'''
    #Create a timestamp for the log entry
    now = datetime.datetime.now()
    time_stamp = now.strftime("%Y-%m-%d %H:%M:%S")
    date_string = now.strftime("%Y-%m-%d")
    
    #Define a log file name based on the date
    log_file_name = f"{performance_metric['current_host']}_{date_string}.csv"
    
    #check to see if the log file exists and write the log header row if necessary
    write_csv_header(log_file_name,performance_metric)
    
    #Create the log entry in CSV format
    log_entry = (
        f"{time_stamp},"
        f"{performance_metric['current_host']},"
        f"{performance_metric['current_os']},"
        f"{performance_metric['cpu_usage']},"
        f"{performance_metric['ram_usage']},"
        f"{performance_metric['disk_used']},"
        f"{performance_metric['byte_sent']},"
        f"{performance_metric['byte_received']}\n"
        )
        
    #Write the log entry to the file
    with open(log_file_name, "a") as log_file:
        log_file.write(log_entry)
        
    
def main():
    '''Main function to run the system monitoring application'''    
    while True:
        #print the screen escape sequence to clear the screen between loops
        clear_screen()
        my_systemdata = system_performance()
        performance_display(my_systemdata)
        log_data(my_systemdata)
        time.sleep(1)

if __name__ == "__main__":
    main()
