def get_parameter_dict():
    parameter_dict = {}
    with open("parameter-file.txt") as InFile:
        for row in InFile:
            if row[0] is not "#" and row[0] is not "\n" and row[0] is not " ":
                row = row.replace("\n","").split("=")
                parameter_dict[row[0]] = row[1]

    return parameter_dict