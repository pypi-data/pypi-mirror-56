#!/usr/bin/env python2.7
import sys
from lib2to3.fixer_base import BaseFix
from lib2to3.fixer_util import Name, Comma, Newline, Assign, String
from lib2to3.main import main
from lib2to3.pgen2 import token
from lib2to3.pytree import type_repr, Leaf


class FixSomething(BaseFix):

    PATTERN = """
        classdef <'class' classname=any any*>
        |
        funcdef <'def' funcname=any any* >
    """

    def start_tree(self, tree, filename):
        super(FixSomething, self).start_tree(tree, filename)
        # Reset the patterns attribute for every file:
        self._names = []

    def transform(self, node, results):
        if 'classname' in results:
            self._names.append(results['classname'].value)
        elif 'funcname' in results:
            if type_repr(node.parent.type) == 'file_input':
                self._names.append(results['funcname'].value)
        return node

    def finish_tree(self, tree, filename):
        print(filename)

        if isinstance(tree, Leaf):
            return

        names = [
            Leaf(token.LBRACE, "[", prefix=" "),
            Newline(),
        ]

        for name in self._names:
            names.append(String('"' + name + '"', prefix='    '))
            names.append(Comma())
            names.append(Newline())

        names.append(Leaf(token.LBRACE, "]", prefix=""))

        tree.append_child(Assign(Name('__all__'), names))
        tree.append_child(Newline())


if __name__ == '__main__':
    sys.path.append('/Users/lensvol/projects/personal/astboom')
    sys.exit(main('astboom'))