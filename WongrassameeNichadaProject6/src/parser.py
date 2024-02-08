import sys

def parseempty(line, comment):
    """remove blank, \n, \t space and comments
    return :
        - line with no space or comment
        - comment status"""

    linenospace = ""
    i = 0
    while i < len(line):
        if line[i:i+2] == "//":
            linenospace += "\n"
            break
        elif line[i:i+2] == "/*":
            comment = True
            i+=2
        elif line[i:i+2] == "*/":
            comment = False
            i+=2 #note
        elif line[i] == " " or line[i] == "\t":
            i+=1
        else:
            if not comment :
                # only append char that is not in comment or blank
                linenospace += line[i]
            i+=1
    return linenospace, comment

if __name__ == "__main__":
    # parse .asm to .out
    filename = sys.argv[1][:-4] # parse filename
    with open(f'{filename}.out', "w") as fout:
        with open(f'{filename}.asm', "r") as fd:
            comment = False # comment status at the beginning of the file
            for line in fd:
                linenospace, comment = parseempty(line, comment)
                if linenospace and linenospace != "\n":
                    # write to output file
                    fout.write(linenospace)
