#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 08:28:08 2018

@author: (-)
"""

#Connect Four

import itertools
import random

class ConnectBoard():
    
    def __init__(self, dimensions=(6, 8)):
        self.blank = '-'
        self.connect_length = 4
        self.dimensions = dimensions
        self.board = self.reset_board()
        self.gameover = False
        
# Board Manipulation and Queries #
        
    def produce_token(self, player=False):
        return 'X' if (player) else 'O'
    
    def get_token(self, location):
        row, column = location
        return self.board[row][column]
        
    def add_token(self, location, player=False):
        row, column = location
        self.board[row][column] = self.produce_token(player)     
        
    def valid_space(self, location):
        return self.get_token(location) == self.blank
    
    def valid_column(self, column):
        rows, _ = self.dimensions
        return any(self.valid_space((row, column)) for row in range(rows))
        
    def drop_token(self, column, player=False):
        rows, _ = self.dimensions
        span = range(rows - 1, -1, -1)
        for bottom in span:
            location = (bottom, column)
            if self.valid_space(location):
                self.add_token(location, player)
                break

    def get_moves(self, player=False):
        board = self.board
        token = self.produce_token(player)
        moves = []
        for i, row in enumerate(board):
            for j, square in enumerate(row):
                if square == token:
                    move = (i, j)
                    moves.append(move)
        
        return moves
    
    def reset_board(self):
        height, width = self.dimensions
        board = [list(self.blank) * width for row in range(height)]
        return board
    
    def display_board(self):
        
        def display_row(row):
            row_display = ''
            for square in row:
                row_display += '{}|'.format(square)
            return row_display[:-1] + '\n'
        
        board, display = self.board, ''
        _, columns = self.dimensions
        header = ' '.join(map(str, range(columns))) + '\n'
        display += header
        for row in board:
            display += display_row(row)
        print(display)
    
# Pair-Generating Utility Functions #
    
    def pairs(self, locations):
        return zip(locations[:-1], locations[1:])
    
    def delta_type(self, first, second):
        first_x, first_y = first
        second_x, second_y = second
        delta = (first_x - second_x, first_y - second_y)
        return delta
    
    def pair_differences(self, locations):
        deltas = set()
        for pair in self.pairs(locations):
            deltas.add(self.delta_type(*pair))
        return deltas
    
# Win Condition and Sequence Comparison Functions #

    def is_linear(self, locations):
        deltas = self.pair_differences(locations)
        return len(deltas) == 1
    
    def is_adjacent(self, locations):
        deltas = self.pair_differences(locations)
        adjacent_locations = itertools.product(range(-1, 2), range(-1, 2))
        return all(delta in adjacent_locations for delta in deltas)
    
    def meets_win_condition(self, player=False):
        locations = self.get_moves(player)
        combinations = itertools.combinations(locations, self.connect_length)
        for combination in combinations:
            if self.is_linear(combination) and self.is_adjacent(combination):
                self.gameover = True
                break
        else:
            return False
        return True
    
    def full_board(self):
        rows, columns = self.dimensions
        locations = itertools.product(range(rows), range(columns))
        return all(not self.valid_space(entry) for entry in locations)
    
    def check_winner(self, player=False):   
        winner = "Congratulations, you won!"
        loser = "Sorry, you lost."
        tie = "The board is full- nobody wins!"
        message = None
        
        condition = self.meets_win_condition(player)
        
        if condition:
            message = winner if (player) else loser
            
        elif self.full_board():
            message = tie
            
        if message:
            print(message)
        
# Computer Moves
        
    def random_move(self):
        _, columns = self.dimensions
        return random.choice(range(columns))
        
    def computer_move(self):
        move = self.random_move()
        while not self.valid_column(move):
            move = self.random_move()
        return move

# Game Event Loop and Input #

    def initial_state(self):
        self.reset_board()
        self.gameover = False
        
    def input_prompt(self, message=None):
        """Displays a message and accepts a node value to check."""
        _, columns = self.dimensions
        if message is None:
            message = 'Drop a token on the board. '
        options = range(columns)

        try:
            choice = int(input(message))
            if (choice not in options) or (not self.valid_column(choice)):
                raise ValueError
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            error = "Enter a free column. 0 is the far left, 1 is next, etc."
            print(error)
            choice = self.input_prompt()
        return choice
    
    def event_loop(self):
        self.display_board()
        turns = itertools.cycle([True, False])
        while not self.gameover:
            player = next(turns)
            choice = self.input_prompt() if (player) else self.computer_move()
            self.drop_token(choice, player)
            self.display_board()
            self.check_winner(player)
            
    def run(self):
        self.initial_state()
        self.event_loop()
        
testrun = ConnectBoard()
testrun.run()
    