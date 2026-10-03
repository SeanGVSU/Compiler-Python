class TokenType:
    
    PLUS = "PLUS"
    MINUS = "MINUS"
    STAR = "STAR"
    SLASH = "SLASH"
    PERCENT = "PERCENT"

    EQUAL = "EQUAL"
    EQUAL_EQUAL = "EQUAL_EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    LESS = "LESS"
    LESS_EQUAL = "LESS_EQUAL"
    GREATER = "GREATER"
    GREATER_EQUAL = "GREATER_EQUAL"

    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"
    LEFT_BRACKET = "LEFT_BRACKET"
    RIGHT_BRACKET = "RIGHT_BRACKET"
    LEFT_BRACE = "LEFT_BRACE"
    RIGHT_BRACE = "RIGHT_BRACE"

    COMMA = "COMMA"
    COLON = "COLON"
    DOT = "DOT"
    SEMICOLON = "SEMICOLON"

    
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    STRING = "STRING"

    
    IF = "IF"
    ELSE = "ELSE"
    ELIF = "ELIF"
    FOR = "FOR"
    WHILE = "WHILE"
    DEF = "DEF"
    RETURN = "RETURN"
    CLASS = "CLASS"
    IMPORT = "IMPORT"
    FROM = "FROM"
    AS = "AS"
    IN = "IN"
    IS = "IS"
    NOT = "NOT"
    AND = "AND"
    OR = "OR"
    TRUE = "TRUE"
    FALSE = "FALSE"
    NONE = "NONE"
    PRINT = "PRINT"

    EOF = "EOF"


class Token:
    def __init__(self, token_type, lexeme, literal, line):
        self.type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return f"{self.type} {self.lexeme} {self.literal} (line {self.line})"