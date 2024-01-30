from sys import argv
from enum import Enum

argc = len(argv)
repl = False
expr = ""

if argc < 2:
    repl = True
    print("REPL mode is under construction.")
    exit(1)
elif argc == 2:
    expr = argv[1]
elif argc == 3:
    assert argv[1] == "-f"
    try:
        f = open(argv[2], "r")
        expr = f.read()
        f.close()
    except FileNotFoundError:
        print(f"error: file {argv[2]} does not exist")


class TokenKind(Enum):
    TOKEN_EOF = 0
    TOKEN_PLUS = 1
    TOKEN_MINUS = 2
    TOKEN_MUL = 3
    TOKEN_DIV = 4
    TOKEN_POW = 5
    TOKEN_INT = 6
    TOKEN_FLOAT = 7
    TOKEN_PRINT = 8
    TOKEN_IDENT = 9
    TOKEN_DUP = 10
    TOKEN_ILLEGAL = 11


class Token:
    def __init__(self):
        self.kind = 0
        self.literal = ""


class Lexer:
    def __init__(self, expr):
        self.expr = expr
        self.pos = 0
        self.read_pos = 0
        self.ch = ""
        self.read_ch()

    def read_ch(self):
        if self.read_pos >= len(self.expr):
            self.ch = ""
        else:
            self.ch = self.expr[self.read_pos]

        self.pos = self.read_pos
        self.read_pos += 1

    def read_tokens(self):
        tok = Token()
        is_float = False

        while self.ch.isspace():
            self.read_ch()

        if self.ch.isdigit():
            num = ""

            while self.ch.isdigit():
                num += self.ch
                self.read_ch()

            if self.ch == ".":
                is_float = True
                num += self.ch
                self.read_ch()

                while self.ch.isdigit():
                    num += self.ch
                    self.read_ch()

            tok.kind = TokenKind.TOKEN_FLOAT if is_float\
                else TokenKind.TOKEN_INT
            tok.literal = num

        if self.ch.isalpha():
            ident = ""

            while self.ch.isalpha():
                ident += self.ch
                self.read_ch()

            tok.kind = TokenKind.TOKEN_IDENT
            if ident != "dup":
                tok.kind = TokenKind.TOKEN_ILLEGAL
            else:
                tok.kind = TokenKind.TOKEN_DUP

            tok.literal = ident

        match self.ch:
            case '+': tok.kind = TokenKind.TOKEN_PLUS; tok.literal = "+"
            case '-': tok.kind = TokenKind.TOKEN_MINUS; tok.literal = "-"
            case '*': tok.kind = TokenKind.TOKEN_MUL; tok.literal = "*"
            case '/': tok.kind = TokenKind.TOKEN_DIV; tok.literal = "/"
            case '^': tok.kind = TokenKind.TOKEN_POW; tok.literal = "^"
            case '.': tok.kind = TokenKind.TOKEN_PRINT; tok.literal = "."
            case '':  tok.kind = TokenKind.TOKEN_EOF; tok.literal = ""

        self.read_ch()
        return tok


stack = []
def evaluate(tokens):
    for tok in tokens:
        match tok.kind:
            case TokenKind.TOKEN_INT: stack.append(int(tok.literal))
            case TokenKind.TOKEN_FLOAT: stack.append(float(tok.literal))
            case TokenKind.TOKEN_PLUS:
                if len(stack) < 2:
                    print("error: operator '+' requires two numerical arguments")
                    return

                n2, n1 = stack.pop(), stack.pop()
                stack.append(n1 + n2)
            case TokenKind.TOKEN_MINUS:
                if len(stack) < 2:
                    print("error: operator '-' requires two numerical arguments")
                    return

                n2, n1 = stack.pop(), stack.pop()
                stack.append(n1 - n2)
            case TokenKind.TOKEN_MUL:
                if len(stack) < 2:
                    print("error: operator '*' requires two numerical arguments")
                    return

                n2, n1 = stack.pop(), stack.pop()
                stack.append(n1*n2)
            case TokenKind.TOKEN_DIV:
                if len(stack) < 2:
                    print("error: operator '/' requires two numerical arguments")
                    return

                n2, n1 = stack.pop(), stack.pop()
                if n2 == 0:
                   print("error: cannot divide by 0")
                   return

                stack.append(n1/n2)
            case TokenKind.TOKEN_POW:
                if len(stack) < 2:
                    print("error: operator '^' requires two numerical arguments")
                    return

                n2, n1 = stack.pop(), stack.pop()
                if n2 == 0 and n1 == 0:
                    print("error: 0^0 is undefined")
                    return

                stack.append(n1**n2)
            case TokenKind.TOKEN_PRINT:
                if len(stack) > 0:
                    print(stack[len(stack) - 1])
                    stack.pop()
            case TokenKind.TOKEN_DUP:
                if len(stack) <= 0:
                    print("error: one parameter is needed for dup")
                    return

                stack.append(stack[len(stack) - 1])
            case TokenKind.TOKEN_ILLEGAL:
                print(f"Got illegal token: {tok.literal}")


tokens = []

def functionality(e: str):
    lexer = Lexer(e)

    while tok := lexer.read_tokens():
        if tok.kind == TokenKind.TOKEN_EOF:
            break
        #print((tok.kind, tok.literal))
        tokens.append(tok)

    evaluate(tokens)

if repl:
    print("Entering repl mode...")
while repl:
    try:
        expr = input(">> ")
        print(expr, stack)
        functionality(expr)
    except (KeyboardInterrupt, EOFError) as e:
        print("\nGoodbye")
        exit(1)
else:
    functionality(expr)
