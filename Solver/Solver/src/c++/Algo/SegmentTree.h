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
// }, [&]() -> ValType { return {INT_MAX, 0}; });
//
// Example to show the sum on a segment
// SegmentTree<long long> seg(a, [&](long long a, long long b) { return a + b; }, [&]() { return 0; });
// min on a segment
// SegmentTree<long long> seg(a, [&](long long a, long long b) { return min(a, b); }, [&]() { return INT_MAX; });
template <class T>
class SegmentTree {
    vector<T> tree;
    function<T(const T &, const T &)> func;
    function<T()> defaultValue;
    int n;

public:
    SegmentTree(
        const vector<T> &arr,
        const function<T(const T &, const T &)> &_func,
        const function<T()> &_defaultValue
    )
        : tree(arr.size() * 4),
          func(_func),
          defaultValue(_defaultValue),
          n((int)arr.size()) {
        function<T(int, int, int)> build = [&](int vert, int left, int right) {
            if (left > right)
                return defaultValue();
            if (left == right) {
                tree[vert] = arr[left];
                return tree[vert];
            }
            int mid    = (left + right) / 2;
            tree[vert] = func(build(vert * 2 + 1, left, mid), build(vert * 2 + 2, mid + 1, right));
            return tree[vert];
        };
        build(0, 0, n - 1);
    }

    // change value on i index to val
    void set(int i, T val) {
        auto value = [&](int vert, int left, int right) {
            if (left > right)
                return defaultValue();
            return tree[vert];
        };
        function<T(int, int, int)> _set = [&](int vert, int left, int right) {
            if (left > right)
                return defaultValue();
            if (left == right) {
                assert(left == i);
                tree[vert] = val;
                return val;
            }
            int mid = (left + right) / 2;
            if (i <= mid)
                tree[vert] = func(_set(vert * 2 + 1, left, mid), value(vert * 2 + 2, mid + 1, right));
            else
                tree[vert] = func(_set(vert * 2 + 2, mid + 1, right), value(vert * 2 + 1, left, mid));
            return tree[vert];
        };
        assert(0 <= i && i < n);
        _set(0, 0, n - 1);
    }

    // get min on a segment [i, j)
    T get(int i, int j) {
        j                               -= 1;
        function<T(int, int, int)> _get  = [&](int vert, int left, int right) {
            if (max(i, left) > min(j, right))
                return defaultValue();
            if (i <= left && right <= j) {
                return tree[vert];
            }
            int mid = (left + right) / 2;
            return func(_get(vert * 2 + 1, left, mid), _get(vert * 2 + 2, mid + 1, right));
        };
        assert(0 <= i && i <= j && j < n);
        return _get(0, 0, n - 1);
    }
};

#endif