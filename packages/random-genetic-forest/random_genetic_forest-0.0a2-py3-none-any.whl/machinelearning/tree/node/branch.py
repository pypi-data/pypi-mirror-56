

class Branch:

    def __init__(self,test,node,test_value):
        self.test = test
        self.node = node
        self.test_value = test_value

    def value_test(self, value):
        return self.test(value,self.test_value)

    def get_node(self):
        return self.node

    def print_branch(self):
        print(self.node)