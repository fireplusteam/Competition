#ifndef compresser_h
#define compresser_h

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

// Unordered Coordinats compression, map coordinates to range [0, n], where n is the number of distinct values in a
template <class T>
class Compresser {
    unordered_map<T, int> mp;
    vector<T> orig;

public:
    // if you want not to sort it, use isSorted = false
    Compresser(const vector<T> &a, bool isSorted = true) {
        auto b = a;
        if (isSorted)
            sort(b.begin(), b.end());
        for (int i = 0; i < (int)a.size(); ++i) {
            if (mp.contains(b[i]) == false) {
                mp[b[i]] = (int)orig.size();
                orig.push_back(b[i]);
            }
        }
    }
    int compressed(const T &a) {
        return mp[a];
    }
    vector<int> compressed(const vector<T> &a) {
        vector<int> r(a.size());
        for (int i = 0; i < (int)a.size(); ++i) {
            r[i] = mp[a[i]];
        }
        return r;
    }
    T uncompressed(const int &a) {
        return orig[a];
    }
    vector<T> uncompressed(const vector<int> &a) {
        vector<T> r(a.size());
        for (int i = 0; i < (int)a.size(); ++i) {
            r[i] = orig[a[i]];
        }
        return r;
    }
};

#endif