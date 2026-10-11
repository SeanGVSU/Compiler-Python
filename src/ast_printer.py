from Tokens import TokenType
import Tokens

class Literal:
    def __init__(self, value):
        self.value = value

class Grouping:
    def __init__(self, expression):
        self.expression = expression

class Unary:
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

class Binary:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class AstPrinter:
    def print_expr(self, expression):
        if isinstance(expression, Literal):
            if expression.value is None:
                return "nil"
            if expression.value is True:
                return "true"
            if expression.value is False:
                return "false"

            return str(expression.value)

        elif isinstance(expression, Grouping):
            return "(group " + self.print_expr(expression.expression) + ")"

        elif isinstance(expression, Unary):
            if expression.operator.type not in (TokenType.MINUS, TokenType.BANG, TokenType.NOT):
                raise ValueError("Invalid unary operator: " + expression.operator.lexeme)

            return "(" + expression.operator.lexeme + " " + self.print_expr(expression.right) + ")"

        elif isinstance(expression, Binary):
            if expression.operator.type not in (
                TokenType.PLUS,
                TokenType.MINUS,
                TokenType.STAR,
                TokenType.SLASH,
                TokenType.PERCENT,
                TokenType.EQUAL_EQUAL,
                TokenType.NOT_EQUAL,
                TokenType.LESS,
                TokenType.LESS_EQUAL,
                TokenType.GREATER,
                TokenType.GREATER_EQUAL
            ):
                raise ValueError("Invalid binary operator: " + expression.operator.lexeme)
            return "(" + expression.operator.lexeme + " " + self.print_expr(expression.left) + " " + self.print_expr(expression.right) + ")"


def make_token(token_type, lexeme):
    return Tokens.Token(token_type, lexeme, None, 1)


#plus = make_token(TokenType.PLUS, "+")
#expression = Binary(Literal(1), plus, Literal(2))
#print(AstPrinter().print_expr(expression))         
# expected (+ 1 2)

#minus = make_token(TokenType.MINUS, "-")
#expression = Unary(minus, Literal(5))
#print(AstPrinter().print_expr(expression))         
# expected (- 5)

#bang = make_token(TokenType.BANG, "!")
#expression = Unary(bang, Literal(False))
#print(AstPrinter().print_expr(expression))         
# expected (! false)