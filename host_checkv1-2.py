#!/usr/bin/env python3
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

def get_device_ipv4_address():
    """Retrieves first active IPv4 address by looping through installed network interfaces, skipping the loopback address"""
    
    device_interfaces = psutil.net_if_addrs()
    
    for interface_name, interface_addresses in device_interfaces.items():
        if interface_name == "lo":
            continue #skips the loopback address
        for address in interface_addresses:
            if address.family == socket.AF_INET:
                if interface_name.startswith('eth'):
                    interface_type = 'Ethernet'
                elif interface_name.startswith('wl'):
                    interface_type = 'Wi-Fi'
                else:
                    interface_type = 'Other'
                return address.address, address.netmask, interface_type #returns tuple if valid IPv4 address found
            
    
    #If no valid IPv4 address has been found, returning blank values for subnet_mask and interface_type
    return "Not Connected.", "", ""
        
    
    
def system_performance():
    '''Looks at system and returns performance data metrics as a dictionary'''
    #generate a list of all users currently logged in to a system
    users_list = psutil.users()
    #list comprehension creates a list of current user names
    user_names = [user.name for user in users_list]
    #make a single string of all logged on users
    logged_in = ", ".join(user_names)
    
    my_network_address,subnet_mask,interface_type = get_device_ipv4_address()
    
    cpu_usage = psutil.cpu_percent(interval=0.5)
    ram_usage = psutil.virtual_memory().percent
    disk_used = psutil.disk_usage("/").percent
    net_io = psutil.net_io_counters()
    byte_sent = byte_format(net_io.bytes_sent)
    byte_received = byte_format(net_io.bytes_recv)
    
    #check to see if system temperatures data is available, if so collect it for reporting
    
    cpu_temp = "N/A"
    try:
        #psutil returns dictionary of sensor data
        #coretemp is a common key on Linux OS machines
        temps = psutil.sensors_temperatures()
        if "coretemp" in temps:
            #Access first item in list of tuples
            cpu_temp = temps["coretemp"][0].current
        #add other checks for other OS systems
    except AttributeError:
        #handles error where core temperature is not implemented in the OS
        cpu_temp = "N/A"
    except Exception as e:
        print(f"Error getting CPU temperature : {e}")
    
    battery_level = round(psutil.sensors_battery().percent)
        
    return {
        "logged_in" : logged_in,
        "network_ip" : my_network_address,
        "subnet_mask" : subnet_mask,
        "interface_type" : interface_type,
        "cpu_usage" : cpu_usage,
        "cpu_temp" : cpu_temp,
        "ram_usage" : ram_usage,
        "disk_used" : disk_used,
        "byte_sent" : byte_sent,
        "byte_received" : byte_received,
        "battery_level" : battery_level
    }

def performance_display(performance_metric,current_host,current_os):
    '''Accepts a dictionary of performance metrics, name of the current host, and the current OS and displays them'''
    print("Python System Monitor Script")
    print(f"Host Name : {current_host}")
    print(f"OS Platform : {current_os}")
    print(f"IPv4 Address : {performance_metric['network_ip']} Subnet mask : {performance_metric['subnet_mask']} Interface : {performance_metric['interface_type']}")
    print(f"Logged in users: {performance_metric['logged_in']}")
    print(f"CPU Usage : {performance_metric['cpu_usage']}%")
    print(f"CPU Temp : {performance_metric['cpu_temp']}°")
    print(f"RAM Usage : {performance_metric['ram_usage']}%")
    print(f"Disk Usage : {performance_metric['disk_used']}%")
    print(f"Bytes Sent : {performance_metric['byte_sent']}")
    print(f"Bytes Received : {performance_metric['byte_received']}")
    print(f"Battery Level : {performance_metric['battery_level']}%")
    print("CTRL + C to end program.")

def write_csv_header(log_file_name, performance_metric,current_host,current_os):
    '''Check to see if file is new, and if so write a header row for the log data'''
    #Define the header row contents, based on keys in the performance dictionary
    header_row = "current_host" +"," + "current_os" + "," + ",".join(performance_metric.keys())
    #Check to see if log file exists and is not empty
    if not os.path.exists(log_file_name) or os.stat(log_file_name).st_size == 0:
        with open(log_file_name, "a") as log_file:
            log_file.write(f"timestamp,{header_row}\n")

def log_data(performance_metric,current_host,current_os):
    '''collects host performance data as CSV data and returns that data to a cache list'''
    #Create a timestamp for the log entry
    now = datetime.datetime.now()
    time_stamp = now.strftime("%Y-%m-%d %H:%M:%S")
    
    #Create the log entry in CSV format
    log_entry = (
        f"{time_stamp},"
        f"{current_host},"
        f"{current_os},"
        f"{performance_metric['logged_in']},"
        f"{performance_metric['network_ip']},"
        f"{performance_metric['subnet_mask']},"
        f"{performance_metric['interface_type']},"
        f"{performance_metric['cpu_usage']},"
        f"{performance_metric['cpu_temp']},"
        f"{performance_metric['ram_usage']},"
        f"{performance_metric['disk_used']},"
        f"{performance_metric['byte_sent']},"
        f"{performance_metric['byte_received']},"
        f"{performance_metric['battery_level']}\n"
        )
    return log_entry
    
def write_log(performance_cache, current_host):
    #Write the log entry to the file
    date_string = datetime.date.today().strftime("%Y-%m-%d")
    log_file_name = f"{current_host}_{date_string}.csv"
    
    try:
        with open(log_file_name, "a") as log_file:
            log_file.write("".join(performance_cache))
    except IOError as e:
        print(f"Failed to write log entry: {e}")
    
def main():
    '''Main function to run the system monitoring application'''
    performance_cache = [] #initialize performance data cache list
    
    #retrieve static system information
    current_host = get_hostname()
    current_os = my_os()
    
    #create first line data for header of the performance CSV file
    my_systemdata = system_performance()
    # Call write_csv_header directly
    date_string = datetime.date.today().strftime("%Y-%m-%d")
    log_file_name = f"{current_host}_{date_string}.csv"
    write_csv_header(log_file_name, my_systemdata, current_host, current_os)
    
    try:
        while True:
            start_time = time.time() #set start time of loop
            #print the screen escape sequence to clear the screen between loops
            clear_screen()
            my_systemdata = system_performance()
            performance_display(my_systemdata,current_host,current_os)
            performance_cache.append(log_data(my_systemdata,current_host,current_os))
            
            # Check if cache is full (e.g., after 60 seconds of data)
            if len(performance_cache) >= 60:
                write_log(performance_cache, current_host)
                performance_cache = [] # Clear the cache after writing
            
            #calculate the time elapsed to run through the loop
            elapsed_time = time.time() - start_time
            #calculate the balance of time left to sleep so this loop runs at regular 1-second intervals
            sleep_time = 1.0 - elapsed_time
            if sleep_time > 0:
                time.sleep(sleep_time)

    except KeyboardInterrupt:
        clear_screen()
        print("Exiting program.")
        if len (performance_cache) > 0:
            write_log(performance_cache, current_host)
            print("Writing cached data to the performance log.")
        #add a pause so user can confirm program has exited
        time.sleep(3)
    
if __name__ == "__main__":
    main()
