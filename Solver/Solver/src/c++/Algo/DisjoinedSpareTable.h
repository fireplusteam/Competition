#ifndef DisjoinedSpareTable_h
#define DisjoinedSpareTable_h

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

// https://discuss.codechef.com/t/tutorial-disjoint-sparse-table/17404
// Prebuild in O(nlog(n))
// answer query in O(1)
// set define function like [&](int a, int b) { return min(a, b); } or similar
// Example of usage of calculating GCD on a range
// vector<long long> a(n); // init state
// DisjoinedSpareTable<long long> table(a.size(), [&](int index) {
//     if (index < a.size()) {
//         return a[index];
//     }
//     return 1LL;
// }, [&](long long a, long long b) { return gcd(a, b); });
template <class T>
class DisjoinedSpareTable {
    int maxLev;
    vector<T> table[32];
    std::function<T(int)> initialValue; // init value at index
    std::function<T(T, T)> func;
    void build(int level, int l, int r) {
        int m           = (l + r) / 2;

        table[level][m] = initialValue(m);
        for (int i = m - 1; i >= l; i--)
            table[level][i] = func(table[level][i + 1], initialValue(i));

        if (m + 1 < r) {
            table[level][m + 1] = initialValue(m + 1);
            for (int i = m + 2; i < r; i++)
                table[level][i] = func(table[level][i - 1], initialValue(i));
        }
        if (r - l > 1) // r - l > 1
        {
            build(level + 1, l, m);
            build(level + 1, m, r);
        }
    }

public:
    DisjoinedSpareTable(int n, const std::function<T(int)> &_initValue, const std::function<T(T, T)> &func) {
        this->initialValue = _initValue;
        this->func         = func;
        int size           = n;
        maxLev             = __builtin_clz(size) ^ 31;

        if ((1 << maxLev) != size) {
            size = 1 << ++maxLev;
        }
        for (int i = 0; i <= maxLev; ++i) {
            table[i].resize(size);
        }
        build(0, 0, size);
    }

    T query(int x, int y) {
        if (x == y)
            return initialValue(x);
        int k2  = __builtin_clz(x ^ y) ^ 31;
        int lev = maxLev - 1 - k2;
        int ans = table[lev][x];
        if (y & ((1 << k2) - 1)) // y % (1<<k2)
            ans = func(ans, table[lev][y]);
        return ans;
    }
};


// Simple SpareTable, not suitable for sum on a range, only for min/max/gcd
template <class T>
class SpareTable {
    vector<int> lg;
    vector<T> st[30];
    int n;
    function<T(T, T)> mergeFunc;

public:
    SpareTable(const vector<T> &arr, const function<T(T, T)> &_func)
        : mergeFunc(_func) {
        n = (int)arr.size();
        lg.resize(n + 1);
        lg[1] = 0;
        for (int i = 2; i <= n; ++i) {
            lg[i] = lg[i / 2] + 1;
        }
        st[0]      = arr;
        auto power = [&](int p) {
            int r = 0;
            while (p > 0) {
                r  += 1;
                p >>= 1;
            }
            return r + 1;
        };
        const int K = power(n);
        for (int i = 1; i <= K; ++i) {
            st[i].resize(n);
            for (int j = 0; j + (1 << i) <= n; ++j) {
                st[i][j] = mergeFunc(st[i - 1][j], st[i - 1][j + (1 << (i - 1))]);
            }
        }
    }

    T query(int l, int r) {
        int i = lg[r - l + 1];
        return mergeFunc(st[i][l], st[i][r - (1 << i) + 1]);
    }
};

#endif