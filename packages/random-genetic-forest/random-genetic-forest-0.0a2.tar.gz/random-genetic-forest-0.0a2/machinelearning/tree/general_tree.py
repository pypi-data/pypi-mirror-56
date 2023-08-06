from machinelearning.tree.node.treenode import TreeNode


class GeneralTree:

    def __init__(self, value):
        self.root = TreeNode(value)
        self.current = self.root
        self.size = 1

    def get_root(self):
        return self.root

    def set_root(self,root_node):
        self.root = root_node

    def get_current_node(self):
        return self.current

    def depth_first_traversal(self, node):
        node.print_node()

        for branch in node.get_children():
            self.depth_first_traversal(branch.get_node())
