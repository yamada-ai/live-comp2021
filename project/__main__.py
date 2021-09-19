from project.controller import Controller

def sys_utterance(text, turn):
    print("sys[{0}]: {1}".format(turn, text))

# def user_utterance(text, turn):
#     print("usr[{0}]: {1}".format(turn, text))

def wait_user_utterance(turn):
    utterance = input("usr[{0}]: ".format(turn))
    return utterance

if __name__ == "__main__":
    print("start conversation")

    init_utt = "湯川先輩お疲れ様です! 今お時間いいですか?"
    rule_path = "./project/rule/"
    controller = Controller(rule_path)

    turn_limit = 16
    turn_mem = [0, 0]

    context = []
    # usr = []
    for i in range(turn_limit):
        if i==0:
            sys_utterance(init_utt, i+1)
            # user_utterance("嫌だ", i+1)
            utterance = wait_user_utterance(i+1)
            context.append(init_utt)
            context.append(utterance)
        else:
            utt = controller.reply(context)
            sys_utterance(utt, i+1)
            utterance = wait_user_utterance(i+1)
            context.append(utt)
            context.append(utterance)
        
        # コントローラーに context の情報をセット
        print()