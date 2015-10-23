import os
import sys
import string
import ConfigParser

def get_performtraversals_time_list(app_name,minimum_time,start_time,end_time):
    time_list = []
    child_func_number = 0
    TIME_INDEX = 3
    current_time = 0
    for line in open(app_name + '_process_trace.txt'):
        items = line.split()
        if len(items) == 1:
            start_time += float(items[0])
            end_time += float(items[0])
            continue
        time = float(items[TIME_INDEX].strip(':'))
        last_item = items[-1]
        if ': B' in line:
            if 'performTraversals' in last_item:
                current_time = time
            else:
                child_func_number += 1
        elif ': E' in line:
            if child_func_number == 0:
                delta_time = time - current_time
                time_tuple = (current_time,delta_time)
                if delta_time >= minimum_time and current_time >= start_time and current_time <= end_time:
                    time_list.append(time_tuple)
            else:
                child_func_number -= 1
        #else:
        #    print last_item
    return time_list


def write_performtraversals_time_file(time_list,app_name,minimum_time,delta_time):
    time_file = file(app_name + '_performtraversals_' + str(int(minimum_time*1000)) +'.txt','w')
    for items in time_list:
        time_file.write(str(items[0]) + '\t' + str(items[1]) + '\n')
    total_number = len(time_list)
    frequency = total_number * 1.0 / delta_time
    time_file.write('Total:\t' + str(len(time_list)) + '\n')
    time_file.write('Frequency:\t' + str(frequency) + '\n')

def read_configs_and_run():
    config = ConfigParser.ConfigParser()
    config.readfp(open('performtraversals_config.ini'))
    app_name = config.get('Test object','app_name')    
    minimum_time = float(config.get('Time','minimum_time'))
    start_time = float(config.get('Time','start_time'))
    end_time = float(config.get('Time','end_time'))
    #travert unit to 's'
    minimum_time /= 1000
    #TODO get start_time and end_time
    time_list = get_performtraversals_time_list(app_name,minimum_time,start_time,end_time)
    write_performtraversals_time_file(time_list,app_name,minimum_time,end_time - start_time)

if __name__ == '__main__':
    read_configs_and_run()
