import os
import sys

import scipy
import re
import json
import random

class Generator:

    def __init__(self, bot_name, path) -> None:
        self.bot_name = bot_name
        self.phase = 31
        self.phase_rules = [
            self._phase_0,
            self._phase_1,
            self._phase_2,
            self._phase_3,
            self._phase_4,
            self._phase_5,
            self._phase_6,
            self._phase_7,
            self._phase_8,
            self._phase_9,
            self._phase_10,
            self._phase_11,
            self._phase_12,
            self._phase_13,
            self._phase_14,
            self._phase_15,
            self._phase_16,
            self._phase_17,
            self._phase_18,
            self._phase_19,
            self._phase_20,
            self._phase_21,
            self._phase_22,
            self._phase_23,
            self._phase_24,
            self._phase_25,
            self._phase_26,
            self._phase_27,
            self._phase_28,
            self._phase_29,
            self._phase_30,
            self._phase_31,
            self._phase_32,
            self._phase_33, 
            self._phase_34,
            self._phase_35,
            self._phase_36,
            self._phase_37,
            self._phase_38,
            self._phase_39,
            self._phase_40,
            self._phase_41,
            self._phase_42,
            self._phase_43,
            self._phase_44,
            self._phase_45
        ]
        self._install_rule(path)

        self._update_phase(self.phase)
        
    
    # change_search_for_phase
    def _update_phase(self, phase):
        #change_search_for_phase
        print(phase)
        self.current_phase = self.phase_rules[phase]
        for rules in self.rule_base:
            if rules["phase"] == phase:
                self.corrent_rule = rules["rule"]
                break
    
    def _install_rule(self, path):
        with open(path, "r") as f:
            rule_base_all = json.load(f)
        self.rule_base = rule_base_all[self.bot_name]

    def reply(self, context):
        self._update_phase(self.phase)
        rep, next_phase = self.current_phase(context)
        self._update_phase(next_phase)
        self.phase = next_phase
        print("next : {0}, current_phase: {1}".format(next_phase, self.current_phase.__name__))
        return rep

    def decide_act(self, usr_act):
        for rule in self.corrent_rule:
            if rule["usr_act"] == usr_act:
                if isinstance(rule["reply"], list):
                    return random.choice(rule["reply"]), rule["next"]
                else:
                    return rule["reply"], rule["next"]

    
    def _phase_0(self, context):
        usr = context[-1]
        # no_list = set("ダメ だめ 駄目 待て 待って ... 何時 嫌 いや は？".split())
        # yes_list = set("どうぞ はい なんでし なんですか いいよ 良い ".split())

        no_list = "ダメ だめ 駄目 待て 待って ... 何時だと？ 嫌 いや は？　やだ".split()
        double_no_list = "でもない ではない 嘘 というわけでは というわけでも ということではない".split()
        yes_list = "どうぞ はい なんでし なんですか いいよ 良い ".split()

        usr_act = "yes"
        for no in no_list:
            if no in usr:
                usr_act = "no"
                # 二重否定は死ね
                for dou in double_no_list:
                    if dou in usr:
                        usr_act = "yes"
                        break
                break
        
        for rule in self.corrent_rule:
            if rule["usr_act"] == usr_act:
                if isinstance(rule["reply"], list):
                    return random.choice(rule["reply"]), rule["next"]
                else:
                    return rule["reply"], rule["next"]
    
    def _phase_1(self, context):
        usr = context[-1]

        why_list = "なんで？ 何故 なぜ 同期だけ 同期と 俺 私".split()
        who_list = "誰 同期って".split()
        no_list = "ダメ だめ 駄目 待て 待って ... 何時 嫌 いや は？ 気が乗ら".split()

        usr_act = "else"
        acts = [why_list, who_list, no_list]
        acts_str = ["why", "who", "no"]
        for act, act_s in zip(acts, acts_str):
            for word in act:
                if word in usr:
                    usr_act = act_s
        
        for rule in self.corrent_rule:
            if rule["usr_act"] == usr_act:
                if isinstance(rule["reply"], list):
                    return random.choice(rule["reply"]), rule["next"]
                else:
                    return rule["reply"], rule["next"]
    
    def _phase_2(self, context):
        usr = context[-1]

        # yes_list = "そうだ ".split()
        usr_act = "yes"
        no_list = "実は いや でも はずだ".split()
        for no in no_list:
            if no in usr:
                usr_act = "no"
                # 二重否定は死ね
                break
        for rule in self.corrent_rule:
            if rule["usr_act"] == usr_act:
                if isinstance(rule["reply"], list):
                    return random.choice(rule["reply"]), rule["next"]
                else:
                    return rule["reply"], rule["next"]


    def _phase_3(self, context):
        usr = context[-1]

    def _phase_4(self, context):
        return "ERROR" , 0

    def _phase_5(self, context):
        return "ERROR" , 0

    def _phase_6(self, context):
        return "ERROR" , 0

    def _phase_7(self, context):
        return "ERROR" , 0

    def _phase_8(self, context):
        return "ERROR" , 0

    def _phase_9(self, context):
        return "ERROR" , 0

    def _phase_10(self, context):
        return "ERROR" , 0

    def _phase_11(self, context):
        return "ERROR" , 0

    def _phase_12(self, context):
        return "ERROR" , 0

    def _phase_13(self, context):
        return "ERROR" , 0

    def _phase_14(self, context):
        return "ERROR" , 0

    def _phase_15(self, context):
        return "ERROR" , 0

    def _phase_16(self, context):
        return "ERROR" , 0

    def _phase_17(self, context):
        return "ERROR" , 0

    def _phase_18(self, context):
        return "ERROR" , 0

    def _phase_19(self, context):
        return "ERROR" , 0

    def _phase_20(self, context):
        return "ERROR" , 0

    def _phase_21(self, context):
        return "ERROR" , 0

    def _phase_22(self, context):
        return "ERROR" , 0

    def _phase_23(self, context):
        return "ERROR" , 0

    def _phase_24(self, context):
        return "ERROR" , 0

    def _phase_25(self, context):
        return "ERROR" , 0

    def _phase_26(self, context):
        return "ERROR" , 0

    def _phase_27(self, context):
        return "ERROR" , 0

    def _phase_28(self, context):
        return "ERROR" , 0

    def _phase_29(self, context):
        return "ERROR" , 0

    def _phase_30(self, context):
        return "ERROR" , 0

    def _phase_31(self, context):
        usr = context[-1]
        
        usr_act = "else"
        if "小林" in usr:
            usr_act = "kobayashi"
        return self.decide_act(usr_act)

    def _phase_32(self, context):
        return self.decide_act("else")

    def _phase_33(self, context):
        usr = context[-1]
        no_list = "嫌 苦手 憎 きらい きらう いや 役に立た".split()
        
        usr_act = "else"
        for no in no_list:
             if no in usr:
                 usr_act = "no"
                 break
        return self.decide_act(usr_act)

    def _phase_34(self, context):
        return self.decide_act("else")

    def _phase_35(self, context):
        return self.decide_act("else")

    def _phase_36(self, context):
        return self.decide_act("else")

    def _phase_37(self, context):
        usr = context[-1]
        no_list = "具体的にな 具体的にはな 特にはな 特にな".split()

        usr_act = "else"
        for no in no_list:
            if no in usr:
                usr_act = "no"
                break
        return self.decide_act(usr_act)

    def _phase_38(self, context):
        return self.decide_act("else")

    def _phase_39(self, context):
        return self.decide_act("else")

    def _phase_40(self, context):
        return self.decide_act("else")

    def _phase_41(self, context):
        return self.decide_act("else")

    def _phase_42(self, context):
        return self.decide_act("else")

    def _phase_43(self, context):
        return self.decide_act("else")

    def _phase_44(self, context):
        return self.decide_act("else")

    def _phase_45(self, context):
        return self.decide_act("else")

        


