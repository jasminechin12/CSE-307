import re

binary = re.compile("^0[b|B][0-1]+")
octal = re.compile("^0[o|O][0-7]+")
hexadecimal = re.compile("^0[x|X][a-fA-F0-9]+")
baseten = re.compile("[1-9][0-9]*")
float = re.compile("^[0-9]*\.[0-9]*")
floatnotation = re.compile("^(([\d]*\.[\d]*[e|E][+-]?[1-9]\d*))|([1-9]*[e|E][+-]?[1-9]\d*)")


def is_legal_num(stuff):
    if re.fullmatch(binary, stuff) or re.fullmatch(octal, stuff) or re.fullmatch(hexadecimal, stuff) or re.fullmatch(baseten, stuff):
        return "int"
    elif re.fullmatch(float, stuff) or re.fullmatch(floatnotation, stuff):
        return "float"
    else:
        return "None"

def main():
    stuff = input()
    stuff = stuff.strip("+-")
    print(is_legal_num(stuff))
    exit()


if __name__ == '__main__':
    main()
