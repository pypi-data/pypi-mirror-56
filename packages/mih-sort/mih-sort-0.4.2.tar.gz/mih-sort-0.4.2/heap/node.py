# encoding: utf-8

import json


class Node(object):


    def __init__(self, parent=None, key=None, value=0, info=None):

        self.reset()

        self.parent   = parent
        self.key      = key
        self.value    = value

        if info is not None:
            self.add(info)



    def reset(self):

        self.setas_root()

        self.key      = None
        self.value    = 0
        self.infoes   = set()

        self.setas_leaf()



    def add(self, info):

        if set == type(info):
            self.infoes = self.infoes.union(info)

        else:
            self.infoes.add(info)



    def delete(self, info):

        self.infoes = self.infoes - {info}



    @property
    def empty(self):

        return not bool(self.infoes)



    def setas_root(self):

        self.parent   = None



    def setas_leaf(self):

        self.children = {}



    def root(self):

        return self.parent is None



    def leaf(self):

        return not bool(self.children)



    def meaningless(self):

        return 0 == self.value



    def __repr__(self):

        return ', '.join((str(id(self.parent)),
                         str(self.key),
                         str(self.value),
                         str(self.root()),
                         str(self.leaf()),
                         json.dumps({
                             k:id(v) for k, v in self.children.items()
                         }, ensure_ascii=False)))





class NodeBinary(Node):



    def setas_leaf(self):

        self.children = []


    @property
    def child_left(self):

        try:
            return self.children[0]
        except:
            return None



    @child_left.setter
    def child_left(self, node):

        try:
            self.children[0] = node
        except:
            self.children.append(node)



    @property
    def child_right(self):

        try:
            return self.children[1]
        except:
            return None



    @child_right.setter
    def child_right(self, node):

        try:
            self.children[1] = node
        except:
            self.children.append(node)



    def left_only(self):

        return 1 == len(self.children)



    def __repr__(self):

        return ', '.join((str(id(self.parent)),
                          str(id(self)),
                          str(self.key),
                          str(self.value),
                          str(self.root()),
                          str(self.leaf()),
                          json.dumps([id(v) for v in self.children], ensure_ascii=False),
                          # json.dumps([id(v) for v in self.infoes]  , ensure_ascii=False),
                          str(self.empty)))
