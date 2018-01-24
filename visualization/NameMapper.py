def map_name_from_file(filename):
    name_dict = {}
    with open(filename) as inFile:
        for row in inFile:
            names = row.split(",")
            for name in names:
                name = name.strip('\n')
                name_dict[name] = names[0]
    name_dict.pop('')
    return name_dict