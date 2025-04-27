class Node:
    def __init__(self, val, parent=None, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        self.parent = parent
        self.cnt = 1

    def pull(self):
        self.cnt = 1
        if self.left:
            self.cnt += self.left.cnt
        if self.right:
            self.cnt += self.right.cnt


from typing import Callable


class SplayTree:

    def __init__(self, key: Callable | None = None):
        self.root = None
        self.key = key
        self.operations = 0

    def _val(self, val):
        if self.key:
            return self.key(val)
        return val

    def _traverse(self, root):
        if not root:
            return
        yield from self._traverse(root.left)
        yield root.val
        yield from self._traverse(root.right)

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
        p.pull()
        x.pull()
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
        p.pull()
        x.pull()
        return x

    def _expose(self, x: Node):
        if not x:
            return None
        while True:
            p = x.parent
            self.operations += 1
            if not p:
                return x
            g = p.parent
            if not g:
                if p.left == x:
                    return self._rotateLeft(x, p)
                else:
                    return self._rotateRight(x, p)
            if g.left == p and p.left == x:  # make x -> p -> g
                self._rotateLeft(p, g)
                self._rotateLeft(x, p)
            elif g.right == p and p.right == x:
                self._rotateRight(p, g)
                self._rotateRight(x, p)
            elif g.left == p and p.right == x:  # make p <- x -> g
                self._rotateRight(x, p)
                self._rotateLeft(x, g)
            elif g.right == p and p.left == x:
                self._rotateLeft(x, p)
                self._rotateRight(x, g)

    def _split(self, x: Node):
        x = self._expose(x)
        right = x.right
        if x.right:
            x.right.parent = None
        x.right = None
        self.root = None
        x.pull()
        return [x, right]

    def _merge(self, x: Node, y: Node):
        if not x and not y:
            return None
        if not x:
            return self._expose(y)
        if not y:
            return self._expose(x)
        if self._val(x.val) > self._val(y.val):
            x, y = y, x
        while x.right:
            x = x.right
        x = self._expose(x)
        x.right = y
        y.parent = x
        x.pull()
        return x

    def _find(self, val):
        if not self.root:
            return None
        node = self.root
        while node:
            if self._val(node.val) == self._val(val):
                break
            elif self._val(node.val) < self._val(val):
                if not node.right:
                    break
                node = node.right
            else:
                if not node.left:
                    break
                node = node.left
        return node

    def insert(self, val):
        node = self._find(val)
        if not node:
            self.root = self._merge(Node(val), self.root)
            return True
        if self._val(node.val) == self._val(val):
            return False
        if self._val(node.val) < self._val(val):
            node.right = Node(val, node)
            self.root = self._expose(node.right)
            return True
        else:
            node.left = Node(val, node)
            self.root = self._expose(node.left)
            return True

    # public Interface
    def contains(self, val):
        self.root = self._find(val)
        self.root = self._expose(self.root)
        if not self.root or self._val(self.root.val) != self._val(val):
            return False
        return True

    def remove(self, val):
        self.root = self._find(val)
        if not self.root or self._val(self.root.val) != self._val(val):
            self.root = self._expose(self.root)
            return False
        x, y = self._split(self.root)
        if x and x.left:
            x.left.parent = None
        if y:
            y.parent = None
        self.root = self._merge(x.left, y)
        return True

    def __getitem__(self, index):
        if index < 0:
            index = len(self) + index
        if index < 0:
            TypeError("Out of Index")

        node = self.root
        sum = -1
        while node:
            if node.left:
                if sum + node.left.cnt < index:
                    sum += node.left.cnt
                else:
                    node = node.left
                    continue
            if 1 + sum == index:
                self.root = self._expose(node)
                return node.val
            sum += 1
            node = node.right
        raise TypeError("Out of index")

    def __iter__(self):
        for i in self.toList():
            yield i

    def __len__(self):
        if not self.root:
            return 0
        return self.root.cnt

    def toList(self):
        return list(self._traverse(self.root))
