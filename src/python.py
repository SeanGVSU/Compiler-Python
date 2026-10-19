import sys
from scanner import Scanner
from parser import Parser, ParseError
from ast_printer import AstPrinter


def run_source(code):
    scanner = Scanner(code)
    tokens = scanner.scan_tokens()

    # Do not parse if scanning found errors.
    if scanner.error:
        for errors in scanner.error:
            print(errors)
        return
    parser = Parser(tokens)

    try:
        expression = parser.parse()
    except ParseError as error:
        print(error)
        return

    # Print only after scanning and parsing succeed.
    printer = AstPrinter()
    print(printer.print_expr(expression))

def run_repl():
    while True:
        try:
            user_text = input(": ")
            run_source(user_text)
        except KeyboardInterrupt:
            print()
            break
        except EOFError:
            print()
            break

def run_file(userfile):
    try:
        with open(userfile, "r") as file:
            code = file.read()
        run_source(code)
    except FileNotFoundError:
        print(f"Could not find file: {userfile}")
    except OSError as error:
        print(f"Could not read file: {error}")


def main():
    if len(sys.argv) == 1:
        run_repl()
    elif len(sys.argv) == 2:
        run_file(sys.argv[1])
    else:
        print("syntax setup: src/python.py (file_code)")


if __name__ == "__main__":
    main()

