def get_parameter_dict(filename):
    parameter_dict = {}
    with open(filename) as InFile:
        for row in InFile:
            # Ignore comments, skips newlines and empty lines
            if row[0] is not "#" and row[0] is not "\n" and row[0] is not " ":
                # Clean up newline, split to key value
                row = row.replace("\n","").split("=")
                
                if row[1].find(",") >= 0:
                    # Make python list from supposing list
                    row[1] = [s.strip() for s in row[1].split(",")]
                
                # key -> value
                parameter_dict[row[0]] = row[1]

    return parameter_dict