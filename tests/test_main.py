from project.classifier.datatool import preprocess
import sys, unittest
sys.path.append("project/classifier/")
from project.controller import Controller
from project.classifier import datatool

class Test_main(unittest.TestCase):

    def sys_utterance(self, text, turn):
        print("sys[{0}]: {1}".format(turn, text))

    def wait_user_utterance(self, turn):
        utterance = input("usr[{0}]: ".format(turn))
        return utterance

    def test(self):
        print("start conversation")

        init_utt = "湯川先輩お疲れ様です! 今お時間いいですか?"
        rule_path = "./project/rule/"
        controller = Controller(rule_path)

        turn_limit = 16
        turn_mem = [0, 0]

        context = []
        usr = []
        for i in range(turn_limit):
            if i==0:
                self.sys_utterance(init_utt, i+1)
                # user_utterance("嫌だ", i+1)
                utterance = self.wait_user_utterance(i+1)
                context.append(init_utt)
                context.append(utterance)
            else:
                utt = controller.reply(context)
                self.sys_utterance(utt, i+1)
                utterance = self.wait_user_utterance(i+1)
                context.append(utt)
                context.append(utterance)
            
            # コントローラーに context の情報をセット
            #print()

        # code = "if (yn(usr[-1]) or how(usr[-1])) and in(['居酒屋', 'お店','スナック', '飲み屋', '酒場', 'バー', '外'], usr[-1])"
        # # code = "if yn(usr[-1]) or how(usr[-1]) "
        # controller.parser.set_usr(["今忙しい", "いいよ"])
        # print(controller.persing(code))       
