import inspect
#direct get the input name from called function code
def retrieve_name_ex(var):
    stacks = inspect.stack()
    try:
        callFunc = stacks[1].function
        code = stacks[2].code_context[0]
        startIndex = code.index(callFunc)
        startIndex = code.index("(", startIndex + len(callFunc)) + 1
        endIndex = code.index(")", startIndex)
        return code[startIndex:endIndex].strip()
    except:
        return ""
def printVar(var):
    print("{} = {}".format(retrieve_name_ex(var),var))

def writeBinFile(fileName, binContent):
    file = open(fileName, "wb")
    file.write(binContent)
    file.close()

def writeTextFile(fileName, textContent, encoding = "utf8"):
    file = open(fileName, "wt", encoding=encoding)
    file.write(textContent)
    file.close()
