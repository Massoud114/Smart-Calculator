variables = dict()

def sign_format(get_string):
    if get_string.count("+") >= 1:
        return "+"
    elif get_string == '-' or get_string.count("-") > 2:
        return "-"
    elif get_string.count("-") == 2:
        return "+"
    else:
        return get_string



def affect(operation):
    global variables
    if operation[1] in variables.keys():
        variables[operation[0]] = variables[operation[1]]
    elif operation[1].isdigit():
        variables[operation[0]] = operation[1]


def error_check(input_array):
    for i in input_array[0]:
        if i.isdigit():
            return "Invalid identifier"
    if not input_array[1].isdigit():
        for i in input_array[1]:
            if i.isdigit():
                return "Invalid assignment"
        else:
            if not input_array[1] in variables.keys():
                return "Unknown variable"
            else:
                return "Ok"
    else:
        return "Ok"

def to_postfix(infix):
    stack = []
    postfix = []
    prec = {'^': 5, '*': 4, '/': 4, '+': 3, '-': 3, '(': 2, ')': 1}
    for i in infix:
        if i == "(":
            stack.append(i)
        elif i == ")":
            next = stack.pop()
            while next != "(":
                postfix.append(next)
                next = stack.pop()
        elif i.isdigit():
            postfix.append(i)
        elif i in "+-*/":
            p = prec[i]
            while len(stack) != 0 and p <= prec[stack[-1]]:
                postfix.append(stack.pop())
            stack.append(i)
    while len(stack) > 0:
        postfix.append(stack.pop())
    return postfix

def postfix_to_result(postfix):
    stack = []
    for i in postfix:
        if i.isdigit():
            stack.append(int(i))
        elif i in "+-*/":
            n1 = int(stack.pop())
            n2 = int(stack.pop())
            if i == '+':
                stack.append(n2 + n1)
            if i == '-':
                stack.append(n2 - n1)
            if i == '*':
                stack.append(n2 * n1)
            if i == '/':
                try:
                    stack.append(int(n2 / n1))
                except ZeroDivisionError:
                    return "Invalid expression"
            if i == '^':
                stack.append(n2 ** n1)
    return stack.pop()


while True:
    result = 0
    action = input().strip()
    if action == "":
        continue
    if action[0] == "/":
        if action == "/exit":
            print("Bye!")
            break
        elif action == "/help":
            print("The program calculates the sum of numbers")
        else:
            print("Unknown command")
            continue
    else:
        if action.__contains__("="):
            if action.count("=") > 1:
                print("Invalid assignment")
                continue
            else:
                user_input = action.split("=")
                for i in range(len(user_input)):
                    user_input[i] = user_input[i].strip()
                if len(user_input) < 2:
                    print("Invalid assignment")
                    continue
                if error_check(user_input) != "Ok":
                    print(error_check(user_input))
                    continue
                else:
                    affect(user_input)
        else:
            user_input = action
            operation = []
            i = 0
            while i < len(user_input):
                if user_input[i].isalnum():
                    number = user_input[i]
                    while i + 1 < len(user_input):
                        if user_input[i + 1].isalnum():
                            number += user_input[i + 1]
                            i += 1
                        else:
                            break
                    operation.append(number)
                elif user_input[i] in '+*/^':
                    number = user_input[i]
                    while i + 1 < len(user_input):
                        if user_input[i + 1] == user_input[i]:
                            number += user_input[i + 1]
                            i += 1
                        else:
                            break
                    operation.append(number)
                elif user_input[i] == "-":
                    number = user_input[i]
                    while i + 1 < len(user_input):
                        if user_input[i + 1].isdigit():
                            number += user_input[i + 1]
                            i += 1
                        elif user_input[i + 1] == user_input[i]:
                            number += user_input[i + 1]
                            i += 1
                        else:
                            break
                    operation.append(number)
                elif user_input[i] in '()':
                    operation.append(user_input[i])
                i += 1
            n_sign = 0
            n_operand = 0
            for i in range(len(operation)):
                operation[i] = sign_format(operation[i])
                if operation[i].lstrip('-').isalnum():
                    n_operand += 1
                elif operation[i] in "+-*/^":
                    n_sign += 1
            if operation.count('(') != operation.count(')') or n_operand != n_sign + 1:
                print("Invalid expression")
                continue
            for i in operation:
                if i.count('*') > 1 or i.count('/') > 1:
                    print("Invalid expression")
            for i in range(len(operation)):
                if operation[i].isalpha():
                    if operation[i] in variables.keys():
                        operation[i] = variables[operation[i]]
                    else:
                        print("Unknown variable")
                        continue
            if len(operation) == 1:
                print(operation[0])
            else:
                print(postfix_to_result(to_postfix(operation)))
