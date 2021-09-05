import re

from Variable import Variable, VariableType, VarUses
from constant import VARIABLE_DECLARATION_REGEX, VARIABLE_USED, EXPRESSION_PATTERN, REPLACE_EXPRESSION_PATTERN
from collections import Counter

from exp import ExpressionLine
import random
import string


class Analyzer:

    def __init__(self, code: []):
        self.code = code
        self.variable_list = []
        self.unused_variable = []
        self.used_variable = []
        self.new_code = []
        self.expression = []
        self.expression_line = []
        self.duplicated_expression = []

    def analyze(self):
        self.__get_variable()
        print("#################################")
        print("Variable in code:")
        for variable in self.variable_list:
            print("Variable {0}, type: {1}, value: {2}, line: {3}".format(variable.name, variable.type, variable.value,
                                                                          variable.declaration))
        self.__find_unused_variable()
        print("#################################")
        if len(self.unused_variable) != 0:
            print("We find unused variable in your code.")
            for variable in self.unused_variable:
                print("{0} variable in line {1}".format(variable.name, variable.declaration))
        print("#################################")
        if len(self.used_variable) != 0:
            print("We find used variable: ")
            for variable in self.used_variable:
                print("{0} variable in line {1}".format(variable.name, variable.uses))
        self.__find_expression()
        print("#################################")
        if len(self.expression) != 0:
            print("We find expression: ")
            for expr in self.expression:
                print(expr)
        self.__find_duplicate_expression()

    def fix(self):
        self.new_code = self.code
        self.__remove_unused_variable()
        self.__fix_duplicate_expression()
        self.__save_new_code()

    def __remove_unused_variable(self):
        for unused in self.unused_variable:
            self.new_code[unused.declaration] = ""

    def __save_new_code(self):
        file = open("example/ref_code.c", "w+")
        for code in self.new_code:
            file.write(code)
        file.close()

    def __get_variable(self):
        line_number = 0
        for line in self.code:
            result = re.findall(VARIABLE_DECLARATION_REGEX, line)
            if len(result) != 0:
                self.variable_list.append(Variable(result[0][1], VariableType(result[0][0]), result[0][4], line_number))
            line_number = line_number + 1

    def __find_unused_variable(self):
        for variable in self.variable_list:
            find = 0
            line_counter = variable.declaration + 1
            for line in self.code[(variable.declaration + 1):]:
                result = re.findall(VARIABLE_USED.format(variable.name), line)
                if len(result) != 0:
                    new_var = Variable(variable.name, variable.type, variable.value, variable.declaration)
                    new_var.add_uses(VarUses(line_counter))
                    self.used_variable.append(new_var)
                    find = 1
                line_counter = line_counter + 1
            if find == 0:
                self.unused_variable.append(variable)

    def __find_expression(self):
        line_counter = 0
        for line in self.code:
            result = re.search(EXPRESSION_PATTERN, line)
            if result is not None:
                expresion = result.group().split('=')[1].replace(' ', '')
                self.expression.append(expresion)
                self.expression_line.append(ExpressionLine(expresion, line_counter))
            line_counter = line_counter + 1

    def __find_duplicate_expression(self):
        duplicated = Counter(self.expression) - Counter(set(self.expression))
        self.duplicated_expression = list(duplicated.keys())

    def __fix_duplicate_expression(self):
        for exp in self.duplicated_expression:
            test_code = self.new_code[:]
            exp_name = self.__generate_random_string()
            exp_line = self.__get_expression_line(exp)
            test_code = test_code[:exp_line] + ['int ' + exp_name + ' = ' + exp + ';\n'] + test_code[exp_line:]
            self.new_code = test_code[:]
            self.__replace_duplicate_expression(exp_line + 1, exp, exp_name)

    def __replace_duplicate_expression(self, line, exp, variable):
        line_counter = line
        for code in self.new_code[line:]:
            result = re.search(REPLACE_EXPRESSION_PATTERN, code)
            if result is not None:
                parts_result = result.group().split('=')
                result_name = parts_result[0]
                result_value = parts_result[1]

                clear_result_value = result_value.replace(' ', '').replace('\n', '')
                if exp == clear_result_value:
                    self.new_code[line_counter] = result_name + " = " + variable + "; \n"
            line_counter = line_counter + 1

    def __generate_random_string(self):
        letters = string.ascii_uppercase
        return ''.join(random.choice(letters) for i in range(10))

    def __get_expression_line(self, expression):
        for exp in self.expression_line:
            if exp.expression == expression:
                return exp.line
