# from parse import parsing
# from parse import lexical
# from classifier import parse
# import classifier
from project.classifier.datatool import preprocess
from project.classifier.parse.parsing import CulcParser
from project.classifier.classify import Classifier
# from project.classifier 
import sys
# sys.path.append("./datatool")
import os
import json
import random

class Controller:
    def __init__(self, rule_path) -> None:
        self.parser = CulcParser()
        self.classifier = Classifier(model_path="./project/classifier/models/", F_path="./project/classifier/X_y_data/")
        self.classifier.load_F("typeClassify_F2.pickle")
        self.classifier.load_model("typeClassify_M2.pickle")
        self.classifier.load_dict("PN.pickle")
        self.parser.set_classifier(self.classifier)
        self._load_rules(rule_path)

        self.stateID_history = []
        
        self.fired_qa_rules = []
        self.user = []
        self.sytem = []

        self.current_ID = {
            "topic" : 0,
            "act"   : 0,
            "phase" : 0,
        }
        self.current_turn = {
            "topic" : 0,
            # "act"   : 0,
            "phase" : 0
        }
        self.next_actID = []
        self.set_current_state()

        self.is_prev_QA = 0
        self.QA_id = {}
        self.is_continue_QA = False
        # self.is_prev_QA = 0

        # self.update_next(self.current_state)
    
    # def check_change_rule(self, context):

    def set_current_state(self):
        self.current_topic = self.topic_rules[self.current_ID["topic"]]["phase"]
        for ph in self.current_topic:
            # 一致する phase
            # print(ph.keys())
            if ph["phase_id"] == self.current_ID["phase"]:
                self.current_phase = ph
                for ac in ph["act"]:
                    # 一致する act
                    if ac["act_id"] == self.current_ID["act"]:
                        self.current_act = ac
                        self.next_actID = self.current_act["next"]

    def update_next(self, current_ID):        
    #     print(self.next_actID)
        pass

    # def check_change_phase(self):


    # phaseの移動も実施
    def go2next_act(self):
        next_act_id_list = []
        for ac in self.current_phase["act"]:
            next_act_id_list.append(ac["act_id"])
            # actを変更
            if ac["act_id"] in self.next_actID:
                # print(ac["condition"])
                if self.parser.parsing(ac["condition"]):
                    self.next_actID = ac["next"]
                    self.current_ID["act"] = ac["act_id"]
                    self.current_act = ac
                    break
        
        self.current_turn["phase"] += 1

        change_phase_rule = self.current_phase["change_phase"]
        # self.parser.set_act_temp(self.next_actID[0])
        for rule in change_phase_rule:
            if self.parser.parsing(rule["condition"]):
                print("change phase")
                # self.current_ID["act"] = 0
                self.current_ID["phase"] = rule["next"][0]
                for ph in self.current_topic:
                    if ph["phase_id"] == self.current_ID["phase"]:
                        self.current_turn["phase"] = 0
                        for ac in ph["act"]:
                            if self.parser.parsing(ac["condition"]):
                                self.current_ID["act"] = ac["act_id"]
                                self.current_act = ac
                                self.set_current_state()
                                break
                        break
                break
        if isinstance(self.current_act["reply"], str):
            return self.current_act["reply"]
        else:
            return random.choice(self.current_act["reply"])
    
    def reply(self, context):
        # ユーザ発話を追加
        self.user.append(context[-1])
        self.parser.set_usr(self.user)
        self.parser.set_ID(self.current_ID)
        self.parser.set_turn(self.current_turn)

        # topic分類
        # 1. QA
        qa_utt = ""
        qa_utt = self.check_QA_rules()
        # print(qa_utt)
        if qa_utt != "":
            self.is_prev_QA = True
            return qa_utt
        else:
            # 決定した topic のルールで発話選択
            t = self.check_change_topic_rule() 
            if t >= 0:
                print("change topic:",t)
                self.current_turn["topic"] = 0
                self.set_current_state()
                utt = self.current_act["reply"]
                self.current_turn["topic"] += 1
            else:
                utt = self.go2next_act()
                # self.set_current_state()
            self.stateID_history.append(self.current_ID)
            self.current_turn["topic"] += 1
            self.is_prev_QA = False
            return utt

    def persing(self, code):
        print("code: {0}".format(code))

        print(self.parser.parsing(code))  

    def check_QA_rules(self):
        utt = ""
        for ac in self.QA_rule["qa_init_phase"]["act"]:
            # 条件部で発火した場合
            if self.parser.parsing(ac["condition"]):
                print(ac["condition"])
                utt = ac["reply"]
                self.current_ID["act"] = ac["act_id"]
                next_id = ac["next"][0]
                # continue QA
                if next_id > 99:
                    self.is_continue_QA = True
                # 98
                elif next_id == 98:
                    # 98 で元のactに戻る
                    self.current_ID["act"] = self.stateID_history[-1]["act"]
                # 99
                else:
                    # 99 で次のphase へ行く？
                    # 現状はそのまま 98 と同じ挙動
                    self.current_ID["act"] = self.stateID_history[-1]["act"]
                break
        return utt
        

    
    def check_change_topic_rule(self):
        t = -1
        for topic in self.topic_change_rules:
            if topic["topic_id"] == self.current_ID["topic"]:
                for rule in topic["change_topic"]:
                    # print(rule["condition"])
                    if self.parser.parsing(rule["condition"]) : 
                        # print("change topic")
                        self.current_ID["topic"] = rule["next"][0]
                        self.current_ID["phase"] = 0
                        # self.current_ID["act"]  = 0
                        t =  rule["next"][0]
                        break
                break
        if t >=0:
            current_topic = self.topic_rules[self.current_ID["topic"]]["phase"]
            for ph in current_topic:
                if ph["phase_id"] == self.current_ID["phase"]:
                    for ac in ph["act"]:
                        if self.parser.parsing(ac["condition"]):
                            self.current_ID["act"] = ac["act_id"]
                            self.current_act = ac
                            self.set_current_state()
                            break
                    break
        return t
        

    # ルールの読み込み
    def _load_rules(self, rule_path):
        self.rules_name = os.listdir(rule_path)
        
        self.topic_change_rules = []
        for fname in self.rules_name:
            if ".json" not in fname:
                continue
            if "change" in fname:
                with open(rule_path+fname, "r", encoding = "utf-8") as f:
                    self.change_rule_json = json.load(f)
                for rule in self.change_rule_json["topic_rule"]:
                    self.topic_change_rules.append(rule)
        # print(self.topic_change_rules)
        # print()
        # QAルールを取得
        qa_path = self.change_rule_json["qa_rule"]["file_name"]
        with open(rule_path+qa_path, "r", encoding = "utf-8") as f:
            self.QA_rule = json.load(f)

        # 各トピックのルールを取得
        self.topic_rules = []
        for topic in self.topic_change_rules:
            topic_path = topic["file_name"]
            # print(rule_path+topic_path)
            with open(rule_path+topic_path, "r", encoding = "utf-8") as f:
                self.topic_rules.append( json.load(f) ) 
        # print(self.topic_rules)

if __name__ == "__main__":
    # print("start")
    code = "if yn( 'それは正しいものですか？')"
    # code = "if "
    rule_path = "./project/rule/"

    controller = Controller(rule_path)

    # print(controller.reply(["湯川先輩お疲れ様です! 今お時間いいですか?", "いいよ"]))
    
    # controller.persing(code)
    print(controller.parser.parsing(code))