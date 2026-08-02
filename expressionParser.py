from enum import Enum, auto
from typing import Any, override
import abc
import numpy as np
import math
import plotting

class nodeType(Enum):
    number = auto()
    plus = auto()
    minus = auto()
    times = auto()
    divided = auto() 
    openParenthesis = auto()
    closedParenthesis = auto()
    identifier = auto()
    sin = auto()
    cos = auto()

def isDigit(c) ->bool:
    return c >= '0' and c <= '9'

class Tokenizer():
    singleCharTypes = {
        '+' : nodeType.plus,
        '-' : nodeType.minus,
        '*' : nodeType.times,
        '/' : nodeType.divided,
        '(': nodeType.openParenthesis,
        ')': nodeType.closedParenthesis,
        't': nodeType.identifier
    }

    def __init__(self, input : str):
        self.input = input
        self.current = 0
        self.tokens = []

    def getCurrentChar(self)->str:
        if self.current < len(self.input):
            return self.input[self.current]
        return ''

    def advance(self):
        self.current += 1

    def processNumber(self):
        c = self.getCurrentChar()
        currentDigit = ''

        while isDigit(c):
            currentDigit += c
            self.advance()
            c = self.getCurrentChar()

        if c == '.':
            currentDigit += c
            self.advance()
            c = self.getCurrentChar()

        while isDigit(c):
            currentDigit += c
            self.advance()
            c = self.getCurrentChar()
        self.tokens.append((nodeType.number,currentDigit))

    def processSin(self):
        self.advance()
        if self.getCurrentChar() == 'i':
            self.advance()
            if self.getCurrentChar() == 'n':
                self.advance()
                self.tokens.append((nodeType.sin,"sin"))

    def processCos(self):
        self.advance()
        if self.getCurrentChar() == 'o':
            self.advance()
            if self.getCurrentChar() == 's':
                self.advance()
                self.tokens.append((nodeType.cos,"cos"))

    def processFunctions(self):
        c = self.getCurrentChar()
        if c == 's':
            self.processSin()
        elif c == 'c':
            self.processCos()

    def tokenize(self)->list[tuple[nodeType,Any]]:
        self.tokens = []
        while self.current <len(self.input):
            c = self.getCurrentChar()
            if c in Tokenizer.singleCharTypes:
                self.tokens.append((Tokenizer.singleCharTypes[c],c))
                self.advance()

            elif isDigit(c):
                self.processNumber()
            else:
                self.processFunctions()

        return self.tokens

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

class Identifier(Expression):
    def __init__(self):
        self.values = np.linspace(0, 5, 1000)
        self.current = 0
        
    @override
    def evaluate(self):
        if self.current < len(self.values):
            value = self.values[self.current]
            self.current +=1
            return value
        return -1
        
class Parenthesized(Expression):
    def __init__(self, value):
        self.value = value

    @override
    def evaluate(self):
        return self.value.evaluate()

class Sin(Expression):
    def __init__(self, value):
        self.value = value

    @override
    def evaluate(self):
        return math.sin(self.value.evaluate())

class Cos(Expression):
    def __init__(self, value):
        self.value = value

    @override
    def evaluate(self):
        return math.cos(self.value.evaluate())

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

        while self.match([nodeType.plus,nodeType.minus]):
            operator = self.previous()
            right = self.factor()
            expr = BinaryOperation(expr, operator, right)

        return expr

    def factor(self)->Expression:
        expr = self.primary()

        while self.match([nodeType.times,nodeType.divided]):
            operator = self.previous()
            right = self.primary()
            expr = BinaryOperation(expr, operator, right)

        return expr

    def primary(self)->Expression:
        if self.match([nodeType.number]):
            return Number(float(self.previous()[1]))
        if self.match([nodeType.identifier]):
            return Identifier()
        if self.match([nodeType.openParenthesis]):
            expr = self.expression()
            self.consume(nodeType.closedParenthesis, "Expected ')' after expression.");
            return Parenthesized(expr)
        if self.match([nodeType.sin]):
            self.consume(nodeType.openParenthesis, "Expected '(' after expression")
            expr = self.expression()
            self.consume(nodeType.closedParenthesis, "Expected ')' after expression")
            return Sin(expr)
        if self.match([nodeType.cos]):
            self.consume(nodeType.openParenthesis, "Expected '(' after expression")
            expr = self.expression()
            self.consume(nodeType.closedParenthesis, "Expected ')' after expression")
            return Cos(expr)


def parseEquation(input : str):
    tokenizer = Tokenizer(input)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    tree = parser.parse()
    #can add a function that takes the range of the identifier as input, traverses the whole tree, finds the identifier nodes and sets the range
    values = []
    x = []
    for i in range(1000):
        x.append(i)
        values.append(tree.evaluate())

    plotting.plot(x, values)


if __name__ == "__main__":
    parseEquation("3*cos(3*t)")