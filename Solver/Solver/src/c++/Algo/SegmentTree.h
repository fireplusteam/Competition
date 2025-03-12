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
    class Node {
        SegmentTree<T> *tree;
        int vert;
        int leftInd;
        int rightInd;

    public:
        Node(SegmentTree<T> *_tree, int _vert, int _leftInd, int _rightInd)
            : tree(_tree),
              vert(_vert),
              leftInd(_leftInd),
              rightInd(_rightInd) {
        }
        Node(const Node &node)
            : tree(node.tree),
              vert(node.vert),
              leftInd(node.leftInd),
              rightInd(node.rightInd) {
        }
        optional<Node> leftNode() {
            if (leftInd > (leftInd + rightInd) >> 1 || leftInd == rightInd)
                return {};
            return Node(tree, vert * 2 + 1, leftInd, (leftInd + rightInd) >> 1);
        }
        optional<Node> rightNode() {
            if (((leftInd + rightInd) >> 1) + 1 > rightInd || leftInd == rightInd)
                return {};
            return Node(tree, vert * 2 + 2, ((leftInd + rightInd) >> 1) + 1, rightInd);
        }
        bool isLeaf() {
            return leftInd == rightInd;
        }
        int getLeftInd() const {
            return leftInd;
        }
        int getRightInd() const {
            return rightInd;
        }
        T getVal() const {
            return tree->tree[vert];
        }
    };
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

    Node getRoot() {
        return Node(this, 0, 0, n - 1);
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


// Example of how to use dfs on SegmentTree to find the minimum index in range [i, j) where a[min_ind] >= x
// struct State {
//     long long maxValue = 0;

//     State(int val, int index)
//         : maxValue(val) {
//     }
//     State() {
//     }
// };

// vector<State> initState(n);
// SegmentTree<State> seg(initState, [&](const State &oldValue, const State &a, const State &b) -> State {
//     State ret    = State(0, 0);
//     ret.maxValue = max(a.maxValue, b.maxValue);
//     return ret;
// });

// /// get min index in [i, j) where elem[root] >= x
// int findMinInd(SegmentTree<State>::Node root, int x, int i, int j) {
//     j                                           -= 1;
//     function<int(SegmentTree<State>::Node)> dfs  = [&](SegmentTree<State>::Node root) {
//         if (max(i, root.getLeftInd()) > min(root.getRightInd(), j))
//             return -1;
//         if (root.getVal().maxValue < x)
//             return -1;
//         if (root.isLeaf()) {
//             return root.getVal().maxValue >= x ? root.getLeftInd() : -1;
//         }
//         if (auto leftNode = root.leftNode()) {
//             int r = dfs(*leftNode);
//             if (r != -1)
//                 return r;
//         }
//         if (auto rightNode = root.rightNode()) {
//             int r = dfs(*rightNode);
//             if (r != -1)
//                 return r;
//         }
//         return -1;
//     };
//     return dfs(root);
// }

#endif