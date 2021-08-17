import os
import sys

from spacy.util import normalize_slice
# sys.dont_write_bytecode = True
# sys.path.append('../')
from ..tools import preprocess

import pprint
import random
import numpy as np

class Feature:
    def __init__(self) -> None:
        self.pre = preprocess.Preprocessor()

        # 用いる素性テンプレート(関数名)
        self.feature_types = [
            self.f_pos_order, 
            self.f_normalize_noun_order
        ]
        self.features = {}
        self._init_feature_functions()

        # 句点を50%で削除する
        self.delete_func = lambda L: L[:-1] if (L[-1] == "補助記号-句点" and random.random() > 0.5) else L
        # FOS, EOS で囲む
        self.filler_func = lambda L: ["FOS", *L, "EOS"]
    
    def _init_feature_functions(self):
        for type_ in self.feature_types:
            type_name = type_.__name__
            self.features[type_name] = set()

    def make_features(self, sentence, len_=3):
        for feature_func in self.feature_types:
            type_name = feature_func.__name__
            features = feature_func(sentence, len_)
            self.features[type_name].update(features)
            # for sentence in sentence_list:
        
        self.numbering_features()
                
    def numbering_features(self):
        self.feature_number_dict = {}
        for feature_func in self.feature_types:
            type_name = feature_func.__name__
            for f in self.features[type_name]:
                self.feature_number_dict[f] = len(self.feature_number_dict)
        self.feature_num = len(self.feature_number_dict)


    def featurization(self, sentence, len_=3):
        if isinstance(sentence, str):
            sentence = [sentence]
        x = np.zeros( self.feature_num )
        for feature_func in self.feature_types:
            type_name = feature_func.__name__
            features = feature_func(sentence, len_)
            for f in features:
                if f in self.feature_number_dict.keys():
                    x[self.feature_number_dict[f]] = 1
        return x


    def f_pos_order(self, sentence, len_=3):
        # 素性タイプ名
        type_ = self.f_pos_order.__name__

        pos = self.pre.get_POS(sentence)
        # 句読点の句点を50%で削除
        random_deleted = map(self.delete_func, pos)
        filled = map(self.filler_func, random_deleted)
        
        feature_set = set()
        for L in filled:
            for i in range(len(L)-len_+1):
                f = "_".join(L[i:i+len_])
                # self.features[type_].add(f)
                feature_set.add(f)
        return feature_set
    
    def f_normalize_noun_order(self, sentence, len_=3):
        type_ = self.f_normalize_noun_order.__name__

        normal = self.pre.noun2normal(sentence)
        random_deleted = map(self.delete_func, normal)
        filled = map(self.filler_func, random_deleted)

        feature_set = set()
        for L in filled:
            for i in range(len(L)-len_+1):
                f = "_".join(L[i:i+len_])
                # self.features[type_].add(f)
                feature_set.add(f)
        return feature_set

    def show_features(self):
        for type_ in self.feature_types:
            type_name = type_.__name__
            print("feature type : {0}, nums : {1}".format(type_name, len(self.features[type_name])))
            # pprint.pprint(self.features[type_name])

            for f in self.features[type_name]:
                print("{0} : {1}".format(self.feature_number_dict[f], f))
            print()




if __name__ == '__main__':
    texts = ['そうですね。最近とても暑いですから。', '休日に行きたいと思います。']
#     texts = ['そうですね。',
#  '最近とても暑いですから。',
#  '休日に行きたいと思います。',
#  'はい。',
#  'あなたは海に行きますか？',
#  '何故ですか？',
#  'そうですか。',
#  '山に行くのはどうでしょうか？',
#  '山はお好きなのですか？',
#  '山のおすすめのスポットはご存知ですか？',
#  'どこに行くといいですか？',
#  '明日はとても暑くなるみたいですね。',
#  '涼しくなってきたら、一緒に山へ行きたいですね。']
    # texts = texts[0]
    F = Feature()
    # pos = features.f_pos_order(texts)
    # normal = features.f_normalize_noun_order(texts)
    F.make_features(texts)
    F.show_features()
