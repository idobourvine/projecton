if __name__ == "__main__":
    import re
    import ast

    bloons = ast.literal_eval("[[0.0, 1.1], [20.2, 33.0]]")
    print(bloons)

    msg = "MESSAGEBloons[0]14\tMESSAGECanShoot[0]12\tMESSAGEDidPop[0]12"
    print(msg)

    splut = msg.split('MESSAGE')

    for i in splut:
        a = i.strip()
        print(i)
        print(a)

    print(splut)
    msg_pattern = re.compile("(\d+$)")

    returned = msg_pattern.sub('', msg)

    print(returned)

