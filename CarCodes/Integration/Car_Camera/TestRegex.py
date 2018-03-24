if __name__ == "__main__":
    import re
    import ast

    bloons = ast.literal_eval("[[0.0, 1.1], [20.2, 33.0]]")
    print(bloons)

    msg = "BloonsMSG[[0.0, 1.1], [20.2, 33.0]]"
    msg_pattern = re.compile("(^\w*MSG)")

    split = msg_pattern.split(msg, 1)
    print(split)
    if not split:
        print("Couldn't split")

    msg_type = split[1]
    raw_msg = split[2]

    print("msg_type: " + msg_type)
    print("raw_msg: " + raw_msg)

    if msg_type == "BloonsMSG":
        bloons = ast.literal_eval(raw_msg)
        print("Caught bloons")
        print(bloons)
