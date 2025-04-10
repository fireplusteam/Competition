#ifndef modular_arithmetic_h
#define modular_arithmetic_h

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

template <class T>
T gcd(T a, T b) {
    if (a == 0 || b == 0)
        return max(a, b);
    while (b > 0) {
        auto c = b;
        b      = a % b;
        a      = c;
    }
    return a;
}

// linear equation a * x + b * x = gcd(a, b)
template <class T>
T extendedEuclid(T a, T b, T& x, T& y) {
    x = 1, y = 0;
    T x1 = 0, y1 = 1, a1 = a, b1 = b;
    T _x1, _y1, _b1, q;
    while (b1) {
        q   = a1 / b1;

        _x1 = x1;
        x1  = x - q * x1;
        x   = _x1;

        _y1 = y1;
        y1  = y - q * y1;
        y   = _y1;

        _b1 = b1;
        b1  = a1 - q * b1;
        a1  = _b1;
    }
    return a1;
}

// a^(-1) to a mod n if a and n are comprime
template <class T>
T modularInverse(T a, T n) {
    T x, y;
    auto g = extendedEuclid(a, n, x, y);
    if (g != 1) {
        return -1; // no solutions
    }
    x = (x % n + n) % n;
    return x;
}

// all solutions of a * x = b mod n
// if a == 0 and b == 0 all from (0, n - 1)
template <class T>
vector<T> linearSolutions(T a, T b, T n) {
    a      = (a % n + n) % n;
    b      = (b % n + n) % n;
    auto g = gcd(a % n, n);
    if (b % g != 0) {
        return {};
    }
    vector<T> ans;
    if (g == n) {
        for (int i = 0; i < n; ++i)
            ans.push_back(i);
        return ans;
    }
    auto _a = modularInverse(a / g, n / g);
    // assert(_a * a / g % (n / g) == 1);
    for (int j = 0; j < g; ++j) {
        auto sol = (_a * (b / g) + j * n / g) % n;
        // assert((a * sol - b) % n == 0);
        ans.push_back(sol);
    }
    return ans;
}
#endif