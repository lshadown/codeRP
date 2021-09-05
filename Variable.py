from enum import Enum


class VariableType(Enum):
    INT = "int"
    DOUBLE = "double"
    STRING = "string"


class VarUses:
    def __init__(self, line):
        self.line = line


class Variable:
    def __init__(self, name, variable_type: VariableType, value, declaration):
        self.name = name
        self.type = variable_type
        self.value = value
        self.declaration = declaration
        self.uses = []

    def add_uses(self, use: VarUses):
        self.uses.append(use)
