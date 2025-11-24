#ifndef disjoined_set_rollback_h
#define disjoined_set_rollback_h

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
/// Disjoined Set that supports rollback
/// Example:
/// DisjoinedSet st;
/// st.persist();
/// st.union(1, 2);
/// st.union(3, 4);
/// st.rollback(); /// rollback to before persist method is called
class DisjoinedSet {
    vector<int> p;
    vector<int> len;
    vector<int> rollbackInds;
    int unique;
    struct RestoreState {
        int a;
    };
    vector<RestoreState> restore;

public:
    DisjoinedSet(int n)
        : p(n),
          len(n),
          unique(n) {
        for (int i = 0; i < n; ++i) {
            p[i]   = i;
            len[i] = 1;
        }
    }

    int get(int x) {
        while (x != p[x])
            x = p[x];
        return x;
    }

    void unite(int x, int y) {
        int a = get(x);
        int b = get(y);
        if (a == b)
            return;
        if (len[a] > len[b])
            swap(a, b);
        restore.push_back({a});
        unique -= 1;
        p[a]    = b;
        len[b] += len[a];
    }
    void persist() {
        rollbackInds.push_back((int)restore.size());
    }
    void rollback() {
        assert(rollbackInds.size() > 0);
        while (restore.size() > rollbackInds.back()) {
            auto state  = restore.back();
            unique     += 1;
            int a       = state.a;
            int b       = p[a];
            p[a]        = a;
            len[b]     -= len[a];
            restore.pop_back();
        }
        rollbackInds.pop_back();
    }
    int getUniqueSets() {
        return unique;
    }
};

// Max Disjoined Set
class DisjoinedSet {
    vector<int> p;
    vector<int> maxElement;

public:
    DisjoinedSet(vector<int> v) {
        int n      = (int)v.size();
        p          = vector<int>(n);
        maxElement = v;
        for (int i = 0; i < n; ++i) {
            p[i] = i;
        }
    }

    int get(int x) {
        if (x != p[x])
            return p[x] = get(p[x]);
        return x;
    }

    void unite(int x, int y) {
        int a = get(x);
        int b = get(y);
        if (a == b)
            return;
        p[a]          = b;
        maxElement[b] = max(maxElement[b], maxElement[a]);
    }
    int getMaxElement(int i) {
        i = get(i);
        return maxElement[i];
    }
};

#endif