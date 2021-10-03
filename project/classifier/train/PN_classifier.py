import math
from project.classifier.datatool.preprocess import Preprocessor

class PN_Classifier():
    def __init__(self, vec_model):

        self.NEGATION = ['ない', 'ず', 'ぬ']
        self.PN_AMORPHOUS = []
        self.pre = Preprocessor()

        self.P_Threshold = 0.5
        self.N_Threshold = -0.5
        self.vec_model = vec_model
        
        # 極性が高いかつ品詞の違う単語・慣用句表現を設定
        self.posi_list = ['満足', '幸せ','喜び','善','賞賛','賢い','向上','あっぱれ','うれしい','徳','才能', '大事']
        self.nega_list = ['残念', '不幸せ','悲しみ','悪','非難','愚か','低下', '一喝', '哀しい', '罪', '平凡', '邪魔']

    def get_word_pn_score(self, _word, _dict):
        res = 0
        if _word in _dict:
            res = _dict[_word]['score']
        else :
            res = self.get_unknownwords_score(_word, _dict)
        return res
    
    def get_unknownwords_score(self, _word, _dict):
        res = 0
        if self.vec_model is None:
            return res
        pn_list = []
        for pg in self.posi_list:
            try:
                pn_list.append(self.vec_model.similarity(pg, _word) * (1))
            except KeyError:
                continue
        for ng in self.nega_list:
            try:
                print(self.vec_model.similarity(ng, _word) * (-1))
                pn_list.append(self.vec_model.similarity(ng, _word) * (-1))
            except KeyError:
                continue
        if len(pn_list) != 0:
            res = sum(pn_list) / len(pn_list)
        # 名詞・形容詞などは値が小さくなるため調整が必要
        return res

    def get_document_pn_score(self, _doc, _dict):
        tot_score = 0
        res = []
        text = ''
        lemmas = self.pre.get_lemma(_doc)
        POSes = self.pre.get_POS(_doc)
        adv_score = 0

        for lemma, POS in zip(lemmas, POSes):
            for i, token in enumerate(list(zip(lemma,POS))):
                score = self.get_word_pn_score(token[0], _dict)
                text += token[0]

                # 否定語
                if token[0] in self.NEGATION and 'あるじゃない' not in text:
                    tot_score *= -1

                # 副詞で強調
                if adv_score != 0:
                    score *= adv_score
                    adv_score = 0
                if token[1] == 'ADV':
                    adv_score = 1.5

                tot_score += score
                if score != 0:
                    res.append([token[0], score])

        if len(res) == 0:
            tot_score = 0
        else :
            tot_score /= len(res)

        return math.tanh(tot_score), res
    
    def predict(self, _text, _dict):
        score, words = self.get_document_pn_score(_text, _dict)
        if score > self.P_Threshold :
            return 8    #'positive'
        elif score < self.N_Threshold:
            return 9    #'negative'