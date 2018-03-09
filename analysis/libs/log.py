def log(what_is_happening, indent_level):
    indent = ''.join((['---'] * indent_level))
    print(indent + what_is_happening)
