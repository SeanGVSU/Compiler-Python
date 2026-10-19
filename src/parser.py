from Tokens import TokenType
from ast_printer import Literal, Grouping, Unary, Binary


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        expression = self.expression()
        if not self.check(TokenType.EOF):
            token = self.peek()
            raise self.error(token,f"Unexpected trailing token '{token.lexeme}'.")
        return expression

    def expression(self):
        return self.equality()

    def equality(self):
        expression = self.comparison()
        while self.match(TokenType.EQUAL_EQUAL, TokenType.NOT_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expression = Binary(expression, operator, right)
        return expression

    def comparison(self):
        expression = self.term()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expression = Binary(expression, operator, right)
        return expression

    def term(self):
        expression = self.factor()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous()
            right = self.factor()
            expression = Binary(expression, operator, right)
        return expression

    def factor(self):
        expression = self.unary()
        while self.match(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            operator = self.previous()
            right = self.unary()
            expression = Binary(expression, operator, right)
        return expression

    def unary(self):
        if self.match(TokenType.MINUS, TokenType.BANG, TokenType.NOT):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.primary()

    def primary(self):
        if self.match(TokenType.NUMBER):
            return Literal(self.previous().literal)

        if self.match(TokenType.STRING):
            return Literal(self.previous().literal)

        if self.match(TokenType.TRUE):
            return Literal(True)

        if self.match(TokenType.FALSE):
            return Literal(False)

        if self.match(TokenType.NONE):
            return Literal(None)

        if self.match(TokenType.LEFT_PAREN):
            expression = self.expression()
            self.consume(TokenType.RIGHT_PAREN,"Expected ')' after expression.")
            return Grouping(expression)
        raise self.error(self.peek(), "Expected expression.")

    # Helpers
    def match(self, *token_types):
        for token_type in token_types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def consume(self, token_type, message):
        if self.check(token_type):
            return self.advance()
        raise self.error(self.peek(), message)

    def check(self, token_type):
        if self.is_at_end():
            return token_type == TokenType.EOF
        return self.peek().type == token_type

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self):
        return self.peek().type == TokenType.EOF

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def error(self, token, message):
        if token.type == TokenType.EOF:
            location = "at end"
        else:
            location = f"at '{token.lexeme}'"
        return ParseError(f"[line {token.line}] Syntax error {location}: {message}")

class ParseError(Exception):
    pass