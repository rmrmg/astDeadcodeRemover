import argparse, ast, sys


class RewriteIf(ast.NodeTransformer):
    changed = 0

    def visit_If(self, node):
        # print("NODE", node, node._fields, node.test._fields, [ast.dump(b) for b in node.body]) #, type(node.test.value))
        if 'value' in node.test._fields:
            #print("NODET", node.test.value)
            if node.test.value is False:
                self.changed += 1
                #print("VVV", ast.dump(node.body[0]))
                node.body = [ast.Pass()]
                return node
            if node.test.value is True:
                # print("VVV", ast.dump(node))
                self.changed += 1
                return node.body
        elif 'op' in node.test._fields and 'operand' in node.test._fields:
            if isinstance(node.test.op, ast.Not) and node.test.operand.value == True:
                # print("NODE O", node.test.op, "OPE", node.test.operand)
                # not True
                node.body = [ast.Pass()]
                return node
        else:
            print("NODE else:", [(b, ast.dump(getattr(node.test, b))) for b in node.test._fields])
        return node


class RewriteFunction(ast.NodeTransformer):
    changed = 0
    def visit_FunctionDef(self, node):
        retPoz = [poz for poz, nd in enumerate(node.body) if isinstance(nd, ast.Return)]
        if retPoz:
            # print("NO", node.body, retPoz)
            self.changed += 1
            node.body = node.body[:retPoz[0]+1]
        return node


def rewrite(fn):
    tree = ast.parse(open(fn).read())
    rwif = RewriteIf()
    tree2 = ast.fix_missing_locations(rwif.generic_visit(tree))
    # print("CHANGED", rwif.changed)
    if rwif.changed == 0:
        return tree2, (0, )
    rwfun = RewriteFunction()
    tree3 = ast.fix_missing_locations(rwfun.generic_visit(tree))
    return tree3, (rwif.changed, rwfun.changed)


def parseArgs():
    parser = argparse.ArgumentParser(prog='astDeadcodeRemoval', 
                                     description='This program remove dead code in two simple cases: '
                                     '1. when if True/False statement is found'
                                     '2. after first return in function body',
                                     epilog='simple way to run it: astDeadcodeRemoval pythonScipt.py if no out* '
                                     ' option defined results will be printed on stdout')
    parser.add_argument('filenames', type=str, nargs='+', help='input file(s)')
    parser.add_argument('--outprefix', type=str, default='', help='prefix for output file(s)')
    parser.add_argument('--outsuffix', type=str, default='', help='suffix for output file(s)')
    # parser.add_argument('--output', type=str, default='', help='save all results into one file')
    parser.add_argument('--verbose', action='store_true', help='print additional information')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parseArgs()
    for fn in args.filenames:
        newtree, changes = rewrite(fn)
        newcode = ast.unparse(newtree)
        fout = sys.stdout
        if args.outprefix or args.outsuffix:
            fout = open(args.outprefix + fn + args.outsuffix, 'w')
        if args.verbose:
            print(f"{changes} changes in file: {fn}")
        print(newcode, file=fout)
        if args.outprefix or args.outsuffix:
            fout.close()
