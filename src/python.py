import sys

def run_repl():
    while True:
        try:
            user_text = input(" ")
            print(user_text)
            print("Scanner Not Implemented")
        except KeyboardInterrupt:
            break

def run_file(userfile):
        with open(userfile, "r") as file:
            code = file.read()

        print(code)
        print("Scaner Not Implemented")
        
if len(sys.argv) == 1:
    run_repl()
elif len(sys.argv) == 2:
    run_file(sys.argv[1])
else:
    print("syntax setup: python.py (file_code)")