# encoding: utf-8

import json

class Node(object):


    def __init__(self, parent=None, key=None):

        self.reset()

        self.parent   = parent
        self.key      = key



    def reset(self):

        self.setas_root()

        self.key      = None
        self.value    = 0

        self.setas_leaf()



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



    # def __str__(self):
    #     return str(self.key)



    def __repr__(self):

        return ', '.join((str(id(self.parent)),
                         str(self.key),
                         str(self.value),
                         str(self.root()),
                         str(self.leaf()),
                         json.dumps({
                             k:id(v) for k, v in self.children.items()
                         }, ensure_ascii=False)))

        # return json.dumps(self.__dict__, ensure_ascii=False, indent=4)
