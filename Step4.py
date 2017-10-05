import sys
import os
import re
from antlr4 import *
from firstLexer import firstLexer
from firstParser import firstParser
from firstListener import firstListener

class myFirstListener(firstListener):
    def __init__(self, **kwargs):
        self.scope = [] #list of all scopes
        self.blockNumber = 0 #keep track of block number
        self.varType = ""
        self.globalPrinter = [] #array of things to be printed
        self.isElseThere = 0 #checks if else is a part of if
        self.varArray = []
        self.operatorType = ''
        self.labelStack = []
        self.tinyPrinter = []
#######################################
        self.regNumber = 0
        self.operandStack = []
        self.expressionType = 'I' #integer or float
        self.variable = [['i','INT'],['a','INT'],['b','INT']]
        self.reqVar = 0
        self.labelNumber = 0
        return super().__init__(**kwargs)

    def enterProgram(self, ctx):
        self.globalPrinter.append(";IR CODE")
        self.globalPrinter.append(";LABEL main")
        self.globalPrinter.append(";LINK")
        self.tinyPrinter.append(";tiny code")
        return super().enterProgram(ctx)

    def enterAssign_expr(self,ctx):
        wow = ctx.toStringTree()
        wow = wow.replace('] ( (', '] { (')
        wow = wow.replace('] ) (', '] } (')
        wow = wow.replace(' )',' }')
        wow = wow.replace('(', ' ')
        wow = wow.replace(')', ' ')
        y = re.sub('\[(.*?)\]',' ',wow) #deleting everything between []
        z = re.sub("([\(\[]).*?([\)\]])", "\g<1>\g<2>", wow)
        z = re.sub('\[\]',' ' , z)
        z = y
        z = re.sub('{', '(', z)
        z = re.sub('}' , ')', z)
        #print(z) #############################COMMENTED
        self.operatorType = ':='
        self.expressionEval(z)
        return super().enterAssign_expr(ctx)

    def enterCond(self,ctx):
        wow = ctx.toStringTree()
        wow = wow.replace('] ( (', '] { (')
        wow = wow.replace('] ) (', '] } (')
        wow = wow.replace(' )',' }')
        wow = wow.replace('(', ' ')
        wow = wow.replace(')', ' ')
        y = re.sub('\[(.*?)\]',' ',wow) #deleting everything between []
        z = re.sub("([\(\[]).*?([\)\]])", "\g<1>\g<2>", wow)
        z = re.sub('\[\]',' ' , z)
        z = y
        z = re.sub('{', '(', z)
        z = re.sub('}' , ')', z)
        #print(z)
        if( ('<' in z) and ('<=' not in z)):
            self.operatorType = '<'
        elif( '>' in z and ('>=' not in z)):
            self.operatorType = '>'
        elif( '<=' in z):
            self.operatorType = '<='
        elif( '>=' in z):
            self.operatorType = '>='
        elif( '!=' in z ):
            self.operatorType = '!='
        elif( '=' in z and ('!=' not in z) and (':=' not in z)):
            self.operatorType = '='       
        else:
            pass
        self.expressionEval(z) #BE CAREFUL SINCE COMP OPERATORS ARE HERE
        return super().enterCond(ctx)

    def enterString_decl(self, ctx):
        wow = ctx.toStringTree() #string very helpful and gives everything stored in one variable
        x = re.findall((r'\"(.+?)\"'  ),wow) #find values stored in variable
        y = re.findall('[a-zA-Z]+[0-9]*',wow) #find variable names
        i = "name "+str(y[1])+" type STRING value "+"\""+str(x[0])+"\""
        needToPrint = 'str newline "\\n"'
        self.tinyPrinter.append(needToPrint)
        #self.globalPrinter.append(i)
        return super().enterString_decl(ctx)

    def enterVar_decl(self, ctx): #make a global tuple array which stores type and name and call it everytime WRITE or READ is done for I or F commands
         wow = ctx.toStringTree()
         x = re.findall('[a-zA-Z]+[0-9]*',wow)   
         if 'INT' in wow:
             self.varType = 'INT'
         if 'FLOAT' in wow:
             self.varType = 'FLOAT'
         del x[0]
         for i in x:
             k = "name "+i+" type "+self.varType
             self.tinyPrinter.append("var " + i)
             tempTuple = (i,self.varType)
             self.varArray.append(tempTuple)
         return super().enterVar_decl(ctx)

    def enterParam_decl(self,ctx):
         wow = ctx.toStringTree()
         x = re.findall('[a-zA-Z]+[0-9]*',wow)
         if 'INT' in wow:
             self.varType = 'INT'
         if 'FLOAT' in wow:
             self.varType = 'FLOAT'
         del x[0]
         for i in x:
             k = "name "+i+" type "+self.varType
             if ((k,self.scope[-1])) in self.globalPrinter:
                 print("DECLARATION ERROR "+i)
                 sys.exit()
             #self.globalPrinter.append((k,self.scope[-1]))
         return super().enterParam_decl(ctx)

    def enterFunc_decl(self,ctx):
         wow = ctx.toStringTree()
         lister = re.findall('[a-zA-Z]+[0-9]*',wow)
         self.scope.append(lister[2])
         i = "\nSymbol table "+self.scope[-1]
         #self.globalPrinter.append(i)
         return super().enterFunc_decl(ctx)

    def enterIf_stmt(self, ctx):
        self.blockNumber = self.blockNumber + 1 #increase block number
        x=ctx.toStringTree()
        lister = re.findall('[a-zA-Z]+[0-9]*',x)
        if 'ELSE' in lister: #need to check if IF has an ELSE with it
            self.isElseThere = 1
        else:
            self.isElseThere = 0
        element = "BLOCK " + str(self.blockNumber)
        self.scope.append(element)
        i = "\nSymbol table "+self.scope[-1]
        #self.globalPrinter.append(i)
        ###########################
        #self.labelNumber +=1
        #self.globalPrinter.append(";LABEL label"+str(self.labelNumber))
        #self.labelStack.append(self.labelNumber) #stack for label numbers #SERIOUSLY? CHANGED THIS
       # print("entered if")
        #print(self.labelStack)
        return super().enterIf_stmt(ctx)

    def enterElse_part(self, ctx):      
        if self.isElseThere == 1: #this only happens if there is an ELSE present in code
            self.blockNumber = self.blockNumber + 1
            element = "BLOCK " + str(self.blockNumber)
            self.scope.append(element)
            i = "\nSymbol table "+self.scope[-1]
            #self.globalPrinter.append(i)
            ############################
           # print("enterElse")
           # print(self.labelStack)
            second = self.labelStack.pop()
            #first = self.labelStack.pop()
            self.labelNumber +=1         
            self.globalPrinter.append(";JUMP label"+str(self.labelNumber))
            self.globalPrinter.append(";LABEL label" + str(second))
            self.labelStack.append(self.labelNumber)
           # print(self.labelStack)
        return super().enterElse_part(ctx)

    def exitIf_stmt(self,ctx):
        #print("exit if")
        first = self.labelStack.pop()
        self.globalPrinter.append(";LABEL label"+str(first))
      #  print(self.labelStack)
        return super().exitIf_stmt(ctx)

    def enterWhile_stmt(self, ctx):
        self.labelNumber +=1 
        self.globalPrinter.append(";LABEL label"+str(self.labelNumber))
        self.labelStack.append(self.labelNumber) #stack for label numbers
      #  print("enter while")
      #  print(self.labelStack)

        self.blockNumber = self.blockNumber + 1
        element = "BLOCK " + str(self.blockNumber)
        self.scope.append(element)
        i = "\nSymbol table "+self.scope[-1]
        #self.globalPrinter.append(i)
        return super().enterWhile_stmt(ctx)

    def exitWhile_stmt(self,ctx):
        #self.labelNumber +=1
      #  print("exit whike")
        
        second = self.labelStack.pop()
        first = self.labelStack.pop()
       # print(self.labelStack)
        self.globalPrinter.append(";JUMP label"+str(first))
        self.globalPrinter.append(";LABEL label" + str(second))
        return super().exitWhile_stmt(ctx)

    def enterWrite_stmt(self,ctx):
        wow = ctx.toStringTree()
        #print(wow)
        x = re.findall('[a-zA-Z]+[0-9]*',wow)   
        del(x[0])
        #print(x)
        i = 0
        if(len(x) == 1):
            #print("truueeeee")
            for varTuples in self.varArray:
                if x[0] == varTuples[0]:
                    if varTuples[1] == "FLOAT":
                        self.globalPrinter.append(";WRITEF " + x[0]) 
                    else:
                        self.globalPrinter.append(";WRITEI " + x[0]) 
        else:
            while(i<len(x)):
                if(i%2==0):
                    #print(self.varArray + "write")
                    for varTuples in self.varArray:
                        if x[i]  == varTuples[0]:
                            #print(variables + "ssss")
                            if varTuples[1] == "FLOAT":
                                self.globalPrinter.append(";WRITEF " + x[i]) 
                            else:
                                self.globalPrinter.append(";WRITEI " + x[i]) 
                else:
                    self.globalPrinter.append(";WRITES " + x[i])
                i = i+1
        return super().enterWrite_stmt(ctx)

    def enterRead_stmt(self,ctx):
        wow = ctx.toStringTree()
        #print(wow)
        x = re.findall('[a-zA-Z]+[0-9]*',wow)   
        del(x[0])
        #print(x)
        i=0
        while(i<len(x)):
            for varTuples in self.varArray:
                if x[i]  == varTuples[0]:
                    if varTuples[1] == "FLOAT":
                        self.globalPrinter.append(";READF " + x[i]) 
                    else:
                        self.globalPrinter.append(";READI " + x[i]) 
            i = i+1
        return super().enterRead_stmt(ctx)

    def exitProgram(self, ctx):
        self.globalPrinter.append(";RET")
        for i in self.globalPrinter:
            #pass
            print(i)
        for i in self.tinyPrinter:
            print(i) #everything now has been printed till variable declaration etc
        for i in self.globalPrinter:
            z = i.split()
            if(z[0] == ";LABEL"):
                print("label "+ z[1])
            elif((';STORE' in z[0]) and ( ('.' in z[1]) or z[1].isdigit()) and ('$T' in z[2]) ):  # STORE 0.0001 $T1 #STORE 4 $T4
                print("move " + z[1] + " r" + z[2].replace('$T',''))
            elif((';STORE' in z[0]) and z[1].isalpha() and z[2].isalpha() ):  # STORE num approx
                print("move " + z[1] + " r0" )
                print("move r0 "+ z[2] )
            elif((';STORE' in z[0]) and ('$T' in z[1]) and z[2].isalpha()): #STORE $T! tolerance
                print("move " + z[1].replace('$T','r') + " "+z[2])
            elif(z[0] == ";READI"):
                print("sys readi "+ z[1])
            elif(z[0] == ";READF"):
                print("sys readf "+ z[1])
            elif(z[0] == ";WRITEI"):
                print("sys writei "+ z[1])
            elif(z[0] == ";WRITEF"):
                print("sys writer "+ z[1])
            elif(z[0] == ";WRITES"):
                print("sys writes "+ z[1])
            elif(z[0] == ";JUMP"):
                print("jmp "+ z[1])
            elif(z[0] == ";DIVI"):
                z[3]=z[3].replace('$T','r')
                z[1]=z[1].replace('$T','r')
                z[2]=z[2].replace('$T','r')
                print("move " + z[1]+" "+z[3] )
                print("divi " + z[2]+" "+z[3])
            elif(z[0] == ";DIVF"):
                z[3]=z[3].replace('$T','r')
                z[1]=z[1].replace('$T','r')
                z[2]=z[2].replace('$T','r')
                print("move " + z[1]+" "+z[3] )
                print("divr " + z[2]+" "+z[3])
            elif(z[0] == ";MULTI"):
                z[3]=z[3].replace('$T','r')
                z[1]=z[1].replace('$T','r')
                z[2]=z[2].replace('$T','r')
                print("move " + z[1]+" "+z[3] )
                print("muli " + z[2]+" "+z[3])
            elif(z[0] == ";MULTF"):
                z[3]=z[3].replace('$T','r')
                z[1]=z[1].replace('$T','r')
                z[2]=z[2].replace('$T','r')
                print("move " + z[1]+" "+z[3] )
                print("mulr " + z[2]+" "+z[3])
            elif(z[0] == ";SUBI"):
                z[3]=z[3].replace('$T','r')
                z[1]=z[1].replace('$T','r')
                z[2]=z[2].replace('$T','r')
                print("move " + z[1]+" "+z[3] )
                print("subi " + z[2]+" "+z[3])
            elif(z[0] == ";SUBF"):
                z[3]=z[3].replace('$T','r')
                z[1]=z[1].replace('$T','r')
                z[2]=z[2].replace('$T','r')
                print("move " + z[1]+" "+z[3] )
                print("subr " + z[2]+" "+z[3])
            elif(z[0] == ";ADDI"):
                z[3]=z[3].replace('$T','r')
                z[1]=z[1].replace('$T','r')
                z[2]=z[2].replace('$T','r')
                print("move " + z[1]+" "+z[3] )
                print("addi " + z[2]+" "+z[3])
            elif(z[0] == ";ADDF"):
                z[3]=z[3].replace('$T','r')
                z[1]=z[1].replace('$T','r')
                z[2]=z[2].replace('$T','r')
                print("move " + z[1]+" "+z[3] )
                print("addr " + z[2]+" "+z[3])
            elif(z[0] == ";GTI"): #DONE
                print("cmpi " + z[1] + " r" + z[2].replace('$T',''))
                print("jgt " + z[3])
            elif(z[0] == ";GEI"): #DONE
                print("cmpi " + z[1] + " r" + z[2].replace('$T',''))
                print("jge " + z[3])
            elif(z[0] == ";LTI"):
                print("cmpi " + z[1] + " r" + z[2].replace('$T',''))
                print("jlt " + z[3])
            elif(z[0] == ";LEI"):
                print("cmpi " + z[1] + " r" + z[2].replace('$T',''))
                print("jle " + z[3])
            elif(z[0] == ";NEI"):
                print("cmpi " + z[1] + " r" + z[2].replace('$T',''))
                print("jne " + z[3])
            elif(z[0] == ";EQI" ): 
                print("cmpi " + z[1] + " r" + z[2].replace('$T',''))
                print("jeq " + z[3])
            elif(z[0] == ";GTF"): #DONE
                print("cmpr " + z[1] + " r" + z[2].replace('$T',''))
                print("jgt " + z[3])
            elif(z[0] == ";GEF" and z[1].isalpha() and z[2].isalpha()): #DONE
                print("cmpr " + z[1] + " " + z[2])
                print("jge " + z[3])
            elif(z[0] == ";GEF"): #DONE
                print("cmpr " + z[1] + " r" + z[2].replace('$T',''))
                print("jge " + z[3])
            elif(z[0] == ";LTF"):
                print("cmpr " + z[1] + " r" + z[2].replace('$T',''))
                print("jge " + z[3])
            elif(z[0] == ";LEF"):
                print("cmpr " + z[1] + " r" + z[2].replace('$T',''))
                print("jle " + z[3])
            elif(z[0] == ";NEF"):
                print("cmpr " + z[1] + " r" + z[2].replace('$T',''))
                print("jne " + z[3])
            elif(z[0] == ";EQF"): #DONE
                print("cmpr " + z[1] + " r" + z[2].replace('$T',''))
                print("jeq " + z[3])
            elif(z[0] == ";JUMP"):
                print("jmp "+z[1])
            else:
                pass
        print("sys halt")
        return super().exitProgram(ctx)
    ###################################################
    def expressionEval(self,infixexpr):
        prec = {}
        prec["*"] = 3
        prec["/"] = 3
        prec["+"] = 2
        prec["-"] = 2
        prec["("] = 1
        opStack = []
        postfixList = []
        #print(infixexpr + "dfdsf" + self.operatorType)
        self.reqVar = infixexpr.split(self.operatorType)[0].strip()
       # <' | '>' | '=' | '!=' | '<=' | '>=' 
        for i in self.varArray:
            if i[0]==self.reqVar:
                if i[1]=='FLOAT':
                    self.expressionType = 'F'
                else:
                    self.expressionType = 'I'
        infixexpr = infixexpr.split(self.operatorType)[1]
        tokenList = infixexpr.split()
        #self.globalPrinter.append(self.reqVar)
        if((len(tokenList) == 1) and (self.operatorType == ':=')): #need to add operatorType here
            if(tokenList[0].isdigit): #a := 5
                self.globalPrinter.append(";STOREI " + tokenList[0] + " $T"+ str(self.regNumber+1) )
                self.globalPrinter.append(";STOREI $T" + str(self.regNumber+1) + " "+ self.reqVar)
                self.regNumber+=1
            elif('.' in tokenList[0]):
                self.globalPrinter.append(";STOREF " + tokenList[0] + " $T"+ str(self.regNumber+1) )
                self.globalPrinter.append(";STOREI $T" + str(self.regNumber+1) + " "+ self.reqVar)
                self.regNumber+=1
            elif(tokenList.isalpha()):
                self.globalPrinter.append(";STORE" + self.expressionType+ " " + tokenList[0] + " " + self.reqVar )
            else:
                pass
        elif((len(tokenList) == 1) and ( tokenList[0].isdigit()) and (self.operatorType == '<')): #a<3 #DONE
           # print("lesser just")
            self.labelNumber +=1
            self.globalPrinter.append(";STOREI " + tokenList[0] + " $T" + str(self.regNumber+1))
            self.globalPrinter.append(";GEI "+self.reqVar + " $T"+ str(self.regNumber+1) + " label" + str(self.labelNumber))
            self.labelStack.append(self.labelNumber)
         #   print("<")
          #  print(self.labelStack)
            self.regNumber +=1
        elif((len(tokenList) == 1) and ( tokenList[0].isalpha()) and (self.operatorType == '<')): #diff < tolerance #DONE
          #  print("lesser just")
            self.labelNumber +=1
            self.globalPrinter.append(";GEF " +self.reqVar + " " + tokenList[0] + " label" + str(self.labelNumber))
            self.labelStack.append(self.labelNumber)
         #   print("<")
         #   print(self.labelStack)
        elif((len(tokenList) == 1) and (self.operatorType == '!=')): #DONE
          #  print("not equal")
            self.labelNumber +=1
            self.globalPrinter.append(";STOREI " + tokenList[0] + " $T" + str(self.regNumber+1))
            self.globalPrinter.append(";EQI "+self.reqVar + " $T"+ str(self.regNumber+1) + " label" + str(self.labelNumber))
            self.labelStack.append(self.labelNumber)
            self.regNumber +=1
         #   print("!=")
         #   print(self.labelStack)
        elif((len(tokenList) == 1) and (self.operatorType == '<=')): #DONE
         #   print("less than =")
            self.labelNumber +=1
            self.globalPrinter.append(";STOREI " + tokenList[0] + " $T" + str(self.regNumber+1))
            self.globalPrinter.append(";GT "+self.reqVar + " $T"+ str(self.regNumber+1) + " label" + str(self.labelNumber))
            self.labelStack.append(self.labelNumber)
            self.regNumber +=1
        #    print("<=")
         #   print(self.labelStack)
        elif((len(tokenList) == 1) and (self.operatorType == '>=')): #DONE
         #   print("GTE")
            self.labelNumber +=1
            self.globalPrinter.append(";STOREI " + tokenList[0] + " $T" + str(self.regNumber+1))
            self.globalPrinter.append(";LT "+self.reqVar + " $T"+ str(self.regNumber+1) + " label" + str(self.labelNumber))
            self.labelStack.append(self.labelNumber)
            self.regNumber +=1
         #   print(">=")
        #    print(self.labelStack)
        elif((len(tokenList) == 1) and (self.operatorType == '=')): #DONE
          #  print("==")
            #print("self.req"+self.reqVar)
            self.labelNumber +=1
            self.globalPrinter.append(";STOREI " + tokenList[0] + " $T" + str(self.regNumber+1))
            self.globalPrinter.append(";NEI "+self.reqVar + " $T"+ str(self.regNumber+1) + " label" + str(self.labelNumber))
            self.labelStack.append(self.labelNumber)
            self.regNumber +=1
         #   print("=")
         #   print(self.labelStack)
        elif((len(tokenList) == 1) and (tokenList[0].isdigit()) and (self.operatorType == '>')):  #diff >0
          #  print("greater just")
            self.labelNumber +=1
            self.globalPrinter.append(";STOREI " + tokenList[0] + " $T" + str(self.regNumber+1))
            self.globalPrinter.append(";LEI "+self.reqVar + " $T"+ str(self.regNumber+1) + " label" + str(self.labelNumber))
            self.labelStack.append(self.labelNumber)
            self.regNumber +=1
          #  print(">")
          #  print(self.labelStack)
        elif((len(tokenList) == 1) and ('.' in tokenList[0]) and (self.operatorType == '>')): #diff > 0.0
           # print("greater just")
            self.labelNumber +=1
            self.globalPrinter.append(";STOREF " + tokenList[0] + " $T" + str(self.regNumber+1))
            self.globalPrinter.append(";LEF "+self.reqVar + " $T"+ str(self.regNumber+1) + " label" + str(self.labelNumber))
            self.labelStack.append(self.labelNumber)
            self.regNumber +=1
          #  print(">")
         #   print(self.labelStack)
        elif((len(tokenList) == 5) and (tokenList[1]=='0.0') and (tokenList[3]=='tolerance') and (self.operatorType == '>')): #diff > 0.0 - tolerance
         #   print("greater just")
            self.labelNumber +=1
            self.globalPrinter.append(";STOREF " + tokenList[1] + " $T" + str(self.regNumber+1))
            self.globalPrinter.append(";LEF "+self.reqVar + " $T"+ str(self.regNumber+1) + " label" + str(self.labelNumber))
            self.labelStack.append(self.labelNumber)
            self.regNumber +=1
         #   print(">")
         #   print(self.labelStack)
        else:
            for token in tokenList:
                if token.isalpha():
                    postfixList.append(token)
                elif token.isdigit():
                    postfixList.append(token)
                elif('.' in token):
                    postfixList.append(token)
                elif token == '(':
                    opStack.append(token)
                elif token == ')':
                    topToken = opStack.pop()
                    while topToken != '(':
                        postfixList.append(topToken)
                        topToken = opStack.pop()
                else:
                    while (len(opStack)!=0) and \
                       (prec[opStack[-1]] >= prec[token]):
                          postfixList.append(opStack.pop())
                    opStack.append(token)

            while len(opStack)!=0:
                postfixList.append(opStack.pop())
            postfixExpr = " ".join(postfixList)
            #print(postfixExpr)
            self.postfixEval(postfixExpr)

    #NOTE NOTE NOTE NOTE
    #The code for infix to postfix was referred from http://interactivepython.org/courselib/static/pythonds/BasicDS/InfixPrefixandPostfixExpressions.html
    def postfixEval(self,postfixExpr):
        self.operandStack = []
        tokenList = postfixExpr.split()
        #print(tokenList)
        for token in tokenList:
            if token.isdigit() : #subs with regex expr
                self.operandStack.append(token) #self.operandStack.append(int(token))
            elif ('.' in token):
                self.operandStack.append(token)  #self.operandStack.append(float(token))
            elif token.isalpha():
                self.operandStack.append(token)
            else:
                #self.globalPrinter.append("operands below")
                #self.globalPrinter.append(self.operandStack)
                operand2 = self.operandStack.pop()
                operand1 = self.operandStack.pop()
                self.doMath(token,operand1,operand2)
        self.globalPrinter.append(";STORE" + self.expressionType + " $T" + str(self.regNumber) + " "+ self.reqVar) #FINAL ASSIGNMENT :=
        return self.operandStack.pop()

    def doMath(self,op, op1, op2):
        if op == "*":
            if(op1.isdigit() and op2.isalpha()):#int*var
                #self.globalPrinter.append("1")
                self.globalPrinter.append(";STOREI "+  op1+ " $T"+str(self.regNumber+1))#4here
                self.globalPrinter.append(";MULTI "+ "$T" + str(self.regNumber+1) + " "+ op1 + " $T" + str(self.regNumber+2))
                self.regNumber+=2
                self.operandStack.append("$T"+str(self.regNumber))
            elif(('.' in op1) and op2.isalpha()):#float*var
                #self.globalPrinter.append("2")
                self.globalPrinter.append(";STOREF "+ op1+ " $T"+str(self.regNumber+1))#4here
                self.globalPrinter.append(";MULTF "+ "$T" + str(self.regNumber+1) + " "+ op1 + " $T" + str(self.regNumber+2))
                self.regNumber+=2
                self.operandStack.append("$T"+str(self.regNumber))  
            elif(op1.isalpha() and op2.isalpha()):#var*var
                #self.globalPrinter.append("3")
                self.globalPrinter.append(";MULT" + self.expressionType + " "+ op1 + " "+ op2 + " "+ "$T"+ str(self.regNumber+1))
                self.regNumber+=1
                self.operandStack.append("$T"+str(self.regNumber))
            elif(('.' in op1) and ('$T' in op2)): #float*reg
                #self.globalPrinter.append("4")
                self.globalPrinter.append(";STOREF " + op1 + " $T" + str(self.regNumber+1))
                self.globalPrinter.append(";MULTF " + "$T" + str(self.regNumber+1) + " "+ op2 + " $T"+str(self.regNumber+2))
                self.regNumber+=2
                self.operandStack.append("$T"+str(self.regNumber))  
            elif(op1.isdigit() and ('$T' in op2)): #int*reg
                #self.globalPrinter.append("5")
                self.globalPrinter.append(";STOREI " + op1 + "$T" + str(self.regNumber+1))
                self.globalPrinter.append(";MULTI " + "$T" + str(self.regNumber+1) + " "+ op2 + " $T"+str(self.regNumber+2))
                self.regNumber+=2
                self.operandStack.append("$T"+str(self.regNumber))  
            elif(op1.isalpha() and ('$T' in op2)):# var*reg
                #self.globalPrinter.append("6")
                self.globalPrinter.append(";MULT" + self.expressionType + " "+ op1 + " "+ op2 + " "+ "$T"+ str(self.regNumber+1))
                self.regNumber+=1
                self.operandStack.append("$T"+str(self.regNumber))
            elif(('$T' in op1) and ('$T' in op2)): #reg*reg
                #self.globalPrinter.append("7")
                self.globalPrinter.append(";MULT" + self.expressionType+  " "+ op1 + " "+ op2 + " $T"+str(self.regNumber+1))
                self.regNumber+=1
                self.operandStack.append("$T"+str(self.regNumber))  
            else: #a*number not there?
                pass
        elif op == "/":
            if('$T' in op1): #register/a division
                self.globalPrinter.append(";DIVI $T"+ str(self.regNumber) + " "+ op2 + " $T"+str(self.regNumber+1))
                self.regNumber +=1
                self.operandStack.append("$T"+str(self.regNumber))
            else: #a/b division
                self.globalPrinter.append(";DIVF "+ op1 +" "+ op2 + " $T"+str(self.regNumber+1))
                self.regNumber +=1
                self.operandStack.append("$T"+str(self.regNumber))
        elif op == "+":
            if(('$T' in op1) and ('$T' in op2)):#reg + reg
                #self.globalPrinter.append("1")
                self.globalPrinter.append(";ADD" + self.expressionType + " " + op1 + " "+ op2 + " $T"+str(self.regNumber+1))
                self.regNumber +=1
                self.operandStack.append("$T"+str(self.regNumber))
            elif(op1.isdigit() and op2.isalpha()):#int + var
                #self.globalPrinter.append("2")
                self.globalPrinter.append(";STOREI " + op1 + " $T" + str(self.regNumber+1))
                self.globalPrinter.append(";ADDI $T" + str(self.regNumber+1) + " " + op2 + " $T" + str(self.regNumber+2))
                self.regNumber +=2
                self.operandStack.append("$T"+str(self.regNumber))
            elif(('.' in op1) and op2.isalpha()):# float+var
                #self.globalPrinter.append("3")
                self.globalPrinter.append(";STOREF " + op1 + " $T" + str(self.regNumber+1))
                self.globalPrinter.append(";ADDF $T" + str(self.regNumber+1) + " " + op2 + " $T" + str(self.regNumber+2))
                self.regNumber +=2
                self.operandStack.append("$T"+str(self.regNumber))
            elif(op1.isdigit() and ('$T' in op2)):#int + reg
                #self.globalPrinter.append("4")
                self.globalPrinter.append(";STOREI " + op1 + " $T" + str(self.regNumber+1))
                self.globalPrinter.append(";ADDI $T" + str(self.regNumber+1) +" "+ op2+" $T"+ str(self.regNumber+2))
                self.regNumber +=2
                self.operandStack.append("$T"+str(self.regNumber))
            elif(('.' in op1) and ('$T' in op2)):# float+ reg
                #self.globalPrinter.append("5")
                self.globalPrinter.append(";STOREF " + op1 + " $T" + str(self.regNumber+1))
                self.globalPrinter.append(";ADDF $T" + str(self.regNumber+1) +" "+ op2+" $T"+ str(self.regNumber+2))
                self.regNumber +=2
                self.operandStack.append("$T"+str(self.regNumber))
            elif(op1.isalpha() and op2.isdigit()):    #var + int OR
                #self.globalPrinter.append("6")
                self.globalPrinter.append(";STOREI " + op2 + " $T" + str(self.regNumber+1))
                self.globalPrinter.append(";ADDI " + op1 + " $T" + str(self.regNumber+1) + " $T" + str(self.regNumber+2))
                self.regNumber +=2
                self.operandStack.append("$T"+str(self.regNumber))
            elif(op1.isalpha() and ('.' in op2)):    #var + float
                #self.globalPrinter.append("7")
                self.globalPrinter.append(";STOREF " + op2 + " $T" + str(self.regNumber+1))
                self.globalPrinter.append(";ADDF " + op1 + " $T" + str(self.regNumber+1) + " $T" + str(self.regNumber+2))
                self.regNumber +=2
                self.operandStack.append("$T"+str(self.regNumber))
            elif(('$T' in op1) and op2.isdigit()):    #reg + int
                #self.globalPrinter.append("8")
                self.globalPrinter.append(";STOREF " + op2 + " $T" + str(self.regNumber+1))
                self.globalPrinter.append(";ADDF $T" + str(self.regNumber+1) +" "+ op1+" $T"+ str(self.regNumber+2))
                self.regNumber +=2
                self.operandStack.append("$T"+str(self.regNumber))
            elif(('$T' in op1) and ('.' in op2)):    #reg + float
                #self.globalPrinter.append("9")
                self.globalPrinter.append(";STOREF " + op2 + " $T" + str(self.regNumber+1))
                self.globalPrinter.append(";ADDF $T" + str(self.regNumber+1) +" "+ op1+" $T"+ str(self.regNumber+2))
                self.regNumber +=2
                self.operandStack.append("$T"+str(self.regNumber))
            elif(op1.isalpha() and ('$T' in op2)):    #var + reg
                #self.globalPrinter.append("10")
                self.globalPrinter.append(";ADD" + self.expressionType + " " + op1 + " "+ op2 + " $T" + str(self.regNumber+1))
                self.regNumber +=1
                self.operandStack.append("$T"+str(self.regNumber))
            elif(op2.isalpha() and ('$T' in op1)):    #reg + var
                #self.globalPrinter.append("11")
                self.globalPrinter.append(";ADD" + self.expressionType + " " + op1 + " "+ op2 + " $T" + str(self.regNumber+1))
                self.regNumber +=1
                self.operandStack.append("$T"+str(self.regNumber))
            elif(op1.isalpha() and op2.isalpha()):
                #self.globalPrinter.append("12")
                self.globalPrinter.append(";ADD" + self.expressionType + " " + op1 + " "+ op2+ " $T" + str(self.regNumber+1))
                self.regNumber +=1
                self.operandStack.append("$T"+str(self.regNumber))
            else:
                pass #where is var + var?
        elif(op == '-'):
            #self.globalPrinter.append("tree")
            if(('$T' in op1) and ('$T' in op2)):#reg + reg
                self.globalPrinter.append("1")
                self.globalPrinter.append(";SUB" + self.expressionType + " " + op1 + " "+ op2 + " $T"+str(self.regNumber+1))
                self.regNumber +=1
                self.operandStack.append("$T"+str(self.regNumber))
            elif(op1.isdigit() and op2.isalpha()):#int + var
                self.globalPrinter.append("2")
                self.globalPrinter.append(";STOREI " + op1 + " $T" + str(self.regNumber+1))
                self.globalPrinter.append(";SUBI " + "$T"+str(self.regNumber+1) + " " + op2 + " $T" + str(self.regNumber+2))
                self.regNumber +=2
                self.operandStack.append("$T"+str(self.regNumber))
            elif(('.' in op1) and op2.isalpha()):# float+var
                self.globalPrinter.append("3")
                self.globalPrinter.append(";STOREF " + op1 + " $T" + str(self.regNumber+1))
                self.globalPrinter.append(";SUBF $T" + str(self.regNumber+1) + " " + op2 + " $T" + str(self.regNumber+2))
                self.regNumber +=2
                self.operandStack.append("$T"+str(self.regNumber))
            elif(op1.isdigit() and ('$T' in op2)):#int + reg
                self.globalPrinter.append("4")
                self.globalPrinter.append(";STOREI " + op1 + " $T" + str(self.regNumber+1))
                self.globalPrinter.append(";SUBI $T" + str(self.regNumber+1) +" "+ op2+" $T"+ str(self.regNumber+2))
                self.regNumber +=2
                self.operandStack.append("$T"+str(self.regNumber))
            elif(('.' in op1) and ('$T' in op2)):# float+ reg
                self.globalPrinter.append("5")
                self.globalPrinter.append(";STOREF " + op1 + " $T" + str(self.regNumber+1))
                self.globalPrinter.append(";SUBF $T" + str(self.regNumber+1) +" "+ op2+" $T"+ str(self.regNumber+2))
                self.regNumber +=2
                self.operandStack.append("$T"+str(self.regNumber))
            elif(op1.isalpha() and op2.isdigit()):    #var + int OR
                self.globalPrinter.append("6")
                self.globalPrinter.append(";STOREI " + op2 + " $T" + str(self.regNumber+1))
                self.globalPrinter.append(";SUBI $T" + str(self.regNumber+1) + " " + op1 + " $T" + str(self.regNumber+2))
                self.regNumber +=2
                self.operandStack.append("$T"+str(self.regNumber))
            elif(op1.isalpha() and ('.' in op2)):    #var + float
                self.globalPrinter.append("7")
                self.globalPrinter.append(";STOREF " + op2 + " $T" + str(self.regNumber+1))
                self.globalPrinter.append(";SUBF " + str(self.regNumber+1) + " " + op1 + " $T" + str(self.regNumber+2))
                self.regNumber +=2
                self.operandStack.append("$T"+str(self.regNumber))
            elif(('$T' in op1) and op2.isdigit()):    #reg + int
                self.globalPrinter.append("8")
                self.globalPrinter.append(";STOREF " + op2 + " $T" + str(self.regNumber+1))
                self.globalPrinter.append(";SUBF $T" + str(self.regNumber+1) +" $T"+ op1+" $T"+ str(self.regNumber+2))
                self.regNumber +=2
                self.operandStack.append("$T"+str(self.regNumber))
            elif(('$T' in op1) and ('.' in op2)):    #reg + float
                self.globalPrinter.append("9")
                self.globalPrinter.append(";STOREF " + op2 + " $T" + str(self.regNumber+1))
                self.globalPrinter.append(";SUBF $T" + str(self.regNumber+1) +" "+ op1+" $T"+ str(self.regNumber+2))
                self.regNumber +=2
                self.operandStack.append("$T"+str(self.regNumber))
            elif(op1.isalpha() and ('$T' in op2)):    #var + reg 
                self.globalPrinter.append("10")
                self.globalPrinter.append(";SUB" + self.expressionType + " " + op1 + " "+ op2 + " $T" + str(self.regNumber+1))
                self.regNumber +=1
                self.operandStack.append("$T"+str(self.regNumber))
            elif(op2.isalpha() and ('$T' in op1)):    #reg + var
                self.globalPrinter.append("11")
                self.globalPrinter.append(";SUB" + self.expressionType + " " + op1 + " "+ op2 + " $T" + str(self.regNumber+1))
                self.regNumber +=1
                self.operandStack.append("$T"+str(self.regNumber))
            elif(('$T' in op1) and ('$T' in op2)): #reg-reg
                self.globalPrinter.append('12')#########CHECK ORDER
                self.globalPrinter.append(";SUB"+self.expressionType + " " + op1 + " "+ op2 + " $T"+str(self.regNumber+1))
                self.regNumber+=1
                self.operandStack.append("$T"+str(self.regNumber))
            elif(op1.isalpha() and op2.isalpha()):
                self.globalPrinter.append("13")
                self.globalPrinter.append(";SUB"+self.expressionType + " " + op1 + " "+ op2 + " $T"+str(self.regNumber+1))
                self.regNumber+=1
                self.operandStack.append("$T"+str(self.regNumber))
            elif(op1.isdigit() and op2.isdigit()): #int - int
                self.globalPrinter.append('14')
                self.globalPrinter.append(";STORE"+ self.expressionType+" "+ op1+ " $T"+str(self.regNumber+1))
                self.globalPrinter.append(";STORE"+ self.expressionType+" "+ op2+ " $T"+str(self.regNumber+2))
                self.globalPrinter.append(";SUB" + self.expressionType + " $T" + str(self.regNumber+1) + " $T"+ str(self.regNumber+2) + " $T" + str(self.regNumber+3))
                self.regNumber+=3
                self.operandStack.append("$T"+str(self.regNumber))
        else:
            pass

file = FileStream(sys.argv[1])
lexer = firstLexer(file)
stream = CommonTokenStream(lexer)
parser = firstParser(stream)
tree = parser.program()
printer = myFirstListener()
walker = ParseTreeWalker()
walker.walk(printer, tree)