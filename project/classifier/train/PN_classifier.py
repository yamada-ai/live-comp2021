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
        self.posi_list = ['満足', '幸せ','喜び','善','賞賛','賢い','向上','徳','才能', '大事']
        self.nega_list = ['残念', '不幸','悲しみ','悪','非難','愚か','低下', '罪', '平凡', '邪魔']

    def get_unknownwords_score(self, _word):
        res = 0
        if self.vec_model is None:
            return res
        pn_list = []
        for pg in self.posi_list:
            try:
                pn_list.append((self.vec_model.similarity(pg, _word) - 0.99) * (1000))
            except KeyError:
                continue
        for ng in self.nega_list:
            try:
                pn_list.append((self.vec_model.similarity(ng, _word) - 0.99)* (-1000))
            except KeyError:
                continue
        if len(pn_list) != 0:
            res = sum(pn_list) / len(pn_list)
        # 名詞・形容詞などは値が小さくなるため調整が必要
        if res > 0.3:
            return 1
        if res > 0.1:
            return 0.5
        elif res > -0.1:
            return 0
        elif res > -0.3:
            return -0.5
        else:
            return -1

    def get_word_pn_score(self, _word, _dict):
        res = 0
        if _word in _dict:
            res = _dict[_word]['score']
        else :
            res = self.get_unknownwords_score(_word)
        return res

    def get_wago_pn_score(self, _word, _text, _score, _dict, _wago_dict):
        wago = ""
        score = 0
        extract_word = []
        if _word in _wago_dict:
            key = ''
            for t in _text:
                key = t + key
            if t in _dict:
                extract_word.append([t, _dict[t]['score']])
                # search wago
                if key in _wago_dict[_word]:
                    wago = key
                    score = _wago_dict[_word][wago]['score']
        return wago, score, extract_word

    def totaling_score(self, _scores):
        all_tot = 0
        """
        token[0] : lemma or tag
        token[1] : score
        """
        for token in _scores:
            if 'REV' in token[0]:
                all_tot *= token[1]
            else:
                all_tot += token[1]
        return math.tanh(all_tot)

    def get_document_pn_score(self, _doc, _dict, _wago_dict):

        # tokenize _doc
        if not self.pre.get_lemma(_doc):
            return 0 , []
        lemmas = self.pre.get_lemma(_doc)[0]
        POSes = self.pre.get_POS(_doc)[0]
        # 変数の初期化
        scores = []
        prevtext = []
        score = 0.
        tag = ''
        for index, token in enumerate(list(zip(lemmas,POSes))):
            prevtext = [token[0]] + prevtext
            # 用言の極性
            wago_tag, wago_score, extract = self.get_wago_pn_score(token[0], prevtext, scores, _dict, _wago_dict)
            if wago_score != 0:
                # 後処理
                scores.append([wago_tag, wago_score])
                for ex in extract:
                    scores.remove(ex)
                continue

            # 副詞による強調表現
            if token[1] == '副詞':
                tag, score = 'ADV', 1.5
                continue

            # 単語の極性
            if tag == 'ADV':
                tag += '+' + token[0]
                score *= self.get_word_pn_score(token[0], _dict)
            else:
                tag, score = token[0], self.get_word_pn_score(token[0], _dict)

            # 否定語
            if token[0] in self.NEGATION and 'あるじゃない' not in prevtext:
                tag, score = "REV" + token[0], -1
            
            # 初期化
            if tag == '' or score == 0:
                continue
            scores.append([tag, score])
            score = 0
            tag = ''
        return self.totaling_score(scores), scores
    
    def predict(self, _text, _dict, _wago_dict):
        score, words = self.get_document_pn_score(_text, _dict, _wago_dict)
        # print(words)
        # print(score)
        if score > self.P_Threshold :
            return 8    #'positive'
        elif score < self.N_Threshold:
            return 9    #'negative'