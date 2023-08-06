# encoding: utf-8

import progressbar
import _pickle as pickle

from trie import TrieHeap


class TrieDouble(object):


    def __init__(self, ratio=None, batch_size=1):

        self.ratio      = ratio

        self._trie_top  = TrieHeap()
        self._trie_rest = TrieHeap()

        self._count     = 0
        self.batch_size = 1



    def check(self):

        # TODO:

        pass



    @property
    def need_tune(self):

        return 0 == self._count % self.batch_size



    def trie_to_trie(self, node, trie1, trie2):
        """ Delete node of trie1, Add to trie2

        Parameters
        ----------
        node: trie.heap.node in trie1

        trie1: trie

        trie2: trie
        """

        # update in trie2
        infoes = set()

        for n in node.infoes:
            key       = trie1.trace(n)
            value     = node.key
            node_trie = trie2.add(key, value)
        
            infoes.add(node_trie)
        
        # delete in trie1 & heap1
        trie1.delete_bynode(node)
        
        # update in heap2
        node.infoes = infoes
        trie2._heap.add_bynode(node)



    def tune_top_ratio(self):

        if (self._trie_top.count_sum-self._trie_top.count_min)/\
           (self._trie_top.count_sum+self._trie_rest.count_sum) >= self.ratio:

            self.trie_to_trie(self._trie_top.node_min,
                              self._trie_top,
                              self._trie_rest)



    def tune_rest_ratio(self):

        if self._trie_top.count_sum/\
          (self._trie_top.count_sum+self._trie_rest.count_sum) < self.ratio:

            self.trie_to_trie(self._trie_rest.node_max,
                              self._trie_rest,
                              self._trie_top)


    def tune_top_unique(self, node):

        if self.have_rest_heap(node.key):
            self.trie_to_trie(node, self._trie_top, self._trie_rest)



    def tune_rest_unique(self, node):
        """ for key unique

        warnging: key is change with each update.
        """

        if self.have_top_heap(node.key):
            self.trie_to_trie(node, self._trie_rest, self._trie_top)



    def tune(self, node):

        self.tune_top_unique(node)
        self.tune_top_ratio()

        # self.tune_rest_unique(node)
        self.tune_rest_ratio()



    def update(self, key, value=1):

        self._count += 1

        if self._trie_top.empty:
            self._trie_top.update(key, value)

        elif self.have_top_trie(key):
            _, node_heap = self._trie_top.update(key, value)

            if self.need_tune:
                self.tune_top_unique(node_heap)
                self.tune_top_ratio()

        elif self.have_rest_trie(key):
            _, node_heap = self._trie_rest.update(key, value)

            if self.need_tune:
                self.tune_rest_unique(node_heap)
                self.tune_rest_ratio()

        elif self._trie_rest.empty:
            # rest empty --> top <= ratio
            # put more, then tune
            _, node_heap = self._trie_top.update(key, value)

            if self.need_tune:
                self.tune_top_unique(node_heap)
                self.tune_top_ratio()

        else:
            _, node_heap = self._trie_rest.update(key, value)

            if self.need_tune:
                self.tune_rest_unique(node_heap)
                self.tune_rest_ratio()



    def have_top_trie(self, key):

        return self._trie_top.have_trie(key)



    def have_rest_trie(self, key):

        return self._trie_rest.have_trie(key)



    def have_top_heap(self, key):

        return self._trie_top.have_heap(key)



    def have_rest_heap(self, key):

        return self._trie_rest.have_heap(key)



    def save(self, fn, predict=False):

        if not predict:
            with open(fn, 'wb') as f:
                pickle.dump(self.__dict__, f)

        else:
            with open('%s.top' % fn, 'wb') as f:
                pickle.dump({
                                'ratio'    : self.ratio,
                                '_trie_top': self._trie_top
                            }, f)



    def load(self, fn, predict=False):

        if not predict:
            with open(fn, 'rb') as f:
                d = pickle.load(f)
                self.__dict__.update(d)

        else:
            with open('%s.top' % fn, 'rb') as f:
                d = pickle.load(f)
                self.__dict__.update(d)
