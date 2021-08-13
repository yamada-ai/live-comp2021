import re
from sre_constants import NOT_LITERAL

class Token:
    def __init__(self, TNUM, surface) -> None:
        self.surface = surface
        self.TNUM = TNUM
    
    def __str__(self) -> str:
        return "TNUM : {0}, surface : {1}".format(self.TNUM, self.surface)
    
    def __eq__(self, o: object) -> bool:
        if isinstance(o, Token):
            return self.TNUM == o.TNUM
        elif isinstance(o, int):
            return self.TNUM == o
        elif isinstance(o, str):
            return self.surface == o
        else:
            return NotImplemented
        
    def __hash__(self) -> int:
        return self.TNUM

    
    def get_surface(self):
        return self.surface
    
    def get_TNUM(self):
        return self.TNUM
    
    def get_data(self):
        return self.surface, self.TNUM
    
    

class Tokenizer:
    def __init__(self) -> None:
        self.keywords = "if and or not True False count in re".split()
        self.symbols = "+ - * / = <= >= < > ( ) : , [ ]".split()
        self.TTOKEN = "TNUMBER TSTRING TSKIP".split()

        self.unique_symbol = set("+ - * / = ( ) : , [ ]".split())

        self._make_TNUM_dict()
    
    def _make_TNUM_dict(self) -> None:
        self.TNUM_dict = {}
        TNUM_element = self.keywords + self.symbols + self.TTOKEN
        for element in TNUM_element:
            self.TNUM_dict[element] = len(self.TNUM_dict)

    def lexical_analyze(self, code : str) -> int:
        self.code = code + "$"
        self.tokens = []
        self.current_c = " "
        while not self._is_end_code():
            TNUM, surface = self.read()
            if TNUM < 0:
                print("syntax error")
                return -1
            if TNUM == self.TNUM_dict["TSKIP"]:
                continue
            self.tokens.append(Token(TNUM, surface))
        self.tokens_len = len(self.tokens)
        self.token_i = 0
        return 1 

    def next_token(self) -> Token:
        if self.token_i < self.tokens_len:
            token = self.tokens[self.token_i]
            self.token_i += 1
            return token
        else:
            return None

    def tname2TNUM(self, tname : str) -> int:
        return self.TNUM_dict[tname]
    
    def _is_end_code(self) -> bool:
        return self.code == ""

    def _next_char(self) -> str:
        c = self.code[0]
        self.current_c = c
        self.code = self.code[1:]
        return c

    def _get_current_c(self) -> str:
        return self.current_c    

    def read(self):
        # if self._is_end_code():
        #     return -1, None

        c = self._get_current_c()
        buffer = ""
        # keyword
        if c.isalpha():
            buffer += c
            while 1:
                c = self._next_char()
                if self._is_end_code():
                    break
                # not allow NAME , only keywords
                elif c.isalpha():
                    buffer += c
                else:
                    break
            # keywords
            if buffer in self.keywords:
                return self.TNUM_dict[buffer], buffer
            else:
                print("{0} is not keyword".format(buffer))
                return -1, buffer
        
        # integer
        elif c.isdecimal():
            buffer += c
            while 1:
                c = self._next_char()
                if self._is_end_code():
                    break
                elif c.isdecimal():
                    buffer += c
                else:
                    break
            return self.TNUM_dict["TNUMBER"], buffer

        # plain string
        elif c == '"':
            while 1:
                c = self._next_char()
                if self._is_end_code():
                    print("{0} of the end is required".format('"'))
                    return -1, None
                elif c == '"':
                    c = self._next_char()
                    return self.TNUM_dict["TSTRING"], buffer
                else:
                    buffer += c
        
        # symbol
        elif c in self.symbols:
            buffer += c
            c = self._next_char()
            # unique symbol (ex. "+", "-")
            if buffer in self.unique_symbol:
                return self.TNUM_dict[buffer], buffer
            else:
                if buffer == "<":
                    if c == "=":
                        buffer += c
                        return self.TNUM_dict[buffer], buffer
                    else:
                       return self.TNUM_dict[buffer], buffer

                elif buffer == ">":
                    if c == "=":
                        buffer += c
                        return self.TNUM_dict[buffer], buffer
                    else:
                       return self.TNUM_dict[buffer], buffer
                else:
                    return -1, None
        
        elif c == " " or c == "\t":
            c = self._next_char()
            while c == " " or c == "\t":
                c = self._next_char()
                if self._is_end_code():
                    return self.TNUM_dict["TSKIP"], None
            return self.TNUM_dict["TSKIP"], None

        else:
            print("{0} : unknown char".format(c))
            return -1, None

    def display_tokens(self) -> None:
        for token in self.tokens:
            print(token)

if __name__ == "__main__":
    print("start")
    code = '[2 ,3 ,4]'
    # code = "abcdefghijk"

    LA = Tokenizer()
    print(LA.TNUM_dict)
    LA.lexical_analyze(code)
    LA.display_tokens()