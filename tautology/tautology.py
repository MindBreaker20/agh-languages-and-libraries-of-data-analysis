'''
Author: Bartłomiej Jamiołkowski
Date: 23.12.2022
Topic: Check if an expression is a tautology
'''

import pandas as pd
from re import findall
from itertools import product

connectivity = {'(': 7, ')': 7, '~': 6, '^': 5, '&': 4, '|': 3, '>': 2}


def truth_table_generator(expr):  # generating dataframe representing truth table
    logical_variables = list(set(findall('[a-z]', expr)))  # unique logical variables found in expression
    truth_value_combinations = list(product([1, 0], repeat=len(logical_variables)))
    truth_table = pd.DataFrame(truth_value_combinations, columns=logical_variables)
    return truth_table


def prioritize(expr):  # converting symbols in expression into numbers representing priority
    converted_expression = []

    for symbol in expr:
        if symbol.isalpha():  # Checking whether symbol is logical variable or not
            converted_expression.append(symbol)
        else:
            if symbol == '(':
                converted_expression.append(connectivity.get('('))
                connectivity['('] = connectivity.get('(') + 1  # In case of nested brackets a priority is increased
                connectivity[')'] = connectivity.get(')') + 1
            elif symbol == ')':
                connectivity['('] = connectivity.get('(') - 1   # In case of repeated brackets previously increased
                connectivity[')'] = connectivity.get(')') - 1   # priority is decreased
                converted_expression.append(connectivity.get(')'))
            else:
                converted_expression.append(connectivity.get(symbol))  # converting other symbols without logical var

    return converted_expression


def get_bracket_indexes(expr, m):  # searching indexes for given modified expression and max priority
    indexes = []

    for i in range(len(expr)):
        if expr[i] == m:
            indexes.append(i)
    return indexes[0], indexes[1]


def check_logical_value(sub_expr, idx, p):  # obtaining results of logical operators
    logical_combinations = {2: [1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1], 3: [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0],
                            4: [1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0], 5: [1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0]}

    sub_expr = list(sub_expr)
    logical_values = logical_combinations.get(p)  # getting values of logical variables and results of operations

    if sub_expr[idx - 1] == logical_values[0] and sub_expr[idx + 1] == logical_values[1]:
        sub_expr[idx - 1] = logical_values[2]  # left logical variable is replaced with result of operation
    elif sub_expr[idx - 1] == logical_values[3] and sub_expr[idx + 1] == logical_values[4]:
        sub_expr[idx - 1] = logical_values[5]
    elif sub_expr[idx - 1] == logical_values[6] and sub_expr[idx + 1] == logical_values[7]:
        sub_expr[idx - 1] = logical_values[8]
    elif sub_expr[idx - 1] == logical_values[9] and sub_expr[idx + 1] == logical_values[10]:
        sub_expr[idx - 1] = logical_values[11]

    sub_expr.pop(idx)  # converted logical symbol and right converted logical variable are removed from list
    sub_expr.pop(idx)

    return sub_expr


def calculate_logic_value(sub_expr):
    priority = 6  # subexpression contains brackets no more
    sub_expr = list(sub_expr)

    while priority != 1:

        if priority in sub_expr:  # checking if priority exists in subexpression
            idx = sub_expr.index(priority)
            if priority == 6:  # checking if negation occurs in subexpression
                if sub_expr[idx + 1] == 1:  # number after negation is logical variable with true or false value
                    sub_expr[idx] = 0  # converted symbol of negation is replaced with logical value
                    sub_expr.pop(idx + 1)  # used logical value is removed from list of elements of subexpression
                elif sub_expr[idx + 1] == 0:
                    sub_expr[idx] = 1
                    sub_expr.pop(idx + 1)
            elif priority in range(2, 6):
                sub_expr = check_logical_value(sub_expr, idx, priority)
        else:
            priority -= 1

    return sub_expr


def tautology(expr):  # checking if expression is tautology or not
    truth_table = truth_table_generator(expr)
    truth_table_combinations = dict(truth_table.to_dict(orient='index'))
    truth_table[expr] = 0  # creating column of zeros in order to store every output

    for key, value in truth_table_combinations.items():  # keys are rows in dataframe whereas values are dictionaries
        combinations_dict = dict(value)
        converted_expression = prioritize(expr)

        for i in range(0, len(converted_expression)):  # setting logical variables values for current combination
            if converted_expression[i] in combinations_dict:
                converted_expression[i] = combinations_dict.get(converted_expression[i])

        while True:
            max_priority = max(converted_expression)

            if max_priority >= 7:  # Checking if there are left brackets
                start_idx, end_idx = get_bracket_indexes(converted_expression, max_priority)
                subexpression = converted_expression[start_idx + 1:end_idx]  # slicing list by indexes
                logical_value = calculate_logic_value(subexpression)  # logical value of subexpression
                converted_expression = converted_expression[:start_idx] + logical_value + converted_expression[end_idx + 1:]
            else:  # when there are no more brackets
                converted_expression = calculate_logic_value(converted_expression)
                break

        if converted_expression[0] == 1:  # on the end of iteration there is only single element list
            truth_table.at[key, expr] = 1  # result of every simulation is written to dataframe
        elif converted_expression[0] == 0:
            truth_table.at[key, expr] = 0

    if (truth_table[expr] == 1).all():  # checking whether all simulations gave positive results or not
        print('Expression is tatutology')
    else:
        print('Expression is not tatutology')

    print(truth_table)


if __name__ == "__main__":
    while True:
        expression = input("Enter expression: ")
        if expression == "":
            break
        tautology(expression)


'''
Examples of expressions which are tautologies:
'((p>q)&p)>q'
'(p>q)|(q>p)'
'((p|q)&(p>r)&(q>r))>r'
Examples of expressions which are not tautologies:
'p>((~p)|q)'
'~(p>q)|~(q>p)'
'''