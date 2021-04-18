'''
This file implements the AVL Tree data structure.
The functions in this file are considerably harder than the functions in the BinaryTree and BST files,
but there are fewer of them.
'''

from containers.BinaryTree import BinaryTree, Node
from containers.BST import BST


class AVLTree(BST):
    '''
    FIXME:
    AVLTree is currently not a subclass of BST.
    You should make the necessary changes in the class declaration line above
    and in the constructor below.
    '''

    def __init__(self, xs=None):
        '''
        FIXME:
        Implement this function.
        '''
        super().__init__()
        self.xs = xs
        if self.xs is not None:
            self.insert_list(xs)

    def balance_factor(self):
        '''
        Returns the balance factor of a tree.
        '''
        return AVLTree._balance_factor(self.root)

    @staticmethod
    def _balance_factor(node):
        '''
        Returns the balance factor of a node.
        '''
        if node is None:
            return 0
        return BinaryTree._height(node.left) - BinaryTree._height(node.right)

    def is_avl_satisfied(self):
        '''
        Returns True if the avl tree satisfies that all nodes
        have a balance factor in [-1,0,1].
        '''
        return AVLTree._is_avl_satisfied(self.root)

    @staticmethod
    def _is_avl_satisfied(node):
        '''
        FIXME:
        Implement this function.
        '''
        ret = True
        if node is None:
            return True
        if AVLTree._balance_factor(node) not in [-1, 0, 1]:
            ret = False
        if node.left:
            if AVLTree._balance_factor(node.left) in [-1, 0, 1]:
                ret &= AVLTree._is_avl_satisfied(node.left)
            else:
                ret = False
        if node.right:
            if AVLTree._balance_factor(node.right) in [-1, 0, 1]:
                ret &= AVLTree._is_avl_satisfied(node.right)
            else:
                ret = False
        return ret

    @staticmethod
    def _left_rotate(node):
        '''
        FIXME:
        Implement this function.

        The lecture videos provide a high-level overview of tree rotations,
        and the textbook provides full python code.
        The textbook's class hierarchy for their AVL tree code is fairly
        different from our class hierarchy,
        however, so you will have to adapt their code.
        '''
        if node is None or node.right is None:
            return

        newNode = Node(node.right.value)
        newNode.right = node.right.right

        nodeleft = Node(node.value)
        nodeleft.left = node.left
        nodeleft.right = node.right.left

        newNode.left = nodeleft

        return newNode

    @staticmethod
    def _right_rotate(node):
        '''
        FIXME:
        Implement this function.

        The lecture videos provide a high-level overview of tree rotations,
        and the textbook provides full python code.
        The textbook's class hierarchy for their AVL tree code is fairly
        different from our class hierarchy,
        however, so you will have to adapt their code.
        '''
        if node is None or node.left is None:
            return

        newNode = Node(node.left.value)
        newNode.left = node.left.left

        noderight = Node(node.value)
        noderight.right = node.right
        noderight.left = node.left.right

        newNode.right = noderight

        return newNode

    def insert(self, value):
        '''
        FIXME:
        Implement this function.

        The lecture videos provide a high-level overview of how
        to insert into an AVL tree,
        and the textbook provides full python code.
        The textbook's class hierarchy for their AVL tree code is fairly
        different from our class hierarchy,
        however, so you will have to adapt their code.

        HINT:
        It is okay to add @staticmethod helper functions for this code.
        The code should look very similar to the code for your insert
        function for the BST,
        but it will also call the left and right rebalancing functions.
        '''
        if self.root:
            if value == self.root.value:
                return
            self._insert(value, self.root)
            if not self.is_avl_satisfied():
                self.root = self.rebalance(self.root)
                if not self.is_avl_satisfied():
                    self.root = self.rebalance(self.root)
        else:
            self.root = Node(value)

    @staticmethod
    def _insert(value, node):
        if value < node.value:
            if node.left:
                return AVLTree._insert(value, node.left)
            else:
                node.left = Node(value)
        elif value > node.value:
            if node.right:
                return AVLTree._insert(value, node.right)
            else:
                node.right = Node(value)
        return

    def rebalance(self, node):
        '''
        recurses over the entire AVL tree to find all nodes
        with balance factors not in [-1, 0, 1]
        '''
        if node is None:
            return
        if AVLTree._balance_factor(node) in [-1, 0, 1]:
            node = self._rebalance(node)
        else:
            node.right = self.rebalance(node.right)
            node.left = self.rebalance(node.left)
        return node

    @staticmethod
    def _rebalance(node):
        '''
        There are no test cases for the rebalance function,
        so you do not technically have to implement it.
        But both the insert function needs the rebalancing code,
        so I recommend including that code here.
        '''
        balanceFactor = AVLTree._balance_factor(node)
        if balanceFactor < 0:
            if AVLTree._balance_factor(node.right) > 0:
                node.right = AVLTree._right_rotate(node.right)
                node = AVLTree._left_rotate(node)
            else:
                node = AVLTree._left_rotate(node)
        elif balanceFactor > 0:
            if AVLTree._balance_factor(node.left) < 0:
                node.left = AVLTree._left_rotate(node.right)
                node = AVLTree._right_rotate(node)
            else:
                node = AVLTree._right_rotate(node)
        return node
