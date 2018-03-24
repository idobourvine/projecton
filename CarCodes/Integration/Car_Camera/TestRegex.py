if __name__ == "__main__":
    import re
    import ast

    msg_pattern = re.compile("(^\w*MSG)")
    useless_number_pattern = re.compile("(\d+$)")

    msg = "MESSAGEBloonsMSG[[-9.34, 2.63]]21\tMESSAGECanShootMSG[" \
          "0]19\tMESSAGEDidPopMSG[0]"

    messages = msg.split('MESSAGE')

    for real_msg in messages:
        if real_msg == '':
            continue

        stripped = real_msg.strip()
        removed_useless_num = useless_number_pattern.sub(
            '', stripped)
        print("removed_useless_num: " + removed_useless_num)

        split = msg_pattern.split(removed_useless_num, 1)

        if not split:
            print("Couldn't split")
            continue

        print("split recieved: " + str(split))

        msg_type = split[1]
        raw_msg = split[2]
        data = ast.literal_eval(raw_msg)

        print(data)

