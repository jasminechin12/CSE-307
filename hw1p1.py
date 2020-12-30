import re

keywords = ["False", "None", "True", "And", "as", "assert", "break", "def", "del",
            "elif", "else", "except", "finally", "for", "if", "import", "in", "is",
            "lambda", "nonlocal", "not", "raise", "return", "try", "while", "with",
            "yield", "class", "continue", "from", "global", "or", "pass"]

pattern = re.compile("^[a-zA-Z_][a-zA-Z0-9_]*")


def is_legal_identifier(stuff):
    if stuff in keywords:
        return False
    elif re.fullmatch(pattern, stuff) is None:
        return False
    else:
        return True


def main():
    stuff = input()
    print(is_legal_identifier(stuff))
    exit()


if __name__ == '__main__':
    main()
