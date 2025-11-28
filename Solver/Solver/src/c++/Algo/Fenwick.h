#ifndef fenwick_h
#define fenwick_h

#if !defined(__clang__) && defined(__GNUC__)
    #include <bits/stdc++.h>
#else
    #include <algorithm>
    #include <bitset>
    #include <cassert>
    #include <complex>
    #include <cstdio>
    #include <ctime>
    #include <deque>
    #include <fstream>
    #include <functional>
    #include <iostream>
    #include <list>
    #include <map>
    #include <optional>
    #include <queue>
    #include <random>
    #include <regex>
    #include <set>
    #include <sstream>
    #include <stack>
    #include <unordered_map>
    #include <unordered_set>
#endif

using namespace std;

// Sum on a segment, update at a single index
class Fenwick {
    vector<long long> sum;

public:
    Fenwick(int n)
        : sum(n + 1) {
    }

    // update on [x] with val
    void update(int x, int val) {
        x += 1;
        assert(1 <= x && x < sum.size());
        while (x < sum.size()) {
            sum[x] += val;
            x      += x & -x;
        }
    }
    // sum on [0, l]
    long long get(int l) {
        ++l;
        assert(1 <= l && l < sum.size());
        long long ans = 0;
        while (l > 0) {
            ans += sum[l];
            l   -= l & -l;
        }
        return ans;
    }
    // sum on [l, r]
    long long get(int l, int r) {
        assert(0 <= l && l <= r && r < sum.size() - 1);
        if (l == 0)
            return get(r);
        return get(r) - get(l - 1);
    }
};

// Sum on a segment, update at a range, get value at index
class FenwickRangeUpdate {
    vector<long long> sum;

    // sum on [0, l]
    long long _get(int l) {
        ++l;
        assert(1 <= l && l < sum.size());
        long long ans = 0;
        while (l > 0) {
            ans += sum[l];
            l   -= l & -l;
        }
        return ans;
    }

public:
    FenwickRangeUpdate(int n)
        : sum(n + 1) {
    }

    // update on [l, r] with val
    void update(int l, int r, int val) {
        assert(0 <= l && l <= r && r < sum.size() - 1);
        ++l, ++r;
        while (l < sum.size()) {
            sum[l] += val;
            l      += l & -l;
        }
        r++;
        while (r < sum.size()) {
            sum[r] -= val;
            r       = r & -r;
        }
    }
    // value at index i
    long long get(int i) {
        assert(0 <= i && i < sum.size() - 1);
        if (i == 0)
            return get(i);
        return get(i) - get(i - 1);
    }
};


/// MAX Fenwick
/// get min/max/sum on range [l, r], update at index

// MAX: FenwickGeneric<int> f(n, INT_MIN, [&](const int &a, const int &b) { return max(a, b); })
// MIN: FenwickGeneric<int> f(n, INT_MAX, [&](const int &a, const int &b) { return min(a, b); })
// SUM: FenwickGeneric<int> f(n, 0, [&](const int &a, const int &b) { return a + b; })
template <class T>
class FenwickGeneric {
    vector<T> left;
    vector<T> right;
    vector<T> val;
    T inf;
    const int n;

    function<T(const T &, const T &)> merge;

    inline int next(int a) {
        return a + (a & -a);
    }
    inline int prev(int a) {
        return a - (a & -a);
    }

public:
    FenwickGeneric(int _n, const T &_inf, const function<T(const T &, const T &)> &_merge)
        : left(_n + 1, _inf),
          right(_n + 1, _inf),
          val(_n + 1, _inf),
          inf(_inf),
          n(_n + 1),
          merge(_merge) {
    }

    // update on [x] with val
    void update(int x, const T &_val) {
        ++x;
        assert(1 <= x && x < n);
        auto _x = x;
        while (_x < n) {
            this->left[_x] = merge(this->left[_x], _val);
            _x             = next(_x);
        }
        _x = x;
        while (_x > 0) {
            this->right[_x] = merge(this->right[_x], _val);
            _x              = prev(_x);
        }
        val[x] = merge(val[x], _val);
    }

    // get value on [l, r]
    T get(int l, int r) {
        ++l, ++r;
        if (l > r) {
            return inf;
        }
        assert(1 <= l && l < n);
        assert(1 <= r && r < n);
        T ans   = inf;
        auto _l = r;
        while (prev(_l) >= l) {
            ans = merge(ans, left[_l]);
            _l  = prev(_l);
        }
        _l = l;
        while (next(_l) <= r) {
            ans = merge(ans, right[_l]);
            _l  = next(_l);
        }
        ans = merge(ans, val[_l]);
        return ans;
    }
};

#endif