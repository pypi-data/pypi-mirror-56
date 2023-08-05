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
 #  SOFTWARE.
 
import sys
import lexee
import inspect
import importlib
from antlr4 import *
from lexee.symbols.config import Config
from antlr4.tree.Tree import TerminalNodeImpl
from protolingo.utils import load_classes, load_all_modules_from_dir
from pylingo.pylingoParser import pylingoParser
from pylingo.pylingoVisitor import pylingoVisitor

class Interpreter(pylingoVisitor):
    def __init__(self):
        self.symbols = []

    def visitLexee(self, ctx:pylingoParser.LexeeContext):
        return super().visitChildren(ctx)
    
    def visitPreamble(self, ctx:pylingoParser.PreambleContext):
        if(ctx.ident()):
            result = self.visitChildren(ctx)
            self.symbols[-1].identity.extend([child.getText().strip('"') for child in ctx.getChildren()] [1::])
        else:
            current = {}
            if(self.symbols[-1].current):
                self.symbols[-1].current[-1][ctx.getText()] = current
            else:
                setattr(self.symbols[-1], ctx.getText(), current)
            self.symbols[-1].current.append(current)
            result = self.visitChildren(ctx)
        return result

    def visitIdent(self, ctx:pylingoParser.IdentContext):
        module = importlib.import_module("lexee.symbols.%s" % ctx.getText())
        symbol = getattr(module, ctx.getText().capitalize())
        self.symbols.append(symbol(ctx.getText()))
        return self.visitChildren(ctx)
    
    def visitCode(self, ctx:pylingoParser.CodeContext):
        result = self.visitChildren(ctx)
        if(self.symbols[-1].current):
            self.symbols[-1].current.pop()
        return result

    def visitObj (self, ctx:pylingoParser.ObjContext):
        if(isinstance(ctx.parentCtx.getChild(0), TerminalNodeImpl)):
            key = ctx.parentCtx.getChild(0).getText().strip('"')
            return self.visitContext(key, {}, ctx)
        return self.visitChildren(ctx)
    
    def visitBody (self, ctx:pylingoParser.BodyContext):
        return self.visitChildren(ctx)

    def visitVariable (self, ctx:pylingoParser.VariableContext):
        return self.visitChildren(ctx)

    def visitAssignment(self, ctx:pylingoParser.AssignmentContext):
        return self.visitChildren(ctx)
        
    def visitArray (self, ctx:pylingoParser.ArrayContext):
        key = ctx.parentCtx.parentCtx.getChild(0).getText().strip('"')
        return self.visitContext(key, [], ctx)
       
    #def visitDoc(self, ctx:pylingoParser.DocContext):
    #    if(isinstance(ctx.parentCtx.parentCtx.getChild(0), pylingoParser.VariableContext)):
    #        key = ctx.parentCtx.parentCtx.getChild(0).getText().strip('"')
    #        return self.visitContext(key, {}, ctx)
    #    return  self.visitChildren(ctx)
       
    def visitJson(self, ctx:pylingoParser.JsonContext):
        if(isinstance(ctx.parentCtx.parentCtx.getChild(0), pylingoParser.VariableContext)):
            key = ctx.parentCtx.parentCtx.getChild(0).getText().strip('"')
            return self.visitContext(key, {}, ctx)
        if(isinstance(ctx.parentCtx.parentCtx.getChild(0), pylingoParser.ArrayContext)):
            return self.visitContext(None, {}, ctx)
        return  self.visitChildren(ctx)

    def visitValue(self, ctx:pylingoParser.ValueContext):
        if(isinstance(ctx.parentCtx.parentCtx.getChild(0), pylingoParser.VariableContext)):
            if(ctx.getToken(pylingoParser.DOCUMENT,0)):
                value = ctx.getText()[5:-3]
            else:
                value = ctx.getText().strip('"')
            key = ctx.parentCtx.parentCtx.getChild(0).getText().strip('"')
            if(self.symbols[-1].current):
                self.symbols[-1].current[-1][key] = value
            else:
                setattr(self.symbols[-1], key, value)
        else:
            value = ctx.getText()
            key = ctx.parentCtx.parentCtx.parentCtx.getChild(0).getText().strip('"')
            if(self.symbols[-1].current):
                [self.symbols[-1].current[-1].append(value) for value in self.visitArrayElements(value)] 
            else:
                [getattr(self.symbols[-1],key).append(value) for value in self.visitArrayElements(value)]

        return self.visitChildren(ctx)
    
    def visitContext(self, key, current, ctx):
        if(self.symbols[-1].current):
            if(type(self.symbols[-1].current[-1]) is list):
                self.symbols[-1].current[-1].append(current)
            else:
                self.symbols[-1].current[-1][key] = current
        else:
            setattr(self.symbols[-1], key, current)

        self.symbols[-1].current.append(current)
        result = self.visitChildren(ctx)
        self.symbols[-1].current.pop()
        return result

    def visitArrayElements(self, value):
          slices = [ i for i, txt in enumerate(value) if txt == "," and value[i-1] == "\"" and value[i-2] != "\\" ]
          slices.append(len(value))
          return [ value[0:x-1].strip('"').encode('utf-8').decode('unicode_escape') if i == 0 else value[slices[i-1]+1:x].strip('"').encode('utf-8').decode('unicode_escape') if i < (len(slices)) else value[x+1:len(value)].strip('"').encode('utf-8').decode('unicode_escape') for i,x in enumerate(slices) ]
              