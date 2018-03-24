if __name__ == "__main__":
    import re
    import ast

    bloons = ast.literal_eval("[[0.0, 1.1], [20.2, 33.0]]")
    print(bloons)

    msg = "CanShootMSG[0]12"
    msg_pattern = re.compile("(\d+$)")

