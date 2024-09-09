
#teststring = "this has a % si()%%gn"

def remove_special_characters(string):
    special_chars = "!#¤%&/()=?`*^¨\'@£$$€€{{[[]}\~"
    for char in special_chars:
        if char in string:
            string = string.replace(char, "")
    return string

#result = remove_special_characters(teststring)
#print(result)


