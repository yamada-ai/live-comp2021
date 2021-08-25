
# from parse import parsing
# from parse import lexical
# from classifier import parse
# import classifier
from classifier.parse.parsing import CulcParser
import os
import json

class Controller:
    def __init__(self, rule_path) -> None:
        self.parser = CulcParser()

        self._load_rules(rule_path)
        self.ID_history = []
        
    
    # ルールの読み込み
    def _load_rules(self, rule_path):
        self.rules_name = os.listdir(rule_path)
        self.topic_rules = []
        for fname in self.rules_name:
            if "change" in fname:
                with open(rule_path+fname, "r") as f:
                    self.change_rule = json.load(f)
            else:
                with open(rule_path+fname, "r") as f:
                    topic_rule = json.load(f)
    
                    
    


if __name__ == "__main__":
    print("start")
    code = 'if in( "うざい", usr[-1] )'
    # code = "if "

    rule_path = "./rule/"

    controller = Controller(rule_path)
    print(controller.parser.parsing(code))