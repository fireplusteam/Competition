#ifndef mint_h
#define mint_h

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


const int mod = 998244353;

template <int mod>
struct MInt {
    int x;

    MInt() {
        x = 0;
    }
    MInt(int32_t xx) {
        x = xx % mod;
        if (x < 0)
            x += mod;
    }
    MInt(long long xx) {
        x = xx % mod;
        if (x < 0)
            x += mod;
    }

    int val() {
        return x;
    }
    MInt &operator++() {
        x++;
        if (x == mod)
            x = 0;
        return *this;
    }
    MInt &operator--() {
        if (x == 0)
            x = mod;
        x--;
        return *this;
    }
    MInt operator++(int32_t) {
        MInt result = *this;
        ++*this;
        return result;
    }

    MInt operator--(int32_t) {
        MInt result = *this;
        --*this;
        return result;
    }
    MInt &operator+=(const MInt &b) {
        x += b.x;
        if (x >= mod)
            x -= mod;
        return *this;
    }
    MInt &operator-=(const MInt &b) {
        x -= b.x;
        if (x < 0)
            x += mod;
        return *this;
    }
    MInt &operator*=(const MInt &b) {
        long long z  = x;
        z           *= b.x;
        z           %= mod;
        x            = (int)z;
        return *this;
    }
    MInt operator+() const {
        return *this;
    }
    MInt operator-() const {
        return MInt() - *this;
    }
    MInt operator/=(const MInt &b) {
        return *this = *this * b.inv();
    }
    MInt power(long long n) const {
        MInt ok = *this, r = 1;
        while (n) {
            if (n & 1) {
                r *= ok;
            }
            ok  *= ok;
            n  >>= 1;
        }
        return r;
    }
    MInt inv() const {
        return power(mod - 2);
    }
    friend MInt operator+(const MInt &a, const MInt &b) {
        return MInt(a) += b;
    }
    friend MInt operator-(const MInt &a, const MInt &b) {
        return MInt(a) -= b;
    }
    friend MInt operator*(const MInt &a, const MInt &b) {
        return MInt(a) *= b;
    }
    friend MInt operator/(const MInt &a, const MInt &b) {
        return MInt(a) /= b;
    }
    friend bool operator==(const MInt &a, const MInt &b) {
        return a.x == b.x;
    }
    friend bool operator!=(const MInt &a, const MInt &b) {
        return a.x != b.x;
    }
    MInt power(MInt a, long long n) {
        return a.power(n);
    }
    friend ostream &operator<<(ostream &os, const MInt &m) {
        os << m.x;
        return os;
    }
    explicit operator bool() const {
        return x != 0;
    }
};
typedef MInt<mod> mint;

struct factorials {
    int n;
    vector<mint> fact, invFact;

    factorials(int nn) {
        n = nn;
        fact.resize(n + 1);
        invFact.resize(n + 1);

        fact[0] = 1;
        for (int i = 1; i <= n; i++) {
            fact[i] = fact[i - 1] * i;
        }

        invFact[n] = fact[n].inv();
        for (int i = n - 1; i >= 0; i--) {
            invFact[i] = invFact[i + 1] * (i + 1);
        }
    }

    mint C(int n, int r) {
        if (n == r)
            return mint(1);
        if (n < 0 || r < 0 || r > n)
            return mint(0);
        return fact[n] * invFact[r] * invFact[n - r];
    }

    mint P(int n, int r) {
        if (n < 0 || r < 0 || r > n)
            return mint(0);
        return fact[n] * invFact[n - r];
    }

    mint solutions(int n, int r) {
        // Solutions to x1 + x2 + ... + xn = r, xi >= 0
        return C(n + r - 1, n - 1);
    }

    mint catalan(int n) {
        return fact[2 * n] * invFact[n] * invFact[n + 1];
    }
};

// Remember to check MOD

#endif