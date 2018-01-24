def get_parameter_dict(filename):
    parameter_dict = {}
    with open(filename) as InFile:
        for row in InFile:
            if row[0] is not "#" and row[0] is not "\n" and row[0] is not " ":
                row = row.replace("\n","").split("=")
                
                if row[1].find(",") >= 0:
                    row[1] = [s.strip() for s in row[1].split(",")]

                parameter_dict[row[0]] = row[1]

    return parameter_dict