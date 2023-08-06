from machinelearning.tree.node.treenode import TreeNode


class InternalNode(TreeNode):

    def __init__(self, label,test):
        super().__init__(label)
        self.test = test


