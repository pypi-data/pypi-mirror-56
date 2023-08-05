from pythonds.trees import BinaryTree


class BinaryTreeExtended(BinaryTree):
    """Extends the BinaryTree base class from pythonds.trees by adding additional attributes and methods that are
    needed to implement forward mode and reverse mode."""
    def __init__(self, rootObj):
        """Stores the derivative of a parent node with respect to its children nodes and stores the result of
        evaluating all subtrees of the given tree. All these values are initialized to None."""
        BinaryTree.__init__(self, rootObj)
        self.leftChildDer = None
        self.rightChildDer = None
        self.val = None

    def insertLeft(self, node):
        """Assigns the left child of the given tree to be a new tree."""
        self.leftChild = BinaryTreeExtended(node)

    def insertRight(self, node):
        """Assigns the right child of the given tree to be a new tree."""
        self.rightChild = BinaryTreeExtended(node)

    def insertLeftExistingTree(self, tree):
        """Assigns the left child of the given tree to be an preexisting tree."""
        self.leftChild = tree

    def insertDerivatives(self, vals):
        """Assigns derivatives of node with respect to left and right children."""
        self.leftChildDer = vals[0]
        self.rightChildDer = vals[1]

    def getDerivatives(self):
        """Retrieves derivatives of node with respect to left and right children."""
        return self.leftChildDer, self.rightChildDer

    def setVal(self, val):
        """Sets value of node."""
        self.val = val

    def getVal(self):
        """Gets value stored at node."""
        return self.val

    def __str__(self):
        """Creates string representation of binary tree for debugging purposes."""
        return str(self.getRootVal()) + \
               '\n|\n|-(L)->' + '\n|      '.join(str(self.leftChild).split('\n')) + \
               '\n|\n|-(R)->' + '\n|      '.join(str(self.rightChild).split('\n'))
