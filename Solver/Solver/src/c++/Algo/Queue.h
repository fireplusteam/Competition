#ifndef queue_header_h
#define queue_header_h

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

// Used if we need to perform some kind of operation on the whole elements of queue like gcd(a0, a1, a2, a3, ...) in
// O(1) time
template <class Value, class State>
class Queue {
    vector<pair<Value, State>> stack;
    vector<pair<Value, State>> reversed;
    function<State(const State &, Value)> pushFunc;
    int _size = 0;

public:
    Queue(const function<State(const State &, Value)> &_pushFunc)
        : pushFunc(_pushFunc) {
    }
    void push(Value val) {
        _size++;
        stack.push_back({val, pushFunc(stack.empty() ? State() : stack.back().second, val)});
    }
    void pop() {
        assert(_size > 0);
        --_size;
        if (reversed.empty()) {
            reversed.resize(stack.size() - 1);
            if (reversed.size() > 0) {
                reversed[0] = {stack.back().first, pushFunc(State(), stack.back().first)};
                for (int i = 1; i < reversed.size(); ++i)
                    reversed[i] = {
                        stack[(int)stack.size() - i - 1].first,
                        pushFunc(reversed[i - 1].second, stack[(int)stack.size() - i - 1].first)
                    };
            }
            stack.clear();
            return;
        }
        reversed.pop_back();
    }
    template <class RetValue>
    RetValue value(const function<RetValue(const State &, const State &)> mergeFunc) {
        return mergeFunc(
            reversed.empty() ? State() : reversed.back().second,
            stack.empty() ? State() : stack.back().second
        );
    }
    void clear() {
        stack.clear();
        reversed.clear();
    }
    int size() const {
        return this->_size;
    }
};

/// example of Usage on:
/// Given an array of 𝑛 integers. Let's say that a segment of this array 𝑎[𝑙..𝑟] (1≤𝑙≤𝑟≤𝑛)is good if the GCD of all
/// numbers on this segment is
//     1 .Your task is to find the shortest good segment.
//     Input:
// The first line contains an integer 𝑛(1≤𝑛≤10^5).The second line contains integers 𝑎𝑖(1≤𝑎𝑖≤1018).class State {

long long getShortestSegmentWithGCDOne(const vector<long long> &a) {
    class State {
    public:
        long long val;
        State(long long _val = 0LL)
            : val(_val) {
        }
    };
    function<long long(long long, long long)> gcd = [&](long long a, long long b) {
        if (a == 0 || b == 0)
            return max(a, b);
        while (b > 0) {
            auto c = b;
            b      = a % b;
            a      = c;
        }
        return a;
    };
    int n = (int)a.size();
    Queue<long long, State> q([&](const State &state, long long b) { return State(gcd(state.val, b)); });
    auto merge    = [&](const State &a, const State &b) { return gcd(a.val, b.val); };
    int j         = 0;
    long long ans = -1;
    for (int i = 0; i < n; ++i) {
        j = max(j, i);
        while (j < n && (q.size() == 0 || q.value<long long>(merge) > 1)) {
            q.push(a[j]);
            ++j;
        }
        if (q.value<long long>(merge) == 1) {
            if (ans == -1 || ans > j - i)
                ans = j - i;
        } else
            break;
        q.pop();
    }
    return ans;
}
#endif