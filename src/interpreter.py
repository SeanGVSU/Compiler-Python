from ast_printer import Literal, Grouping, Unary, Binary, Expression, Print
from Tokens import TokenType



class Interpreter:

    def interpret(self, statements):
        for statement in statements:
            try:
                self.execute(statement)
            except RuntimeError as error:
                print(f"Runtime error: {error}")

    def execute(self, statement):
        if isinstance(statement, Print):
            value = self.evaluate(statement.expression)
            print(value)
        elif isinstance(statement, Expression):
            self.evaluate(statement.expression)

    def evaluate(self, expression):
        if isinstance(expression, Literal):
            if isinstance(expression.value, bool):
                return int(expression.value)
            return expression.value

        if isinstance(expression, Grouping):
            return self.evaluate(expression.expression)

        if isinstance(expression, Unary):
            right = self.evaluate(expression.right)
            if expression.operator.type == TokenType.MINUS:
                return -self.number_value(right)
            if expression.operator.type in (TokenType.BANG, TokenType.NOT):
                return 0 if self.is_truthy(right) else 1

        if isinstance(expression, Binary):
            left = self.evaluate(expression.left)
            right = self.evaluate(expression.right)
            operator = expression.operator.type

            if operator == TokenType.PLUS:
                if isinstance(left, str) and isinstance(right, str):
                    return left + right
                return self.number_value(left) + self.number_value(right)
            if operator == TokenType.MINUS:
                return self.number_value(left) - self.number_value(right)
            if operator == TokenType.STAR:
                return self.number_value(left) * self.number_value(right)
            if operator == TokenType.SLASH:
                right = self.number_value(right)
                if right == 0:
                    raise RuntimeError("Division by zero.")
                return self.number_value(left) / right
            if operator == TokenType.PERCENT:
                right = self.number_value(right)
                if right == 0:
                    raise RuntimeError("Modulo by zero.")
                return self.number_value(left) % right
            if operator == TokenType.EQUAL_EQUAL:
                return int(left == right)
            if operator == TokenType.NOT_EQUAL:
                return int(left != right)
            if operator == TokenType.GREATER:
                return int(self.number_value(left) > self.number_value(right))
            if operator == TokenType.GREATER_EQUAL:
                return int(self.number_value(left) >= self.number_value(right))
            if operator == TokenType.LESS:
                return int(self.number_value(left) < self.number_value(right))
            if operator == TokenType.LESS_EQUAL:
                return int(self.number_value(left) <= self.number_value(right))
        raise RuntimeError("Invalid expression.")

    def number_value(self, value):
        if isinstance(value, bool):
            return int(value)
        if isinstance(value, (int, float)):
            return value
        raise RuntimeError("Operand must be a number.")

    def is_truthy(self, value):
        return value is not None and value != 0


class RuntimeError(Exception):
    pass