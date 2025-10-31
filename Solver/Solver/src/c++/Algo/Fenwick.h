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
class FenwickMax {
    vector<int> val;
    int inf;

public:
    FenwickMax(int n, int _inf = INT_MIN)
        : val(n + 1, _inf),
          inf(_inf) {
    }

    // update on [x] with val
    void update(int x, int _val) {
        x += 1;
        assert(1 <= x && x < this->val.size());
        while (x < this->val.size()) {
            this->val[x]  = max(this->val[x], _val);
            x            += x & -x;
        }
    }
    // max on [0, l]
    int get(int l) {
        ++l;
        assert(1 <= l && l < val.size());
        int ans = inf;
        while (l > 0) {
            ans  = max(ans, val[l]);
            l   -= l & -l;
        }
        return ans;
    }
};

// MIN Fenwick

class FenwickMin {
    vector<int> val;
    int inf;

public:
    FenwickMin(int n, int _inf = INT_MAX)
        : val(n + 1, _inf),
          inf(_inf) {
    }

    // update on [x] with val
    void update(int x, int _val) {
        x += 1;
        assert(1 <= x && x < this->val.size());
        while (x < this->val.size()) {
            this->val[x]  = min(this->val[x], _val);
            x            += x & -x;
        }
    }
    // max on [0, l]
    int get(int l) {
        ++l;
        assert(1 <= l && l < val.size());
        int ans = inf;
        while (l > 0) {
            ans  = min(ans, val[l]);
            l   -= l & -l;
        }
        return ans;
    }
};

#endif