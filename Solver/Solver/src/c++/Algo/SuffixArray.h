#ifndef suffix_array_h
#define suffix_array_h

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

class MinSpareTable {
    vector<int> lg;
    vector<int> st[30];
    int n;

public:
    MinSpareTable(const vector<int> &arr) {
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
                st[i][j] = min(st[i - 1][j], st[i - 1][j + (1 << (i - 1))]);
            }
        }
    }

    int get(int l, int r) {
        int i = lg[r - l + 1];
        return min(st[i][l], st[i][r - (1 << i) + 1]);
    }
};

/// Prebuild in O(n * log(n))
/// Answer LCP in O(1)
class SuffixArray {
    vector<int> p, eqClasses, lcp;
    string a; // input string
    MinSpareTable *spareTable = nullptr;
    int n;

    void buildLCP() {
        lcp.resize(n, 0);
        int k = 0;
        for (int i = 0; i < n; ++i) {
            int pi = eqClasses[i];
            if (pi == 0) {
                k = 0;
                continue;
            }
            int j = p[pi - 1];
            while (a[i + k] == a[j + k])
                ++k;
            lcp[pi] = k;
            k       = max(k - 1, 0);
        }
    }

public:
    // if tail is zero then a string is cyclic
    SuffixArray(const string &s, char tail = '\1') {
        if (tail != 0)
            a = s + tail;
        else
            a = s;

        n = (int)a.size();
        p.resize(n, 0);

        auto get_power_of_two = [](int n) {
            int two_power = 1;
            if ((n & (n - 1)) == 0) {
                two_power = n;
            } else {
                while (n > 0) {
                    n         >>= 1;
                    two_power <<= 1;
                }
            }
            return two_power;
        };
        int two_power = get_power_of_two(n);

        vector<int> counter(256, 0), pNext(n);
        for (int i = 0; i < n; ++i)
            ++counter[a[i]];
        for (int i = 1; i < 256; ++i)
            counter[i] += counter[i - 1];
        for (int i = n - 1; i >= 0; --i)
            p[--counter[a[i]]] = i;

        eqClasses.resize(n, 0);
        int cnt = 0;
        for (int j = 1; j < n; ++j) {
            if (a[p[j - 1]] == a[p[j]])
                eqClasses[p[j]] = cnt;
            else {
                ++cnt;
                eqClasses[p[j]] = cnt;
            }
        }

        for (int k = 1; k < two_power; k <<= 1) {
            vector<int> eqClassesNext(n, 0);
            counter = vector<int>(n, 0);
            for (int i = 0; i < n; ++i) {
                p[i] = (p[i] - k) % n;
                if (p[i] < 0)
                    p[i] += n;
                ++counter[eqClasses[p[i]]];
            }
            for (int i = 1; i < n; ++i)
                counter[i] += counter[i - 1];
            for (int i = n - 1; i >= 0; --i)
                pNext[--counter[eqClasses[p[i]]]] = p[i];
            p.swap(pNext);
            cnt = 0;
            for (int j = 1; j < n; ++j) {
                if (eqClasses[p[j - 1]] == eqClasses[p[j]] &&
                    eqClasses[(p[j] + k) % n] == eqClasses[(p[j - 1] + k) % n])
                    eqClassesNext[p[j]] = cnt;
                else {
                    ++cnt;
                    eqClassesNext[p[j]] = cnt;
                }
            }
            eqClasses.swap(eqClassesNext);
        }
    }

    ~SuffixArray() {
        delete spareTable;
    }

    const vector<int> &getP() const {
        return p;
    }

    const string &getString() const {
        return a;
    }

    int getSize() const {
        return (int)p.size();
    }

    int LCP(int i, int j) {
        if (i > j) {
            static_assert("i should be less j");
        }
        if (lcp.size() == 0) {
            buildLCP();
        }
        int pi = eqClasses[i];
        int pj = eqClasses[j];
        if (pi == pj) {
            return n - i;
        }
        if (spareTable == nullptr) {
            spareTable = new MinSpareTable(lcp);
        }
        return spareTable->get(min(pi, pj) + 1, max(pi, pj));
    }

    // compare sub arrays [i.first, i.second] and [j.first, j.second]
    bool cmpSubs(const pair<int, int> &i, const pair<int, int> &j) {
        int k = LCP(i.first, j.first);
        if (k >= min(i.second - i.first + 1, j.second - j.first + 1)) {
            if (i.second - i.first == j.second - j.first) {
                if (i.first != j.first) {
                    return i.first < j.first;
                }
                return i.second < j.second;
            } else {
                return i.second - i.first < j.second - j.first;
            }
        }
        return a[(i.first + k) % a.size()] < a[(j.first + k) % a.size()];
    }

    int compareStringWithSuffix(const string &sub, int i) {
        int cmp = 0;
        for (int j = 0; j < (int)sub.size() && cmp == 0; ++j) {
            int ind = (p[i] + j) % n;
            cmp     = a[ind] - sub[j];
        }
        return cmp;
    }

    int findString(const string &sub) {
        int l = 0, r = n - 1;
        while (l <= r) {
            int mid = (l + r) >> 1;
            int cmp = compareStringWithSuffix(sub, mid);
            if (cmp == 0) {
                return mid;
            } else if (cmp > 0) {
                r = mid - 1;
            } else {
                l = mid + 1;
            }
        }
        return -1;
    }
};

#endif