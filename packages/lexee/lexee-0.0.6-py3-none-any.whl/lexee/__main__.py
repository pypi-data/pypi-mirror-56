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
import json
import argparse
from antlr4 import *
from pylingo.pyVisitor import pyVisitor
from pylingo.pylingoLexer import pylingoLexer
from pylingo.pylingoParser import pylingoParser
from lexee.interpreter import Interpreter
from lexee.LexeeDoc import LexeeDoc
from protolingo.utils import marshal_output
 
def main(args):
    cli_parser = argparse.ArgumentParser(
            description='configuration arguments provided at run time from the CLI'
        )
    cli_parser.add_argument(
        '-params',
        '--parameters',
        dest='params',
        type=json.loads,
        default="{}",
        help='cli parameters'
    )
    options, cli = cli_parser.parse_known_args(args)
    doc = LexeeDoc.open(cli[1], options.params)
    try:
        for expression in doc:
                print("********************************************************")
                print("*                %s" % expression[0])
                print("********************************************************")
                marshal_output(expression)
        doc.save("%s.state" % cli[1])
    except Exception as e:
        print(e.__str__())
        raise
    finally:
        doc.close()
        
if __name__ == '__main__':
    main(sys.argv)