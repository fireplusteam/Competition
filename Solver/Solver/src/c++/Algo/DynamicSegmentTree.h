#ifndef dynamic_segment_tree_h
#define dynamic_segment_tree_h

#include <stdio.h>
#include <algorithm>
#include <cassert>
#include <complex>
#include <fstream>
#include <functional>
#include <iostream>
#include <map>
#include <queue>
#include <set>
#include <sstream>

using namespace std;

// Example how to use Dynamic Segmented Tree to change the Value in range and get sum in range. Initial values are zeros
// struct State {
//     int sum = 0;
//     int D   = 0;
//     int left, right;

//     State(int _left, int _right)
//         : left(_left),
//           right(_right) {
//     }
//     int getSum() const {
//         return sum + D * (right - left + 1);
//     }
// };
// DynamicSegmentTree<State> seg(n + 1, [&](int left, int right) {
//     return State(left, right);
// }, [&](const State &oldValue, const State &a, const State &b) -> State {
//     State ret = oldValue;
//     ret.sum   = a.getSum() + b.getSum();
//     return ret;
// }, [&](const State &root, const State &leaf) {
//     State ret(leaf.left, leaf.right);
//     ret.D = root.D;
//     return ret;
// });
// int D;
// cin >> D;
// seg.set(a, b + 1, [&](const State &node) {
//     State ret(node.left, node.right);
//     ret.D = D;
//     return ret;
// });
// Example to show the sum on a segment
// SegmentTree<long long> seg(a, [&](const long long& a, const long long& b) { return a + b; });
// min on a segment
// SegmentTree<long long> seg(a, [&](const long long& a, const long long& b) { return min(a, b); });
template <class T>
class DynamicSegmentTree {
    function<T(int, int)> defaultValue;                     // (int leftIndex, int rightIndex)
    function<T(const T &, const T &, const T &)> mergeFunc; // (T root, T leftChild, T rightChild)
    function<T(const T &, const T &)> lazyPropagateFunc;    // (T root, T leaf)
    int n;

public:
    class Node {
        DynamicSegmentTree<T> *tree;
        T val;
        int leftInd;
        int rightInd;
        Node *_leftNode  = nullptr;
        Node *_rightNode = nullptr;
        bool _isMark     = false;

    public:
        Node(DynamicSegmentTree<T> *_tree, const T &_val, int _leftInd, int _rightInd)
            : tree(_tree),
              val(_val),
              leftInd(_leftInd),
              rightInd(_rightInd) {
        }
        Node *leftNode() {
            if (_leftNode)
                return _leftNode;
            assert(!isLeaf());
            _leftNode = tree->nextNode(leftInd, (leftInd + rightInd) >> 1);
            return _leftNode;
        }
        Node *rightNode() {
            if (_rightNode)
                return _rightNode;
            assert(!isLeaf());
            _rightNode = tree->nextNode(((leftInd + rightInd) >> 1) + 1, rightInd);
            return _rightNode;
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
            return val;
        }
        bool isMark() const {
            return _isMark;
        }
        void mark(bool _val) {
            _isMark = _val;
        }
        void updateVal(const T &_val) {
            val = _val;
        }
        void propagate() {
            tree->propagate(this, true);
        }
        void update() const {
            if (!isLeaf())
                tree->updateChild(this);
        }
    };

private:
    Node *rootNode = nullptr;
    list<vector<Node>> cache;
    const int chunkSize = 4096;
    int nextChildInd    = chunkSize;
    void updateChild(Node *root) {
        root->updateVal(mergeFunc(root->getVal(), root->leftNode()->getVal(), root->rightNode()->getVal()));
    }
    void propagate(Node *root, bool shouldUpdate = false) {
        if (!root->isLeaf() && root->isMark()) {
            auto leftNode = root->leftNode();
            leftNode->updateVal(lazyPropagateFunc(root->getVal(), leftNode->getVal()));
            leftNode->mark(true);
            auto rightNode = root->rightNode();
            rightNode->updateVal(lazyPropagateFunc(root->getVal(), rightNode->getVal()));
            rightNode->mark(true);
            // reset root
            root->updateVal(defaultValue(root->getLeftInd(), root->getRightInd()));
            if (shouldUpdate)
                updateChild(root);
            root->mark(false);
        }
    }

    Node *nextNode(int left, int right) {
        int numbers = min(2 * n, chunkSize);
        if (nextChildInd >= numbers) {
            cache.push_back({});
            cache.back().reserve(numbers);
            nextChildInd = 0;
        }
        cache.back().push_back(Node(this, defaultValue(left, right), left, right));
        nextChildInd++;
        return &cache.back().back();
    }

public:
    DynamicSegmentTree(
        int size,
        const function<T(int, int)> &_defaultValue,
        const function<T(const T &, const T &, const T &)> &_func,
        const function<T(const T &, const T &)> &_lazyPropageFunc = [](const T &root, const T &leaf) { return leaf; }
    )
        : defaultValue(_defaultValue),
          mergeFunc(_func),
          lazyPropagateFunc(_lazyPropageFunc),
          n(size) {
        rootNode = nextNode(0, n - 1);
    }

    Node *getRoot() {
        return rootNode;
    }

    void set(int i, int j, const function<T(const T &)> &operation) {
        j                           -= 1;
        function<void(Node *)> _set  = [&](Node *root) {
            if (max(i, root->getLeftInd()) > min(j, root->getRightInd()))
                return;
            if (root->isLeaf()) {
                root->updateVal(operation(root->getVal()));
                return;
            }
            if (i <= root->getLeftInd() && root->getRightInd() <= j) {
                root->mark(true);
                root->updateVal(operation(root->getVal()));
                return;
            }
            propagate(root);
            _set(root->leftNode());
            _set(root->rightNode());
            updateChild(root);
        };
        assert(i <= j && 0 <= i && j < n);
        _set(getRoot());
    }

    void set(int i, T val) {
        function<void(Node *)> _set = [&](Node *root) {
            if (root->isLeaf()) {
                root->updateVal(val);
                return;
            }
            propagate(root);
            int mid = (root->getLeftInd() + root->getRightInd()) / 2;
            if (i <= mid)
                _set(root->leftNode());
            else
                _set(root->rightNode());

            updateChild(root);
        };
        assert(0 <= i && i < n);
        _set(getRoot());
    }

    T get(int i, int j) {
        j                        -= 1;
        function<T(Node *)> _get  = [&](Node *root) {
            assert(max(i, root->getLeftInd()) <= min(j, root->getRightInd()));
            if (i <= root->getLeftInd() && root->getRightInd() <= j) {
                return root->getVal();
            }
            propagate(root, true);
            int mid = (root->getLeftInd() + root->getRightInd()) / 2;
            if (max(root->getLeftInd(), i) > min(mid, j))
                return _get(root->rightNode());
            if (max(mid + 1, i) > min(root->getRightInd(), j))
                return _get(root->leftNode());
            return mergeFunc(root->getVal(), _get(root->leftNode()), _get(root->rightNode()));
        };
        assert(0 <= i && i <= j && j < n);
        return _get(getRoot());
    }
};

#endif