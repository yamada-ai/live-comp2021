
from sklearn.linear_model import LogisticRegression

import sys
# sys.dont_write_bytecode = True
# sys.path.append('../')
from project.classifier.train import feature
from project.classifier.datatool import maneger
from project.classifier.datatool import preprocess
# from train.feature import Feature

sys.modules["feature"] = feature
sys.modules["manager"] = maneger
sys.modules["preprocess"] = preprocess

class Classifier:
    def __init__(self, model_path="./models/", F_path="./X_y_data/") -> None:
        self.model_path = model_path
        self.F_path = F_path
        self.modelM =maneger.DataManager(self.model_path)
        self.FM =  maneger.DataManager(self.F_path)

        self.remain_classes = "how what when where who why yn plain positive negative".split()
        self.classes_dict = dict(zip(self.remain_classes, list(range(len(self.remain_classes)))))


    
    def load_model(self, name="typeClassify_M2.pickle"):
        self.model = self.modelM.load_data(name)
    
    def load_F(self, name="typeClassify_F2.pickle"):
        self.F = self.FM.load_data(name)
        self.F.set_preprocessor(preprocess.Preprocessor())
    
    def predict_type(self, mode, text):
        f = self.F.featurization(text)
        y = self.model.predict(f.reshape(1, -1))
        if self.classes_dict[mode] == y:
            return True
        else:
            return False

if __name__ == "__main__":
    print("start")
    classsifier = Classifier()
    classsifier.load_model()
    classsifier.load_F()

    print(classsifier.predict_type(mode="yn", text="それは正しいものですか？"))
    
