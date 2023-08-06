

class TreeNode:

    def __init__(self, label):
        self.label = label
        self.children = []

    def get_children(self):
        return self.children

    def has_children(self):
        return len(self.children) > 0

    def add_child(self, branch):
        self.children.append(branch)

    def get_label(self):
        return self.label

    def print_node(self):
        print(self.label)



