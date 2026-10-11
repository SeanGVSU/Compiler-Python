plus = make_token(TokenType.PLUS, "+")
expression = Binary(Literal(1), plus, Literal(2))
print(AstPrinter().print_expr(expression))         
# expected (+ 1 2)

minus = make_token(TokenType.MINUS, "-")
expression = Unary(minus, Literal(5))
print(AstPrinter().print_expr(expression))         
# expected (- 5)

bang = make_token(TokenType.BANG, "!")
expression = Unary(bang, Literal(False))
print(AstPrinter().print_expr(expression))         
# expected (! false)