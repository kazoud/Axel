from enum import Enum
from typing import Any, override
import abc

class nodeType(Enum):
    number = 1
    additionSubtraction = 2
    multiplicationDivision = 3
    openParenthesis = 4
    closedParenthesis = 5
    
def tokenize(input: str)->list[tuple[nodeType,Any]]:
    types = {
        '+' : nodeType.additionSubtraction,
        '-' : nodeType.additionSubtraction,
        '*' : nodeType.multiplicationDivision,
        '/' : nodeType.multiplicationDivision,
        '(': nodeType.openParenthesis,
        ')': nodeType.closedParenthesis
    }

    tokens = []
    currentString = ''
    isPartofANumber = False
    i = 0
    while i <len(input):
        c = input[i]
        if (c >= '0' and c <= '9') or (currentString != '' and c == '.'): #if character is part of a decimal number
            currentString += c
            isPartofANumber = True
            if (i == len(input)-1):
                tokens.append((nodeType.number,currentString))
        else:
            if isPartofANumber:
                tokens.append((nodeType.number,currentString))
                currentString = ''
                isPartofANumber = False
            tokens.append((types[c],c))
            currentString = ''
        i+=1

    return tokens

class Expression(abc.ABC):
    @abc.abstractmethod
    def evaluate(self):
        pass

class BinaryOperation(Expression):
    def __init__(self, left : Expression, op: str, right : Expression):
        self.left = left
        self.op = op
        self.right = right

    @override
    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        match self.op[1]:
            case '+':
                return left + right
            case '-':
                return left - right
            case '*':
                return left * right
            case '/':
                return left / right

        return None

class Number(Expression):
    def __init__(self, value : float):
        self.value = value

    @override
    def evaluate(self):
        return self.value

class Parenthesized(Expression):
    def __init__(self, value):
        self.value = value

    @override
    def evaluate(self):
        return self.value.evaluate()

class Parser:
    def __init__(self, tokens: list[tuple[nodeType, str]]):
        self.tokens = tokens
        self.current = 0

    def endOfInput(self)->bool:
        return self.current >= len(self.tokens)
    
    def advanceCurrentToken(self):
        if not self.endOfInput():
            self.current += 1

    def peek(self) -> tuple[nodeType,str]:
        return self.tokens[self.current]
    
    def previous(self) ->tuple[nodeType, str]:
        return self.tokens[self.current-1]

    def check(self, type: nodeType)->bool:
        if self.endOfInput():
            return False
        return self.peek()[0] == type

    def match(self, types: list[nodeType])->bool:
        for type in types:
            if self.check(type):
                self.advanceCurrentToken()
                return True
        return False

    def consume(self, type: nodeType, message: str):
        if self.check(type):
            self.advanceCurrentToken()
        else:
            print(message)

    def parse(self)->Expression:
        return self.expression()

    def expression(self) ->Expression:
        expr = self.factor()

        while self.match([nodeType.additionSubtraction]):
            operator = self.previous()
            right = self.factor()
            expr = BinaryOperation(expr, operator, right)

        return expr

    def factor(self)->Expression:
        expr = self.primary()

        while self.match([nodeType.multiplicationDivision]):
            operator = self.previous()
            right = self.primary()
            expr = BinaryOperation(expr, operator, right)

        return expr

    def primary(self)->Expression:
        if self.match([nodeType.number]):
            return Number(float(self.previous()[1]))
        if self.match([nodeType.openParenthesis]):
            expr = self.expression()
            self.consume(nodeType.closedParenthesis, "Expect ')' after expression.");
            return Parenthesized(expr)

def parseEquation(input : str):
    tokens = tokenize(input)
    parser = Parser(tokens)
    tree = parser.parse()
    return tree.evaluate()

if __name__ == "__main__":
    print(parseEquation("2*(10+3)*5"))