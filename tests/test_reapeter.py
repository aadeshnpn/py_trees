from unittest import TestCase
import py_trees
from py_trees import Behaviour, Status
from py_trees.meta import timeout
import numpy as np

np.random.seed(1)

class NeighbourCondition(Behaviour):

    def setup(self, timeout):
        self.time = 10
        pass

    def initialise(self):
        pass

    def update(self):
        self.time -= 1
        if np.random.rand() > 0.2:
            return Status.SUCCESS
        else:
            return Status.FAILURE


class Move(Behaviour):
    def __init__(self, name):
        super(Move, self).__init__(name)

    def setup(self, timeout):
        pass

    def initialise(self):
        pass

    def update(self):
        return Status.SUCCESS


class JPT(Behaviour):
    def __init__(self, name):
        super(JPT, self).__init__(name)

    def setup(self, timeout):
        pass

    def initialise(self):
        pass

    def update(self):
        return Status.FAILURE


class TestRepeater(TestCase):
    
    def test_repeater(self):
        root = py_trees.composites.Selector("Selector")
        low = timeout(JPT, 1000)('1')
        repeat = py_trees.composites.RepeatUntilFalse(name="Repeat")
        high = NeighbourCondition('R')
        high.setup(0)
        move = Move('M')

        repeat.add_children([high, move])
        root.add_children([low, repeat])

        py_trees.display.print_ascii_tree(root,indent=4, show_status=True)

        behaviour_tree = py_trees.trees.BehaviourTree(root)
        for i in range(2):
            behaviour_tree.tick()
        assert(high.time==5)
