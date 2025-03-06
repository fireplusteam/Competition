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

// Prebuild in O(nlog(n))
// answer query in O(1)
// set define function like [&](int a, int b) { return min(a, b); } or similar
class DisjoinedSpareTable {
    int maxLev;
    vector<int> table[32];
    vector<int> A;
    std::function<int(int, int)> func;
    void build(int level, int l, int r) {
        int m           = (l + r) / 2;

        table[level][m] = A[m];
        for (int i = m - 1; i >= l; i--)
            table[level][i] = func(table[level][i + 1], A[i]);

        if (m + 1 < r) {
            table[level][m + 1] = A[m + 1];
            for (int i = m + 2; i < r; i++)
                table[level][i] = func(table[level][i - 1], A[i]);
        }
        if (r - l > 1) // r - l > 1
        {
            build(level + 1, l, m);
            build(level + 1, m, r);
        }
    }

public:
    DisjoinedSpareTable(const vector<int> &A, const std::function<int(int, int)> &func) {
        this->A    = A;
        this->func = func;
        int size   = (int)A.size();
        maxLev     = __builtin_clz(size) ^ 31;

        if ((1 << maxLev) != size) {
            size = 1 << ++maxLev;
        }
        for (int i = 0; i <= maxLev; ++i) {
            table[i].resize(size);
        }
        build(0, 0, size);
    }

    int query(int x, int y) {
        if (x == y)
            return A[x];
        int k2  = __builtin_clz(x ^ y) ^ 31;
        int lev = maxLev - 1 - k2;
        int ans = table[lev][x];
        if (y & ((1 << k2) - 1)) // y % (1<<k2)
            ans = func(ans, table[lev][y]);
        return ans;
    }
};

#endif