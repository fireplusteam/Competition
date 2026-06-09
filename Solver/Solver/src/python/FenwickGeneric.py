# update at a single index
# min/max/sum at range [l, r]
class FenwickGeneric:
    def __init__(self, n, inf, merge_func):
        self.inf = inf
        self.n = n + 1
        self.merge = merge_func
        
        self.left = [self.inf] * self.n
        self.right = [self.inf] * self.n
        self.val = [self.inf] * self.n

    def _next(self, a):
        return a + (a & -a)

    def _prev(self, a):
        return a - (a & -a)

    def update(self, x, val_to_merge):
        x += 1
        assert 1 <= x < self.n, f"Index {x-1} out of bounds"
        
        _x = x
        while _x < self.n:
            self.left[_x] = self.merge(self.left[_x], val_to_merge)
            _x = self._next(_x)
            
        _x = x
        while _x > 0:
            self.right[_x] = self.merge(self.right[_x], val_to_merge)
            _x = self._prev(_x)
            
        self.val[x] = self.merge(self.val[x], val_to_merge)

    def get(self, l, r):
        l += 1
        r += 1
        if l > r:
            return self.inf
            
        assert 1 <= l < self.n, f"Left index {l-1} out of bounds"
        assert 1 <= r < self.n, f"Right index {r-1} out of bounds"
        
        ans = self.inf
        _l = r
        while self._prev(_l) >= l:
            ans = self.merge(ans, self.left[_l])
            _l = self._prev(_l)
            
        _l = l
        while self._next(_l) <= r:
            ans = self.merge(ans, self.right[_l])
            _l = self._next(_l)
            
        ans = self.merge(ans, self.val[_l])
        return ans


if __name__ == "__main__":
    ft = FenwickGeneric(10, float('inf'), min)
    ft.update(2, 5)
    ft.update(4, 6)
    
    print(ft.get(0, 9))
    