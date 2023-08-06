import unittest

from machinelearning.tree.general_tree import GeneralTree
from machinelearning.tree.node.branch import Branch
from machinelearning.tree.node.treenode import TreeNode


class TestGeneralTree(unittest.TestCase):

    def test_tree_traversal_root(self):
        tree = GeneralTree('Hello')
        tree.get_root().add_child(Branch(lambda value,test_value: True,TreeNode('Yes'), 'Its me'))
        tree.get_root().add_child(Branch(lambda value,test_value: True,TreeNode('No'),  'good bye'))
        tree.depth_first_traversal(tree.get_root())


if __name__ == '__main__':
    unittest.main()
