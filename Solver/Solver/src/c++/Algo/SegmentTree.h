#ifndef segment_tree_h
#define segment_tree_h

// example to use the segment tree to calculate the minimum on a segment and number of min elements on that segment
// typedef pair<int, int> ValType;
// vector<ValType> a(n, {0, 1});
// SegmentTree<ValType> seg(a, [&](const ValType &a, const ValType &b) -> ValType {
//     if (a.first == b.first) {
//         return {a.first, a.second + b.second};
//     }
//     if (a.first > b.first)
//         return b;
//     return a;
// });
//
// Example to show the sum on a segment
// SegmentTree<long long> seg(a, [&](long long a, long long b) { return a + b; });
// min on a segment
// SegmentTree<long long> seg(a, [&](long long a, long long b) { return min(a, b); });
template <class T>
class SegmentTree {
    vector<T> tree;
    function<T(const T &, const T &, const T &)> func; // (T root, T leftChild, T rightChild)
    int n;

public:
    SegmentTree(const vector<T> &arr, const function<T(const T &, const T &, const T &)> &_func)
        : tree(arr.size() * 4),
          func(_func),
          n((int)arr.size()) {
        function<T(int, int, int)> build = [&](int vert, int left, int right) {
            assert(left <= right);
            if (left == right) {
                tree[vert] = arr[left];
                return tree[vert];
            }
            int mid = (left + right) / 2;
            if (left > mid)
                return tree[vert] = build(vert * 2 + 2, mid + 1, right);
            if (mid + 1 > right)
                return tree[vert] = build(vert * 2 + 1, left, mid);
            tree[vert] = func(tree[vert], build(vert * 2 + 1, left, mid), build(vert * 2 + 2, mid + 1, right));
            return tree[vert];
        };
        build(0, 0, n - 1);
    }

    void set(int i, T val) {
        function<T(int, int, int)> _set = [&](int vert, int left, int right) {
            assert(left <= right);
            if (left == right) {
                assert(left == i);
                tree[vert] = val;
                return val;
            }
            int mid = (left + right) / 2;
            if (i <= mid)
                if (mid + 1 <= right)
                    tree[vert] = func(tree[vert], _set(vert * 2 + 1, left, mid), tree[vert * 2 + 2]);
                else
                    tree[vert] = _set(vert * 2 + 1, left, mid);
            else if (left <= mid)
                tree[vert] = func(tree[vert], tree[vert * 2 + 1], _set(vert * 2 + 2, mid + 1, right));
            else
                tree[vert] = _set(vert * 2 + 2, mid + 1, right);
            return tree[vert];
        };
        assert(0 <= i && i < n);
        _set(0, 0, n - 1);
    }

    // void update(int i, int j, const function<T(const T &)> &updateFunc) {
    //     j                                  -= 1;
    //     function<T(int, int, int)> _update  = [&](int vert, int left, int right) {
    //         if (left > right)
    //             return defaultValue();
    //         if (max(i, left) > min(j, right))
    //             return tree[vert];
    //         int mid = (left + right) / 2;
    //         if (i <= left && right <= j) {
    //             if (left == right)
    //                 return tree[vert] = updateFunc(tree[vert]);
    //             return tree[vert] = func(
    //                        updateFunc(tree[vert]),
    //                        value(vert * 2 + 1, left, mid),
    //                        value(vert * 2 + 2, mid + 1, right)
    //                    );
    //         }
    //         tree[vert] = func(tree[vert], _update(vert * 2 + 1, left, mid), _update(vert * 2 + 2, mid + 1, right));
    //         return tree[vert];
    //     };
    //     assert(0 <= i && i <= j && j < n);
    //     _update(0, 0, n - 1);
    // }

    T get(int i, int j) {
        j                               -= 1;
        function<T(int, int, int)> _get  = [&](int vert, int left, int right) {
            if (max(i, left) > min(j, right))
                return tree[vert];
            if (i <= left && right <= j) {
                return tree[vert];
            }
            int mid = (left + right) / 2;
            if (max(left, i) > min(mid, i))
                return _get(vert * 2 + 2, mid + 1, right);
            if (max(mid + 1, i) > min(right, j))
                return _get(vert * 2 + 1, left, mid);
            return func(tree[vert], _get(vert * 2 + 1, left, mid), _get(vert * 2 + 2, mid + 1, right));
        };
        assert(0 <= i && i <= j && j < n);
        return _get(0, 0, n - 1);
    }
};

#endif