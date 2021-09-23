from pathlib import Path
import json
from numpy.lib.function_base import percentile
import pandas as pd
import numpy as np
from pkg_resources import normalize_path
import spacy
import re
# import neologdn

class Preprocessor:

    def __init__(self) -> None:
        self.nlp = spacy.load('ja_ginza')
        # self.nlp.add_pipe('sentencizer')
        self.nlp.add_pipe(self.nlp.create_pipe('sentencizer'))

        # 数字
        self.DELETE_PATTERN_1 = re.compile(
            r'(\d+)(([,.])(\d*))*'
            )
        # 記号
        self.DELETE_PATTERN_2 = re.compile(
            r'[\．_－―─！＠＃＄％＾＆\-‐|\\＊\“（）＿■×+α※÷⇒—●★☆〇◎◆▼◇△□(：〜～＋=)／*&^%$#@!~`){}［］…\[\]\"\'\”\’:;<>?＜＞〔〕〈〉？、。・,\./『』【】「」→←○《》≪≫\n\u3000]+'
            )
        # URL
        self.DELETE_PATTERN_3 = re.compile(
            r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+'
            )
        # embedding size : 300
        self.emb_size = self.get_sentence_vec("emb").shape[0]

        self.independent_words = set("名詞 代名詞 動詞 形容詞 副詞 詞接続詞 感動詞 連体".split() )
    
    def clean_text(self, text):
        # trim contents in brackets
        # not defined

        # trim number
        text = self.DELETE_PATTERN_1.sub('0', text)

        # trim pattern
        text = self.DELETE_PATTERN_2.sub('', text)

        # trim url
        text = self.DELETE_PATTERN_3.sub('', text)

        # normalization
        # text = neologdn.normalize(text)

        return text

    def get_sentence_vec(self, sen) -> np.array:
        # sen_ = self.DELETE_PATTERN_1.sub(sen)
        # sen_ = self.DELETE_PATTERN_2.sub("", sen)
        sentence_vec = self.nlp(sen).vector
        # sentence_vec = self.sen_model.encode(sen)[0]
        return sentence_vec

    # tagging pos in sentences or sentence
    def get_POS(self, sentences):

        pos_list = []
        texts = []
        if isinstance(sentences, str):
            sentences = self.clean_text(sentences)
            doc = self.nlp(sentences)
            texts = [str(s)  for s in doc.sents]
        elif isinstance(sentences, list):
            docs = list(self.nlp.pipe(sentences, disable=['ner']))
            for doc in docs:
                text = [str(s) for s in doc.sents]
                texts.append(self.clean_text(str(text)))
        else:
            return None
        docs = list(self.nlp.pipe(texts, disable=['ner']))
        for doc in docs:
            pos_list.append([ token.tag_ for token in doc ])
        
        return pos_list
    
    # tagging lemma in sentences or sentence
    def get_lemma(self, sentences):

        lemma_list = []
        texts = []

        if isinstance(sentences, str):
            sentences = self.clean_text(sentences)
            doc = self.nlp(sentences)
            texts = [str(s)  for s in doc.sents]
        elif isinstance(sentences, list):
            docs = list(self.nlp.pipe(sentences, disable=['ner']))
            for doc in docs:
                doc = self.clean_text(doc)
                text = [str(s) for s in doc.sents]
                texts.extend(self.clean_text(str(text)))
        else:
            return None
        docs = list(self.nlp.pipe(texts, disable=['ner']))
        for doc in docs:
            lemma_list.append([ token.lemma_ for token in doc ])
        
        return lemma_list
    
    def extract_indepent_word(self, sen):
        indepent_list = []
        if isinstance(sen, str):
            doc = self.nlp(sen)
            texts = [str(s)  for s in doc.sents]

        elif isinstance(sen, list):
            texts = []
            docs = list(self.nlp.pipe(sen, disable=['ner']))
            # return [ self.get_POS(sen_) for sen_ in sen]
            for doc in docs:
                texts.extend( [str(s) for s in doc.sents] )

        else:
            return None
        docs = list(self.nlp.pipe(texts, disable=['ner']))
        for doc in docs:
            words = []
            for token in doc:
                tag = token.tag_.split("-")[0]
                # print(tag)
                if tag in self.independent_words:
                    # print(token.lemma_)
                    words.append(token.lemma_)
            indepent_list.append(words)
        
        return indepent_list

    
    def noun2normal(self, sen):
        normalize_sen = []
        docs = list(self.nlp.pipe(sen, disable=['ner']))
        for doc in docs:
            normalize_sen.append( [ token.tag_ if "名詞" in token.tag_ else token.lemma_ for token in doc ] )
        # for doc in docs:
        #     words = []
        #     for token in doc:
        #         tag = token.tag_.split("-")[0]
        #         # print(tag)
        #         if tag in ["名詞", "動詞"] :
        #             # print(token.lemma_)
        #             words.append(token.lemma_)
        #     normalize_sen.append(words)
        return normalize_sen
    
    def independent2normal(self, sen):
        normalize_sen = []
        docs = list(self.nlp.pipe(sen, disable=['ner']))
        for doc in docs:
            words = []
            for token in doc:
                tag = token.tag_.split("-")[0]
                # print(tag)
                if tag in self.independent_words:
                    # print(token.lemma_)
                    words.append(token.tag_)
                else:
                    words.append(token.lemma_)
            normalize_sen.append(words)
        return normalize_sen
    
    def noun_verb_2normal(self, sen):
        normalize_sen = []
        docs = list(self.nlp.pipe(sen, disable=['ner']))
        for doc in docs:
            words = []
            for token in doc:
                tag = token.tag_.split("-")[0]
                # print(tag)
                if tag in ["名詞", "動詞"]:
                    # print(token.lemma_)
                    words.append(token.tag_)
                else:
                    words.append(token.lemma_)
            normalize_sen.append(words)
        return normalize_sen
            
    
    def read_json_with_NoErr(self, path:str, datalist:list) -> pd.DataFrame:
        cols = ['did', 'tid', 'usr', 'sys', 'ec']
        df = pd.DataFrame(index=[], columns=cols)

        for p in datalist:
            datapath = Path(path + p + '/')
            for file in datapath.glob("*.json"):
                # print(file)
                with open(file, "r") as f:
                    json_data = json.load(f)
                    did = json_data["dialogue-id"]
                    for t in json_data["turns"]:
                        if t["turn-index"] == 0:
                            continue
                        if t["speaker"] == "U":
                            usr = t["utterance"]
                            continue
                        if t["speaker"] == "S" :
                            tid = t["turn-index"]
                            sys = t["utterance"]
                            if t["error_category"]:
                                ec = t["error_category"]
                            else:
                                ec = ["No-Err"]
                            df = df.append(pd.DataFrame([did, tid, usr, sys, ec], index = cols).T)
        df.reset_index(inplace=True, drop=True)
        return df
    
    def make_error_dict(self, error_types):
        error_dict = {}
        for e in error_types:
            error_dict[e] = len(error_dict)
        return error_dict
    
    def extract_X_y(self, df:pd.DataFrame, error_types, prev_num) -> np.array:
        # nlp = spacy.load('ja_ginza')
        
        did = df.did[0]
        n = prev_num
        # print(did)
        # 全体
        X_data = []
        y_data = []
        # 各 did 
        sequence_did = []
        y_did = []
        # エラーの辞書定義
        error_dict = self.make_error_dict(error_types)

        # 初期の調整 padding
        for i in range(n-1):
            sequence_did.append(
                np.concatenate( [np.zeros(self.emb_size), np.zeros(self.emb_size)])
            )

        # didごとに返却する？
        # エラーが発生したら、開始からエラーまでの文脈を入力とする(N=5の固定長でも可能)
        # 先にこのベクトル列を作成し，Tensorに変換して， List に保持
        for d, u, s, e in zip(df.did, df.usr, df.sys, df.ec):
            if did != d:
                did = d
                sequence_did = []
                y_did = []
                # 初期の調整 padding
                for i in range(n-1):
                    sequence_did.append(
                            np.concatenate( [np.zeros(self.emb_size), np.zeros(self.emb_size)])
                        )
                # break

            # sequence_did.append([u, s])
            sequence_did.append(
                    np.concatenate(
                        [self.get_sentence_vec(u), self.get_sentence_vec(s)]
                    )
                # [u, s]
            )
            if e[0] == "No-Err":
                continue
            else:
                y_each_error_label = np.zeros(len(error_types))
                for e_ in e:
                    y_each_error_label[error_dict[e_]] = 1
                X_data.append(sequence_did[-n:])
                # y_did = np.array(y_each_error_label)
                y_data.append(y_each_error_label)
        return np.array(X_data), np.array(y_data)


if __name__ == '__main__':
    texts = ['そうですね。',
 '最近とても暑いですから。',
 '休日に行きたいと思います。',
 'はい。',
 'あなたは海に行きますか？',
 '何故ですか？',
 'そうですか。',
 '山に行くのはどうでしょうか？',
 '山はお好きなのですか？',
 '山のおすすめのスポットはご存知ですか？',
 'どこに行くといいですか？',
 '明日はとても暑くなるみたいですね。',
 '涼しくなってきたら、一緒に山へ行きたいですね。']
    # texts = texts[0]
    pre = Preprocessor()
    pos = pre.get_POS(texts)
    print(pos)