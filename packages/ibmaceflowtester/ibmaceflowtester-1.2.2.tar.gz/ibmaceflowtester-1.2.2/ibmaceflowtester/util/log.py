def write(string):
    print(string, flush=True)


def write_surround_asterisk(string):
    write("*" * (len(string) + 4))
    write(f"* {string} *")
    write("*" * (len(string) + 4))
    write("")


def write_underline(string, char):
    write(string)
    write(char * len(string))
