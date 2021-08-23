
# from parse import parsing
# from parse import lexical
import parse

class Controller:
    def __init__(self) -> None:
        self.parser = parse.CulcParser()


if __name__ == "__main__":
    print("start")
    code = 'if in( "うざい", usr[-1] )'
    # code = "if "

    cont = Controller()
    print(cont.parser.parsing(code))