# encoding: utf-8

import sys
import traceback
import progressbar
import _pickle as pickle

from node              import Node
from collections       import defaultdict
from heap.heap_brother import HeapBrotherPairMax


class Trie(object):


    def __init__(self):

        self._tree    = Node()
        self._counter = defaultdict(int)



    def add(self, key, value=1):

        node_current = self._tree
        length       = len(key) - 1

        for i, w in enumerate(key):
            # child node
            node_child = node_current.children.get(w, Node(parent=node_current, key=w))

            if length == i:
                node_child.value += value

            # current node
            node_current.children[w] = node_child

            # update current ref
            node_current = node_child

        return node_child




    def __getitem__(self, key):

        node_current = self._tree

        for w in enumerate(key):

            # check
            node = node_current.children.get(w, None)

            if node is None:
                return node

            # update current ref
            node_current = node

        return node



    def delete(self, key):

        node = self[key]
        self.delete_bynode(node)




    def delete_bynode(self, node):

        if node:

            if node.root():
                node.reset()

            elif node.leaf():

                # record node.parent
                node_parent = node.parent
                
                # delete node
                # revise node.parent info
                node_parent.children.pop(node.key)

                # mark node.parent as node
                node = node_parent

                while(node.leaf() and node.meaningless()):
                    # record node.parent
                    node_parent = node.parent

                    # delete node
                    # revise node.parent info
                    node_parent.children.pop(node.key)

                    # border condition, root
                    if node_parent.root():
                        break

                    # mark node.parent as node
                    node = node_parent

            else:
                node.value = 0



    def have(self, key):

        node_current = self._tree

        for w in key:
            if w not in node_current.children.keys():
                return False
            node_current = node_current.children[w]

        if 0 == node_current.value:
            return False

        return True



    def trace(self, node):

        t = []

        n = node
        while(n.parent is not None):
            t.append(n.key)
            n = n.parent

        return ''.join(t[::-1])



    def traverse_broad(self):

        current_nodes = [self._tree]

        cnt = 0
        bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)
        while(current_nodes):
            # visit current node
            node = current_nodes.pop(0)
            yield(self.trace(node), node.value)

            # add children
            current_nodes.extend(list(node.children.values()))

            cnt += 1
            bar.update(cnt)



    def revise(self, key, cnt):

        # TODO:

        pass



    @property
    def counter(self):

        self._counter = defaultdict(int)

        for k, v in self.traverse_broad():
            self._counter[v] += 1

        try:
            self._counter.pop(0)
        except:
            traceback.print_exc()

        return self._counter



    def save(self, fn):

        with open(fn, 'wb') as f:
            pickle.dump(self.__dict__, f)


    def load(self, fn):

        with open(fn, 'rb') as f:
            d = pickle.load(f)
            self.__dict__.update(d)




class TrieHeap(Trie):


    def __init__(self):

        super(TrieHeap, self).__init__()
        self._heap = HeapBrotherPairMax()



    def have_trie(self, key):

        return self.have(key)




    def have_heap(self, key):

        return self._heap.have(key)



    def update(self, key, value=1):

        # update trie
        node_trie = self.add(key, value)

        # update heap
        if 1 == node_trie.value:
            key       = node_trie.value
            value     = 1
            info      = node_trie
            node_heap = self._heap.update_byinfo(key, value, info)
        else:
            # delete info old
            key   = node_trie.value - 1
            value = 1
            info  = node_trie
            node_delete = self._heap.delete_byinfo(key, value, info)

            # delete node when empty
            if node_delete.empty:
                self._heap.delete_bynode(node_delete)

            # add new
            key       = node_trie.value
            value     = 1
            info      = node_trie
            node_heap = self._heap.update_byinfo(key, value, info)

        return node_trie, node_heap




    def delete_bynode(self, node):
        """
        Parameters
        ----------
        node : node of heap
        """

        # delete trie
        for n in node.infoes:
            super(TrieHeap, self).delete_bynode(n)

        # delete heap
        self._heap.delete_bynode(node)



    @property
    def count_max(self):

        if self.empty:
            return 0

        node = self.node_max

        return node.key * node.value



    @property
    def count_min(self):

        if self.empty:
            return 0

        node = self.node_min

        return node.key * node.value



    @property
    def count_sum(self):

        return self._heap.value_sum



    @property
    def empty(self):

        return self._heap.empty


    @property
    def node_max(self):

        return self._heap.node_max


    @property
    def node_min(self):

        return self._heap.node_min
