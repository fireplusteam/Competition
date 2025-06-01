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
    Compresser(const vector<T> &a) {
        // if you want to preserve the order of compressed coordinate, we need to sort before performing compression
        // sort(a.begin(), a.end());
        for (int i = 0; i < (int)a.size(); ++i) {
            if (mp.contains(a[i]) == false) {
                mp[a[i]] = (int)orig.size();
                orig.push_back(a[i]);
            }
        }
    }
    vector<int> compressed(const vector<T> &a) {
        vector<int> r(a.size());
        for (int i = 0; i < (int)a.size(); ++i) {
            r[i] = mp[a[i]];
        }
        return r;
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