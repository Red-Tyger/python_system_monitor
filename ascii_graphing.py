#working file to build ascii graphing functions for Python System Monitor project
import psutil
import asciichartpy
import random
import time

'''
Keeping track of the metrics returned by the system_performance() function in the Python System Monitor
        "cpu_usage" : cpu_usage, data range 1-100 percent
        "ram_usage" : ram_usage, data range 1-100 percent
        "disk_reads" : disk_reads_raw, data range 0 to 2 000 000B?
        "disk_writes" : disk_writes_raw, data range 0 to 2 000 000B?
        "byte_sent" : byte_sent_raw, data range 0 to 10 000 000B?
        "byte_received" : byte_received_raw, data range 0 to 10 000 000B?
'''

def bogus_system_data():
    '''generates testing data to make sure our graphing functions are working'''
    #define random numbers for our metrics we want to measure
    return {
    "cpu_usage" : random.randint(0, 100),
    "ram_usage" : random.randint(0, 100),
    "disk_reads" : random.randint(0, 2000000),
    "disk_writes" : random.randint(0, 200000),
    "byte_sent" : random.randint(0, 10000000),
    "byte_received" : random.randint(0, 10000000)
    }
    

def clear_screen():
    """Clears the screen using ANSI escape sequences"""
    print('\x1b[2J\x1b[H', end="")
    
def update_chart_list(my_data_list, new_value):
    '''updates a list passed to the function by removing the 0-index value and appending the new_value at the end of the list'''
    my_data_list.pop(0)
    my_data_list.append(new_value)

def ascii_graphing(graph_object1, graph_object2, graph_object3):
    '''prints a row of 3 asciiplotpy graphs, side by side, accepts a list of text strings to print on screen'''
    
    chart_width = 25 #sets maximum length of each printed row of charts
    
    #pad each line to the total chart_width value
    padded_graph_object1 = [line.ljust(chart_width) for line in graph_object1]
    padded_graph_object2 = [line.ljust(chart_width) for line in graph_object2]
    padded_graph_object3 = [line.ljust(chart_width) for line in graph_object3]
    
    for line1, line2, line3 in zip(padded_graph_object1, padded_graph_object2, padded_graph_object3):
        print(f"{line1}{line2}{line3}")
        
    print()

def main():
    #initialize lists for each metric we are graphing
    chart_width = 10
    cpu_list = [0] * chart_width
    ram_list = [0] * chart_width
    disk_read_list = [0] * chart_width
    disk_write_list = [0] * chart_width
    net_sent_list = [0] * chart_width
    net_recv_list = [0] * chart_width
    
    #define chart dimensions for graph display
    chart_dimensions_percent = {'height' : 5, 'min' : 0, 'max' : 100, 'offset' : 2}
    chart_dimensions_disk = {'height' : 5, 'min' : 0, 'max' : 20000, 'offset' : 2, 'label_fmt': "{:,.2f}"}
    chart_dimensions_net = {'height' : 5, 'min' : 0, 'max' : 10000, 'offset' :2}
    
    #main program loop
    while True:
        clear_screen()
        my_systemdata = bogus_system_data() #generates bogus data to chart
        #convert byte values for disk and net I/O to megabyte values for graphing
        disk_read_list_con = [value / 1048576 for value in disk_read_list] #MB values
        #print(f"converted disk reads: {disk_read_list_con} Mb") remove this line after debugging
        
        #asciichartpy.plot(a_list) returns a string of text as a plot. We split the lines at the \n character to create lists
        cpu_list_plot = asciichartpy.plot(cpu_list, chart_dimensions_percent).splitlines()
        ram_list_plot = asciichartpy.plot(ram_list, chart_dimensions_percent).splitlines()
        disk_read_plot = asciichartpy.plot(disk_read_list_con, chart_dimensions_disk).splitlines()
        disk_write_plot = asciichartpy.plot(disk_write_list, chart_dimensions_disk).splitlines()
        net_sent_plot = asciichartpy.plot(net_sent_list, chart_dimensions_net).splitlines()
        net_recv_plot = asciichartpy.plot(net_recv_list, chart_dimensions_net).splitlines()
        
        #iterate through the lists with the plotted values to display the graphs side by side
        ascii_graphing(cpu_list_plot, ram_list_plot, disk_read_plot)
        ascii_graphing(disk_write_plot, net_sent_plot, net_recv_plot)
        
        print("CTRL + C to exit")
        
        #update the lists with the latest data
        update_chart_list(cpu_list, my_systemdata['cpu_usage'])
        update_chart_list(ram_list, my_systemdata['ram_usage'])
        update_chart_list(disk_read_list, my_systemdata['disk_reads'])
        update_chart_list(disk_write_list, my_systemdata['disk_writes'])
        update_chart_list(net_sent_list, my_systemdata['byte_sent'])
        update_chart_list(net_recv_list, my_systemdata['byte_received'])
        
        time.sleep(1)

if __name__ == "__main__":
    main()
