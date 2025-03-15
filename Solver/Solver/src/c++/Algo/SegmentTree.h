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
    vector<bool> mark;
    vector<T> tree;
    function<T(const T &, const T &, const T &)> func; // (T root, T leftChild, T rightChild)
    function<T(const T &, const T &)> lazyPropageFunc; // (T root, T leaf)
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
        Node leftNode() const {
            return Node(tree, vert + 1, leftInd, (leftInd + rightInd) >> 1);
        }
        Node rightNode() const {
            int mid = (leftInd + rightInd) >> 1;
            return Node(tree, vert + 2 * (mid - leftInd + 1), mid + 1, rightInd);
        }
        bool isLeaf() const {
            return leftInd == rightInd;
        }
        int getLeftInd() const {
            return leftInd;
        }
        int getRightInd() const {
            return rightInd;
        }
        const T &getVal() const {
            return tree->tree[vert];
        }
        bool isMark() const {
            return tree->mark[vert];
        }
        void mark(bool val) const {
            tree->mark[vert] = val;
        }
        void updateVal(const T &val) const {
            tree->tree[vert] = val;
        }
        void update() const {
            if (!isLeaf())
                tree->updateChild(*this);
        }
    };

private:
    void updateChild(const Node &root, optional<T> rootVal = {}) {
        root.updateVal(func(rootVal.value_or(root.getVal()), root.leftNode().getVal(), root.rightNode().getVal()));
    }
    void propagate(const Node &root) {
        if (!root.isLeaf() && root.isMark()) {
            auto leftNode = root.leftNode();
            leftNode.updateVal(lazyPropageFunc(root.getVal(), leftNode.getVal()));
            leftNode.mark(true);
            auto rightNode = root.rightNode();
            rightNode.updateVal(lazyPropageFunc(root.getVal(), rightNode.getVal()));
            rightNode.mark(true);

            // update root
            updateChild(root, T());
            root.mark(false);
        }
    }

public:
    SegmentTree(
        const vector<T> &arr,
        const function<T(const T &, const T &, const T &)> &_func,
        const function<T(const T &, const T &)> &_lazyPropageFunc
    )
        : mark(arr.size() * 2, false),
          tree(arr.size() * 2),
          func(_func),
          lazyPropageFunc(_lazyPropageFunc),
          n((int)arr.size()) {
        function<void(const Node &)> build = [&](const Node &root) {
            if (root.isLeaf()) {
                root.updateVal(arr[root.getLeftInd()]);
                return;
            }
            build(root.leftNode());
            build(root.rightNode());
            updateChild(root);
        };
        build(getRoot());
    }

    Node getRoot() {
        return Node(this, 0, 0, n - 1);
    }

    void set(int i, int j, const function<T(const T &)> &operation) {
        j                                 -= 1;
        function<void(const Node &)> _set  = [&](const Node &root) {
            if (max(i, root.getLeftInd()) > min(j, root.getRightInd()))
                return;
            propagate(root);
            if (root.isLeaf() || (i <= root.getLeftInd() && root.getRightInd() <= j)) {
                root.mark(true);
                root.updateVal(operation(root.getVal()));
                return;
            }
            _set(root.leftNode());
            _set(root.rightNode());
            updateChild(root);
        };
        assert(i <= j && 0 <= i && j < n);
        _set(getRoot());
    }

    void set(int i, T val) {
        function<void(const Node &)> _set = [&](const Node &root) {
            if (root.isLeaf()) {
                root.updateVal(val);
                return;
            }
            propagate(root);
            int mid = (root.getLeftInd() + root.getRightInd()) / 2;
            if (i <= mid)
                _set(root.leftNode());
            else
                _set(root.rightNode());
            updateChild(root);
        };
        assert(0 <= i && i < n);
        _set(getRoot());
    }

    T get(int i, int j) {
        j                              -= 1;
        function<T(const Node &)> _get  = [&](const Node &root) {
            assert(max(i, root.getLeftInd()) <= min(j, root.getRightInd()));
            if (i <= root.getLeftInd() && root.getRightInd() <= j) {
                return root.getVal();
            }
            propagate(root);
            int mid = (root.getLeftInd() + root.getRightInd()) / 2;
            if (max(root.getLeftInd(), i) > min(mid, j))
                return _get(root.rightNode());
            if (max(mid + 1, i) > min(root.getRightInd(), j))
                return _get(root.leftNode());
            return func(root.getVal(), _get(root.leftNode()), _get(root.rightNode()));
        };
        assert(0 <= i && i <= j && j < n);
        return _get(getRoot());
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