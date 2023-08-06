# encoding: utf-8

import numpy   as np
import _pickle as pickle

from .node     import NodeBinary
from .sequence import Sequence


class Heap(object):


    def __init__(self):

        self.reset()



    def reset(self):

        self._heap = None
        self._seq  = Sequence()

        self.value_sum = 0



    @property
    def empty(self):

        return self._heap is None



    @property
    def node_max(self):

        pass



    @property
    def node_min(self):

        pass



    def swap(self):

        pass



    def tune_up(self, node):

        pass



    def tune_down(self, node):

        pass



    def tune_init(self):

        for i in range(self._seq.tail_index(),-1,-1):
            self.tune_down(self._seq[i])



    def tune(self, node):

        if node.root():
            self.tune_down(node)

        elif node.leaf():
            self.tune_up(node)



    def add(self, value):

        pass



    def delete(self):

        pass



    def save(self, fn):

        with open(fn, 'wb') as f:
            pickle.dump(self.__dict__, f)



    def load(self, fn):

        with open(fn, 'rb') as f:
            d = pickle.load(f)
            self.__dict__.update(d)



    def check(self):

        pass





class HeapPair(Heap):



    def tune_down(self, node):

        nodes = [node]

        while(nodes):

            n = nodes.pop()
            nodes.extend(self.swap_down(n))



    def tune_up_brother(self, node):

        tbd_up, tbd_brother = self.swap_up_brother(node)

        while(tbd_up):

            n = tbd_up.pop()
            up, brother = self.swap_up_brother(n)

            tbd_up.extend(up)
            tbd_brother.extend(brother)


        while(tbd_brother):

            n = tbd_brother.pop()
            tbd_brother.extend(self.swap_down(n))




    def add(self, key, value, info):

        # TODO: make node --> add_bynode

        # update value sum
        self.value_sum += key * value

        if self._heap is None:
            node       = NodeBinary(key=key, value=value, info=info)
            self._heap = node
            self._seq.append(self._heap)
        else:
            # new node
            node_parent = self._seq.tail()
            node        = NodeBinary(parent=node_parent, key=key, value=value, info=info)

            # refresh node parent
            node_parent.children.append(node)

            # refresh heap
            self._seq.append(node)

            # tune
            self.tune_up_brother(node)

        return node



    def add_bynode(self, node):

        # update value sum
        self.value_sum += node.key * node.value

        if self._heap is None:
            node.setas_root()
            self._heap = node
            self._seq.append(self._heap)

            return node

        n = self[node.key]

        if n is None:
            node_parent = self._seq.tail()

            node.setas_leaf()
            node.parent = node_parent

            # refresh node parent
            node_parent.children.append(node)

            # refresh heap
            self._seq.append(node)

            # tune
            self.tune_up_brother(node)

            return node

        else:
            n.value += node.value
            n.add(node.infoes)

            # tune
            self.tune_up_brother(n)

            return n




    def delete(self, key):

        node = self[key]

        self.delete_bynode(node)



    def delete_bynode(self, node):

        if 1 == len(self._seq) and node.root():
            self.reset()

        else:
            # update value sum
            self.value_sum -= node.key * node.value

            node_last = self._seq.last()

            if node == node_last:
                # update seq
                self._seq.last_drop()

                # update descendant info
                node.parent.children = [n for n in node.parent.children if n != node]

            else:
                # update seq
                idx = self._seq.index(node)
                self._seq[idx] = node_last
                self._seq.last_drop()

                # update descendant info
                node_last.parent.children = [n for n in node_last.parent.children
                                               if n != node_last and n != node]

                # update tree
                node_last.parent   = node.parent
                node_last.children = [n for n in node.children if n != node_last]

                # update ancestor and descendant info
                if node.parent:
                    if node.parent.child_left == node:
                        node.parent.child_left = node_last
                    else:
                        node.parent.child_right = node_last

                for n in node.children:
                    n.parent = node_last

                # update root
                if node_last.root():
                    self._heap = node_last

                # tune
                self.tune(node_last)




    def delete_byinfo(self, key, value, info):

        # update tree and seq
        node = self[key]

        if node:
            node.value -= value
            node.delete(info)
            self.tune(node)

            # update value sum
            self.value_sum -= key * value

        return node



    def __getitem__(self, key):

        for node in self._seq:
            if key == node.key:
                return node

        return None



    def update(self, key, value):

        # TODO: merge with update_byinfo

        # update value sum
        self.value_sum += key * value

        # update tree and seq
        node = self[key]

        if node:
            node.value += value
            self.tune(node)
        else:
            self.add(key, value)



    def update_byinfo(self, key, value, info):

        # get node
        node = self[key]

        if node:
            # update value sum
            self.value_sum += key * value

            # update
            node.value += value
            node.add(info)
            self.tune(node)

        else:
            # create
            node = self.add(key, value, info)

        return node
