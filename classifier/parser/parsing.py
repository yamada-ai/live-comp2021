
from ast import parse
from lexical import Tokenizer
from lexical import Token
from enum import IntEnum, auto

class Stack:
    def __init__(self) -> None:
        self.stack = []
    
    def push(self, item):
        self.stack.append(item)
    
    def pop(self):
        if len(self.stack) == 0:
            return None
        return self.stack.pop()

# class MidValue:
#     def __init__(self, m_type, value) -> None:
#         self.m_type = m_type
#         self.value = value
    
class Ltype(IntEnum):
    INT = auto()
    BOOL = auto()
    STRING = auto()

    ArINT = auto()
    ArBOOL = auto()
    ArSTRING = auto()

class CulcParser:

    def __init__(self) -> None:
        self.LA = Tokenizer()
        self.TNUM_func = lambda n: self.tname2TNUM(n)

        self.constant_t = set( map(self.TNUM_func,  "TNUMBER TSTRING True False [".split() ) )
        self.func_name = set( map(self.TNUM_func, "in count re".split()) )
        self.multi_op = set( map( self.TNUM_func, "* / and".split() ) )
        self.add_op = set( map( self.TNUM_func, "+ - or".split() ))
        self.relation_op = set( map(self.TNUM_func, "= < > <= >=".split()) )
        self.val_stack = Stack()
        
        
    def parsing(self, code):
        res = self.LA.lexical_analyze(code)
        if res < 0:
            print("failure Lexical Analyze")
            return -1

        self.token = self.next_token()
        self.condition_statement()
        return self.val_stack.pop()
    
    # "if" -> 0
    def tname2TNUM(self, tname):
        return self.LA.tname2TNUM(tname)
    
    def next_token(self):
        return self.LA.next_token()

    # if statement
    def condition_statement(self):
        if self.token != self.tname2TNUM("if"):
            print("keyword 'if' is not found")
            return -1
        

    def expression(self):
        
        simple1 = self.simple_expression()
        relation = -1
        if simple1 == -1:
            print("expression error : syntax error in simple_exp")
            return -1
        
        while self.token in self.relation_op:
            op = self.token
            relation = self.relational_operator()

            simple2 = self.simple_expression()
            if simple2 == -1:
                print("expression error : syntax error in simple_exp")
                return -1
            
            if simple1 != simple2:
                print("expression error : type was not corrected")
            
            v2 = self.val_stack.pop()
            v1 = self.val_stack.pop()
            if op == self.tname2TNUM("="):    
                value = v1 == v2
            elif op == self.tname2TNUM("<"):    
                value = v1 < v2
            elif op == self.tname2TNUM(">"): 
                value = v1 > v2
            elif op == self.tname2TNUM("<="):    
                value = v1 <= v2
            else:
                value = v1 <= v2
            self.val_stack.push(value)
        
        if relation < 0:
            return simple1
        else:
            return relation

    
    def simple_expression(self):
        
        is_minus = False
        is_exist_head_op = False
        if self.token == self.tname2TNUM("+") or self.token == self.tname2TNUM("-"):
            is_exist_head_op = True
            if self.token == self.tname2TNUM("-"):
                is_minus = True
            self.token = self.next_token()

        term1 = self.term()
        if term1 == -1:
            print("simple_exp error : syntax error in factor")
            return -1
        
        if is_exist_head_op and term1 != Ltype.INT:
            print("simple_exp error : The type must be Integer")
            return -1
        
        if is_minus:
            term1_v = self.val_stack.pop()
            self.val_stack.push( -1*term1_v )

        while self.token in self.add_op:
            op = self.token
            add = self.additive_operator()
            term2 = self.term()

            if term2 == -1:
                print("simple_exp error : syntax error in factor")
                return -1
            
            # print(term1, add, term2)
            if not( 
                (term1==add and  term1==term2) and 
                (term1==Ltype.INT or term1==Ltype.BOOL)) :
                    print("simple_exp error: The type must be Integer or Boolean and all the same type")
                    return -1
            # culc
            v2 = self.val_stack.pop()
            v1 = self.val_stack.pop()
            if op == self.tname2TNUM("+"):    
                value = v1 + v2
            elif op == self.tname2TNUM("-"):    
                value = v1 - v2
            else:
                value = v1 or v2
            self.val_stack.push(value)
            # culc

        return term1

    def term(self):
        factor1 = self.factor()
        if factor1 == -1:
            print("term error : syntax error in factor")
            return -1
        
        while self.token in self.multi_op:
            op = self.token
            multiple = self.multiplicative_operator()

            factor2 = self.factor()
            if factor2 == -1:
                print("term error : syntax error in factor")
                return -1
            
            if not( 
                (factor1==multiple and  factor1==factor2) and 
                (factor1==Ltype.INT or factor1==Ltype.BOOL)) :
                    print("term error: The type must be Integer or Boolean and all the same type")
                    return -1
            # culc
            v2 = self.val_stack.pop()
            v1 = self.val_stack.pop()
            if op == self.tname2TNUM("*"):    
                value = v1 * v2
            elif op == self.tname2TNUM("/"):    
                value = int(v1 / v2)
            else:
                value = v1 and v2
            self.val_stack.push(value)
            # culc

        return factor1
            
    def factor(self):
        
        if self.token in self.constant_t:
            result = self.constant()
            return result

        elif self.token == self.tname2TNUM("("):
            # print(self.token)
            self.token = self.next_token()
            # print(self.token)
            # return -1
            result = self.expression()
            if result == -1:
                print("factor error :'(' expresion ')' ")
                return -1
            if self.token != self.tname2TNUM(")"):
                print("factor error :')' is not found")
                return -1
            self.token = self.next_token()
            return result
        
        elif self.token == self.tname2TNUM("not"):
            self.token = self.next_token()
            result = self.factor()
            if result == -1:
                print("factor error :'not' factor ")
                return -1
            if result != Ltype.BOOL:
                print("The type of factor must be Boolean")
                return -1
            # culc
            factor_v = self.val_stack.pop()
            self.val_stack.push( not factor_v)
            # 
            return result
        
        # function zone
        elif self.token in self.func_name:
            if self.token == self.tname2TNUM("in"):
                result = self._in()
        
        else:
            print("factor error : unknown")
            return -1

            
    def constant(self):
        if self.token == self.tname2TNUM("TNUMBER"):
            value = int(self.token.surface)
            self.token = self.next_token()
            self.val_stack.push(value)
            return Ltype.INT
        
        elif self.token == self.tname2TNUM("False"):
            value = False
            self.token = self.next_token()
            self.val_stack.push(value)
            return Ltype.BOOL
        
        elif self.token == self.tname2TNUM("True"):
            value = True
            self.token = self.next_token()
            self.val_stack.push(value)
            return Ltype.BOOL
        
        elif self.token == self.tname2TNUM("TSTRING"):
            value = self.token.surface
            self.token = self.next_token()
            self.val_stack.push(value)
            return Ltype.STRING
        
        # Array
        elif self.token == self.tname2TNUM("["):
            value = []
            self.token = self.next_token()
            # print(self.token)
            result = self.expression()
            if result == -1:
                print("constant error : Array expression() ")
                return -1
            if result in [Ltype.ArINT, Ltype.ArBOOL, Ltype.ArSTRING]:
                print("constant error : Array.dim is not allowed to be more than 2")
                return -1
            # v = self.val_stack.pop()
            value.append(self.val_stack.pop())

            while self.token == self.tname2TNUM(","):
                self.token = self.next_token()
                result2 = self.expression()
                if result != result2:
                    print("constant error : element of Array type error")
                    return -1
                value.append(self.val_stack.pop())
            
            if self.token != self.tname2TNUM("]"):
                print("constant error : ']' of Array is requred")
                return -1
            
            self.val_stack.push(value)
            self.token = self.next_token()
            if result == Ltype.INT:
                return Ltype.ArINT
            elif result == Ltype.BOOL:
                return Ltype.ArBOOL
            else:
                return Ltype.ArSTRING


    def multiplicative_operator(self)  -> Ltype:
        if self.token == self.tname2TNUM("*") or self.token == self.tname2TNUM("/"):
            self.token = self.next_token()
            return Ltype.INT
        else:
            self.token = self.next_token()
            return Ltype.BOOL
    
    def additive_operator(self) -> Ltype:
        if self.token == self.tname2TNUM("+") or self.token == self.tname2TNUM("-"):
            self.token = self.next_token()
            return Ltype.INT
        else:
            self.token = self.next_token()
            return Ltype.BOOL
    
    def relational_operator(self) -> Ltype:
        self.token = self.next_token()
        return Ltype.BOOL
    

    def _in(self):
        self.token = self.next_token()
        if self.token != self.tname2TNUM("("):
            print("in : '(' is required")
            return -1
        
        self.token = self.next_token()
        arg1_t = self.expression()

        

        element_t = None
        if arg1_t in [Ltype.ArINT, Ltype.ArBOOL, Ltype.ArSTRING]:
            if arg1_t == Ltype.ArBOOL:
                element_t = Ltype.BOOL
            elif arg1_t == Ltype.ArSTRING:
                element_t = Ltype.STRING
            else:
                element_t = Ltype.INT

        # print(self.token)
        if self.token != self.tname2TNUM(","):
            print("in : ',' is required")
            return -1

        self.token = self.next_token()
        arg2_t = self.expression()

        if arg2_t in [Ltype.ArINT, Ltype.ArBOOL, Ltype.ArSTRING]:
            print("in error : arg2 is not allowd to be Array type")
            return -1
        
        # arg1 = Array type
        if element_t:
            if element_t != arg2_t:
                print("in error : the element of arg1 and arg2 are not same type ")
                return -1
        else:
            if arg1_t != arg2_t:
                print("in error : arg1 and arg2 are not same type ")
                return -1

        arg2 = self.val_stack.pop()
        arg1 = self.val_stack.pop()

        self.val_stack.push( self._in_func(arg1, arg2) )

        if self.token != self.tname2TNUM(")"):
            print("in : ')' is required")
            return -1
    
    def _in_func(self, arg1, arg2):
        result = False
        if isinstance(arg1, list):
            for element in arg1:
                if isinstance(element, str):
                    if element in arg2:
                        result = True
                        break
                else:
                    if element == arg2:
                        result = True
                        break
        else:
            if isinstance(arg1, str):
                if arg1 in arg2:
                    result = True
            else:
                if arg1 == arg2:
                    result = True
        return result


if __name__ == "__main__":
    print("start")
    code = ' 5/2 + 10 + 3 > 0'
    code = 'if in( ["aa", "b", "c"] , "aa" ):'
    parser = CulcParser()
    result = parser.parsing(code)
    print(result)
    # print(parser.LA.display_tokens())
    # parser.expression()
    # print(parser.val_stack.stack)

    # func = lambda n: parser.tname2TNUM(n)
    # tnum_s = set( map(func,  "TNUMBER TSTRING True False".split() ) )
    # print(tnum_s)