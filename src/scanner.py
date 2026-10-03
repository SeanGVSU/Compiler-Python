from Tokens import Token, TokenType


class Scanner:

    keywords = {
        "if": TokenType.IF,
        "else": TokenType.ELSE,
        "elif": TokenType.ELIF,
        "for": TokenType.FOR,
        "while": TokenType.WHILE,
        "def": TokenType.DEF,
        "return": TokenType.RETURN,
        "class": TokenType.CLASS,
        "import": TokenType.IMPORT,
        "from": TokenType.FROM,
        "as": TokenType.AS,
        "in": TokenType.IN,
        "is": TokenType.IS,
        "not": TokenType.NOT,
        "and": TokenType.AND,
        "or": TokenType.OR,
        "True": TokenType.TRUE,
        "False": TokenType.FALSE,
        "None": TokenType.NONE,
        "print": TokenType.PRINT
    }

    def __init__(self, file_text):
        self.code = file_text
        self.tokens = []

        self.start = 0
        self.current = 0
        self.line = 1

    def scan_tokens(self):
        while not self.end_of_code():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self):
        c = self.look_at_c()

        # character tokens

        if c == "(":
            self.add_token(TokenType.LEFT_PAREN)
        elif c == ")":
            self.add_token(TokenType.RIGHT_PAREN)
        elif c == "[":
            self.add_token(TokenType.LEFT_BRACKET)
        elif c == "]":
            self.add_token(TokenType.RIGHT_BRACKET)
        elif c == "{":
            self.add_token(TokenType.LEFT_BRACE)
        elif c == "}":
            self.add_token(TokenType.RIGHT_BRACE)
        elif c == ",":
            self.add_token(TokenType.COMMA)
        elif c == ":":
            self.add_token(TokenType.COLON)
        elif c == ".":
            self.add_token(TokenType.DOT)
        elif c == ";":
            self.add_token(TokenType.SEMICOLON)
        elif c == "+":
            self.add_token(TokenType.PLUS)
        elif c == "-":
            self.add_token(TokenType.MINUS)
        elif c == "*":
            self.add_token(TokenType.STAR)
        elif c == "%":
            self.add_token(TokenType.PERCENT)

        elif c == "=":  # Operators
            if self.match("="):
                self.add_token(TokenType.EQUAL_EQUAL)
            else:
                self.add_token(TokenType.EQUAL)
        elif c == "!":
            if self.match("="):
                self.add_token(TokenType.NOT_EQUAL)
            else:
                self.error("Unexpected character '!'")
        elif c == "<":
            if self.match("="):
                self.add_token(TokenType.LESS_EQUAL)
            else:
                self.add_token(TokenType.LESS)
        elif c == ">":
            if self.match("="):
                self.add_token(TokenType.GREATER_EQUAL)
            else:
                self.add_token(TokenType.GREATER)

        elif c == "#": # Python comment
            while self.look_up() != "\n" and not self.end_of_code():
                self.look_at_c()
        elif c == "/":
            self.add_token(TokenType.SLASH)

        elif (c == " ") or (c == "\t") or (c == "\r"): # whitespace
            pass
        elif c == "\n":
            self.line += 1

        elif (c == '"') or (c == "'"): # string
            self.string(c)

        elif c.isdigit(): # number
            self.number()

        elif self.is_alphabet(c): # identifier
            self.identifier()
        else:
            self.error(f"Unexpected character '{c}'")

    def look_at_c(self):
        next_c = self.code[self.current]
        self.current += 1
        return next_c

    def add_token(self, token_type, literal=None):
        text = self.code[self.start:self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def match(self, expected):
        if self.end_of_code():
            return False
        if self.code[self.current] != expected:
            return False

        self.current += 1
        return True

    def look_up(self):
        if self.end_of_code():
            return "\0"

        return self.code[self.current]

    def look_up_next(self):
        if self.current + 1 >= len(self.code):
            return "\0"

        return self.code[self.current + 1]

    def end_of_code(self):
        return self.current >= len(self.code)

    def string(self, quote):
        while (self.look_up() != quote and not self.end_of_code()):
            if self.look_up() == "\n":
                self.line += 1

            self.look_at_c()

        if self.end_of_code():
            self.error("Missing quote")
            return

        # Consume closing quote
        self.look_at_c()
        value = self.code[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING, value)

    def number(self):
        while self.look_up().isdigit():
            self.look_at_c()

        # Decimal number
        if (self.look_up() == "." and self.look_up_next().isdigit()):
            self.look_at_c()
            while self.look_up().isdigit():
                self.look_at_c()

        text = self.code[self.start:self.current]
        self.add_token(TokenType.NUMBER, float(text))

    def identifier(self):
        while self.is_alpha_numeric(self.look_up()):
            self.look_at_c()

        text = self.code[self.start:self.current]
        token_type = self.keywords.get(text, TokenType.IDENTIFIER)
        self.add_token(token_type)

    def is_alphabet(self, c):
        return (c.isalpha() or c == "_")

    def is_alpha_numeric(self, c):
        return (self.is_alphabet(c) or c.isdigit())

    def error(self, message):
        print(f"[line {self.line}] Error: {message}")