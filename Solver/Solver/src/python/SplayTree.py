class Node:
    def __init__(self, val, parent=None, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        self.parent = parent


class SplayTree:

    def __init__(self):
        self.root = None
        self.operations = 0

    def _rotateLeft(self, x: Node, p: Node):
        x.parent = p.parent
        if p.parent:
            if p.parent.left == p:
                p.parent.left = x
            else:
                p.parent.right = x
        p.parent = x
        x_right = x.right
        x.right = p
        p.left = x_right
        if x_right:
            x_right.parent = p
        return x

    def _rotateRight(self, x: Node, p: Node):
        x.parent = p.parent
        if p.parent:
            if p.parent.left == p:
                p.parent.left = x
            else:
                p.parent.right = x
        p.parent = x
        x_left = x.left
        x.left = p
        p.right = x_left
        if x_left:
            x_left.parent = p
        return x

    def _expose(self, x: Node):
        if not x:
            self.root = None
            return None
        while True:
            p = x.parent
            if not p:
                self.root = x
                break
            g = p.parent
            self.operations += 1
            if not g:
                if p.left == x:
                    self.root = self._rotateLeft(x, p)
                else:
                    self.root = self._rotateRight(x, p)
                break
            if g.left == p and p.left == x:  # make x -> p -> g
                p = self._rotateLeft(p, g)
                x = self._rotateLeft(x, p)
            elif g.right == p and p.right == x:
                p = self._rotateRight(p, g)
                x = self._rotateRight(x, p)
            elif g.left == p and p.right == x:  # make p <- x -> g
                x = self._rotateRight(x, p)
                x = self._rotateLeft(x, g)
            elif g.right == p and p.left == x:
                x = self._rotateLeft(x, p)
                x = self._rotateRight(x, g)
        return self.root

    def _split(self, x: Node):
        x = self._expose(x)
        right = x.right
        if x.right:
            x.right.parent = None
        x.right = None
        return [x, right]

    def _merge(self, x: Node, y: Node):
        if not x and not y:
            return self._expose(None)
        if not x:
            return self._expose(y)
        if not y:
            return self._expose(x)
        if x.val > y.val:
            x, y = y, x
        while x.right:
            x = x.right
        x = self._expose(x)
        x.right = y
        y.parent = x
        return x

    def _find(self, val):
        if not self.root:
            return None
        node = self.root
        upper = None
        prev = node
        while node:
            if node.val == val:
                self._expose(node)
                return node
            prev = node
            if node.val < val:
                upper = node
                node = node.right
            else:
                node = node.left
        if upper:
            self._expose(upper)
        else:
            self._expose(prev)
        return upper

    def _insert(self, val):
        node = self._find(val)
        if not node:
            return self._merge(Node(val), self.root), True
        if node.val == val:
            return node, False
        x, y = self._split(node)

        assert x.val < val
        x.right = Node(val, parent=x)
        return self._merge(x, y), True

    # public Interface
    def contains(self, val):
        node = self._find(val)
        if not node or node.val != val:
            return False
        return True

    def insert(self, val):
        _, ok = self._insert(val)
        return ok

    def remove(self, val):
        node = self._find(val)
        if not node or node.val != val:
            return False
        x, y = self._split(node)
        if x and x.left:
            x.left.parent = None
        if y:
            y.parent = None
        self._merge(x.left, y)
        return True

    def toList(self):
        ans = []

        def traverse(root):
            if not root:
                return
            traverse(root.left)
            ans.append(root.val)
            traverse(root.right)

        traverse(self.root)
        return ans
