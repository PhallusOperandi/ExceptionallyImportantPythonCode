#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 17:07:09 2018

@author: grantrob
"""

def problem_seven_eight(stream):
    def separate_line(line):
        time, message = line.split(sep='] ')
        processed = time[1:], message
        return processed
        
    def process_line(line):
        time, message = line
        date_length = 11
        hour, minutes = time[date_length:].split(':')
        message = message.split(' ')[1]
        
        return (message, hour, minutes)
    
    def generate_dictionary(lines):
        sleeping_dictionary = {}
        for line in processed:
            message, hour, minutes = line
            if message.startswith('#'):
                number = int(message[1:])
                if number not in sleeping_dictionary:
                    sleeping_dictionary[number] = []
                start = 0 if hour.startswith('23') else int(minutes)
            elif message.startswith('asleep'):
                start = minutes
            elif message.startswith('up'):
                end = minutes
                sleeping_dictionary[number].append((start, end))
    
        return sleeping_dictionary
    
    def expand_ranges(dictionary):
        new_dictionary = {}
        for key, range_list in dictionary.items():
            new_dictionary[key] = []
            for entry in range_list:
                entry = (int(i) for i in entry)
                minutes = [i for i in range(*entry)]
                new_dictionary[key].extend(minutes)
        
        return new_dictionary
        
    def max_sleep_data(dictionary, condition):
        max_guard, max_sleep, max_minute = 0, 0, (0, 0)
        for guard, sleep in dictionary.items():
            total_sleep = len(sleep)
            most_common = max(set(sleep), key=sleep.count) if sleep else 0
            most_common = (sleep.count(most_common), 
                           most_common) if most_common else (0, 0)
            conditions = (total_sleep > max_sleep, 
                          most_common > max_minute)
            if conditions[condition]:
                max_sleep = total_sleep
                max_minute = most_common
                max_guard = guard
        
        return (max_guard, max_sleep, max_minute)
    
    def guard_data_to_solution(guard_data):
        max_guard, _, max_minute = guard_data
        count, minute = max_minute
        return max_guard * minute
                
    data = input_to_list(stream, function=str)
    separated = sorted(separate_line(line) for line in data)
    processed = (process_line(line) for line in separated)
    sleeping_dictionary = generate_dictionary(processed)
    expansions = expand_ranges(sleeping_dictionary)
    condition_7, condition_8 = 0, 1
    guard_7 = max_sleep_data(expansions, condition_7)
    guard_8 = max_sleep_data(expansions, condition_8)
    solutions = (guard_data_to_solution(guard_7),
                 guard_data_to_solution(guard_8))
    return solutions