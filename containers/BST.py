'''
This file implements the Binary Search Tree data structure.
The functions in this file are considerably harder than the
functions in the BinaryTree file.
'''

from containers.BinaryTree import BinaryTree, Node


class BST(BinaryTree):
    '''
    The BST is a superclass of BinaryTree.
    That means that the BST class "inherits" all the methods from BinaryTree,
    and we don't have to reimplement them.
    '''

    def __init__(self, xs=None):
        '''
        FIXME:
        If xs is a list (i.e. xs is not None),
        then each element of xs needs to be inserted into the BST.
        '''
        super().__init__()
        self.xs = xs
        if self.xs is not None:
            self.insert_list(xs)

    def __repr__(self):
        '''
        Notice that in the BinaryTree class,
        we defined a __str__ function,
        but not a __repr__ function.
        Recall that the __repr__ function should return a string that
        can be used to recreate a valid instance of the class.
        Thus, if you create a variable using the command BST([1,2,3])
        it's __repr__ will return "BST([1,2,3])"

        For the BST, type(self).__name__ will be the string "BST",
        but for the AVLTree, this expression will be "AVLTree".
        Using this expression ensures that all subclasses of BST will
        have a correct implementation of __repr__,
        and that they won't have to reimplement it.
        '''
        return type(self).__name__ + '(' + str(self.to_list('inorder')) + ')'

    def __eq__(self, t2):
        '''
        This method checks to see if the contents of self and t2 are equal.
        The expression `a == b` desugars to `a.__eq__(b)`.

        NOTE:
        We only care about "semantic" equality,
        and not "syntactic" equality.
        That is, we do not care about the tree structure itself,
        and only care about the contents of what the tree contains.

        HINT:
        Convert the contents of both trees into a sorted list,
        then compare those sorted lists for equality.
        '''
        selflist = self.to_list('inorder')
        t2list = t2.to_list('inorder')
        if len(selflist) != len(t2list):
            return False
        for i in range(len(selflist)):
            if selflist[i] != t2list[i]:
                return False
        return True

    def is_bst_satisfied(self):
        '''
        Whenever you implement a data structure,
        the first thing to do is to implement a function that checks whether
        the structure obeys all of its laws.
        This makes it possible to automatically test whether
        insert/delete functions
        are actually working.
        '''
        if self.root:
            return BST._is_bst_satisfied(self.root)
        return True

    @staticmethod
    def _is_bst_satisfied(node):
        '''
        FIXME:
        The current implementation has a bug:
        it only checks if the children of the current node
        are less than/greater than,
        rather than ensuring that all nodes to the left/right are
        less than/greater than.

        HINT:
        Use the _find_smallest and _find_largest functions to fix the bug.
        You should use the _ prefixed methods because those are static
        methods just like this one.
        '''
        ret = True
        if node.left:
            if node.value >= BST._find_largest(node.left):
                ret &= BST._is_bst_satisfied(node.left)
            else:
                ret = False
        if node.right:
            if node.value <= BST._find_smallest(node.right):
                ret &= BST._is_bst_satisfied(node.right)
            else:
                ret = False
        return ret

    def insert(self, value):
        '''
        Inserts value into the BST.

        FIXME:
        Implement this function.

        HINT:
        Create a staticmethod helper function following the
        pattern of _is_bst_satisfied.
        '''
        if self.root:
            return BST._insert(value, self.root)
        else:
            self.root = Node(value)

    @staticmethod
    def _insert(value, node):
        if value < node.value:
            if node.left:
                BST._insert(value, node.left)
            else:
                node.left = Node(value)
        elif value > node.value:
            if node.right:
                BST._insert(value, node.right)
            else:
                node.right = Node(value)

    def insert_list(self, xs):
        '''
        Given a list xs, insert each element of xs into self.

        FIXME:
        Implement this function.

        HINT:
        Repeatedly call the insert method.
        You cannot get this method to work correctly until you have
        gotten insert to work correctly.
        '''
        if xs is not None:
            for x in xs:
                self.insert(x)

    def __contains__(self, value):
        '''
        Recall that `x in tree` desugars to `tree.__contains__(x)`.
        '''
        return self.find(value)

    def find(self, value):
        '''
        Returns whether value is contained in the BST.

        FIXME:
        Implement this function.
        '''
        if self.root:
            return BST._find(value, self.root)
        else:
            return None

    @staticmethod
    def _find(value, node):
        '''
        FIXME:
        Implement this function.
        '''
        if value == node.value:
            return True
        else:
            if value > node.value:
                if node.right:
                    return BST._find(value, node.right)
                else:
                    return False
            elif value < node.value:
                if node.left:
                    return BST._find(value, node.left)
                else:
                    return False
        return False

    def find_smallest(self):
        '''
        Returns the smallest value in the tree.
        '''
        if self.root is None:
            raise ValueError('Nothing in tree')
        else:
            return BST._find_smallest(self.root)

    @staticmethod
    def _find_smallest(node):
        '''
        This is a helper function for find_smallest and
        not intended to be called directly by the user.
        '''
        assert node is not None
        if node.left is None:
            return node.value
        else:
            return BST._find_smallest(node.left)

    def find_largest(self):
        '''
        Returns the largest value in the tree.

        FIXME:
        Implement this function.

        HINT:
        Follow the pattern of the _find_smallest function.
        '''
        if self.root is None:
            raise ValueError('Nothing in tree')
        else:
            return BST._find_largest(self.root)

    @staticmethod
    def _find_largest(node):
        assert node is not None
        if node.right is None:
            return node.value
        else:
            return BST._find_largest(node.right)

    def remove(self, value):
        '''
        Removes value from the BST.
        If value is not in the BST, it does nothing.

        FIXME:
        Implement this function.

        HINT:
        You should have everything else working
        before you implement this function.

        HINT:
        Use a recursive helper function.
        '''
        if self.__contains__(value):
            if self.root.value == value:
                if self.root.left:
                    new = BST._find_largest(self.root.left)
                    self.root.value = new
                    self.root.left = BST._remove(new, self.root.left)
                    return self.root
                elif self.root.right:
                    new = BST._find_smallest(self.root.right)
                    self.root.value = new
                    self.root.right = BST._remove(new, self.root.right)
                    return self.root
                else:
                    self.root = None
                    return self.root
            else:
                return BST._remove(value, self.root)
        else:
            pass

    @staticmethod
    def _remove(value, node):
        if node is None:
            return node
        if value > node.value:
            node.right = BST._remove(value, node.right)
        elif value < node.value:
            node.left = BST._remove(value, node.left)
        else:
            if node.left is None:
                new = node.right
                node = None
                return new
            elif node.right is None:
                new = node.left
                node = None
                return new
            else:
                new = BST._find_largest(node.left)
                node.value = new
                node.left = BST._remove(new, node.left)
        return node

    def remove_list(self, xs):
        '''
        Given a list xs, remove each element of xs from self.

        FIXME:
        Implement this function.

        HINT:
        See the insert_list function.
        '''
        for x in xs:
            self.remove(x)
