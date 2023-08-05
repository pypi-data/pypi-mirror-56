
 #  Copyright 2019  Dialect Software LLC or its affiliates. All Rights Reserved.
 #
 #  Licensed under the MIT License (the "License").
 #
 #  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 #  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 #  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 #  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 #  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 #  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 #  SOFTWARE.import pylingo
 
import lexee
import json
import base64
import sys

class LexeeWriter:
    braces = []

    @staticmethod
    def save(path, lexeeDoc:lexee.LexeeDoc):
        file = open(path,"w") 
        LexeeWriter.writeConfig(file, lexeeDoc.config)
        [LexeeWriter.writeImport(file, lexeeDoc.imports[key]) for key in lexeeDoc.imports.keys()]
        [LexeeWriter.writeExpression(file, expression) for expression in lexeeDoc.doc]

    @staticmethod
    def writeConfig(file, config:dict): 
        print("config", end=" {", file=file)
        LexeeWriter.braces.append("\t")
        print("")
        for key in [key for key in config.__dict__.keys() if key not in ["identity","current","depends_on"]] :
            print("".join(LexeeWriter.braces), end=key, file=file)
            print(" =", end=" ", file=file)
            print(json.dumps(config.__dict__[key], indent=5), file=file)
        print("".join(LexeeWriter.braces), end="", file=file)
        LexeeWriter.braces.pop()
        print("}", file=file)
        print("", file=file)

    @staticmethod
    def writeImport(file, symbol:lexee.symbol.Symbol): 
        print(symbol.name, end=" ", file=file)
        print(" ".join(symbol.identity), end=" {", file=file)
        LexeeWriter.braces.append("\t")
        print("", file=file)
        for key in [key for key in symbol.__dict__.keys() if key not in ["name","identity","current","depends_on"]] :
            if(key == "module"):
                print("".join(LexeeWriter.braces), end=key, file=file)
                print(" =", end=" ", file=file)
                print("\"" + symbol.__dict__[key].__name__ + "\"", file=file)
            else:
                print("".join(LexeeWriter.braces), end=key, file=file)
                print(" =", end=" ", file=file)
                print(json.dumps(symbol.__dict__[key], indent=5), file=file)
        print("".join(LexeeWriter.braces), end="", file=file)
        LexeeWriter.braces.pop()
        print("}", file=file)
        print("", file=file)

    @staticmethod
    def writeExpression(file, expression:lexee.expression.LexeeExpression): 
        print(expression.symbol.name, end=" ", file=file)
        print(" ".join(expression.symbol.identity), end=" {", file=file)
        LexeeWriter.braces.append("\t")
        print("", file=file)
        for key in [key for key in expression.__dict__.keys() if key not in ["id","symbol","proxy","output"]] :
            print("".join(LexeeWriter.braces), end=key, file=file)
            print(" =", end=" ", file=file)
            print(json.dumps(expression.__dict__[key], indent=5), file=file)
        print("".join(LexeeWriter.braces), end="output", file=file)
        print(" =", end=" ", file=file)
        print(json.dumps(expression.__dict__["output"], cls=BinEncoder), file=file)
        LexeeWriter.braces.pop()
        print("}", file=file)
        print("", file=file)


class BinEncoder(json.JSONEncoder):
    def encode(self, obj):    
        if isinstance(obj, bytes):
            return json.JSONEncoder.encode(self, obj.decode("utf-8"))
        if isinstance(obj, list):
            return "[" + ",".join([self.encode(item) for item in obj]) + "]"
        if isinstance(obj, str):
            return json.JSONEncoder.encode(self, obj)
        return json.JSONEncoder.encode(self, obj)
