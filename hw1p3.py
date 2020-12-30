import re

matchquotes = re.compile("^(\'.*\')|(\".*\")")
backslashes = re.compile(".*?[\\\\+]$")


def is_legal_string(stuff1, stuff2):
    if len(stuff1) == 0:      # if input1 is empty, automatically false
        return False

    stuff1 = stuff1.lstrip()  # strip leading white spaces in input1
    stuff1 = stuff1.rstrip()  # strip trailing white spaces in input1
    stuff2 = stuff2.rstrip()  # strip trailing white spaces in input2

    count = 0

    if re.fullmatch(backslashes, stuff1) is None:
        for char in range(2, len(stuff1) + 1):
            if stuff1[-char] == "\\":
                count += 1
            else:
                break

        quote = stuff1[0]
        for char in range(1, len(stuff1)-1):
            if stuff1[char] == quote and stuff1[char - 1] != "\\":
                return False

        return len(stuff2) == 0 and re.fullmatch(matchquotes, stuff1) and count % 2 == 0

    else:
        for char in range(1, len(stuff1) + 1):
            if stuff1[-char] == "\\":
                count += 1
            else:
                break

        if count % 2 == 1:
            quote = stuff1[0]
            for char in range(1, len(stuff1)):
                if stuff1[char] == quote and stuff1[char-1] != "\\":
                    return False
            str = stuff1 + stuff2
            return re.fullmatch(matchquotes, str) is not None
        else:
            return False


def main():
    stuff1 = input()
    stuff2 = input()
    print(is_legal_string(stuff1, stuff2))
    exit()


if __name__ == '__main__':
    main()
