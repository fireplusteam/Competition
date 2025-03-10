#ifndef string_hash_h
    #define strin_hash_h

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

// Class for handling string hashing
class StringHash {
public:
    StringHash(const string &s)
        : n((int)s.size()),
          h1(n + 1),
          h2(n + 1),
          p1Inverse(n + 1, -1),
          p2Inverse(n + 1, -1) {

        int p1       = 1;
        int p2       = 1;

        p1Inverse[0] = 1;
        p2Inverse[0] = 1;

        for (int i = 1; i <= n; ++i) {
            h1[i] = (h1[i - 1] + (long long)s[i - 1] * p1) % MOD1;
            h2[i] = (h2[i - 1] + (long long)s[i - 1] * p2) % MOD2;
            p1    = (long long)p1 * P1 % MOD1;
            p2    = (long long)p2 * P2 % MOD2;
        }
    }

    /// get a hash of substring in a range [l, r]
    long long getHash(int l, int r) {
        assert(0 <= l < n);
        assert(0 <= r < n);
        assert(l <= r);
        int hash1 = ((long long)h1[r + 1] - h1[l] + MOD1) * inv1(l) % MOD1;
        int hash2 = ((long long)h2[r + 1] - h2[l] + MOD2) * inv2(l) % MOD2;
        return ((long long)hash1 << 32) + hash2;
    }

    /// get hash of entire string
    long long hash() {
        return getHash(0, n - 1);
    }

    /// compute hash of the arbitrary string without precomputing powers for substrings
    static long long hash(const string &s) {
        long long p1 = 1, p2 = 1;
        int hash1 = 0, hash2 = 0;
        for (int i = 1; i <= (int)s.size(); ++i) {
            hash1 = (hash1 + (long long)s[i - 1] * p1) % MOD1;
            hash2 = (hash2 + (long long)s[i - 1] * p2) % MOD2;
            p1    = (long long)p1 * P1 % MOD1;
            p2    = (long long)p2 * P2 % MOD2;
        }
        return ((long long)hash1 << 32) + hash2;
    }

private:
    int inv1(int i) {
        if (p1Inverse[i] == -1)
            p1Inverse[i] = inversePow(P1, (long long)i * (MOD1 - 2) % (MOD1 - 1), MOD1);
        return p1Inverse[i];
    }
    int inv2(int i) {
        if (p2Inverse[i] == -1)
            p2Inverse[i] = inversePow(P2, (long long)i * (MOD2 - 2) % (MOD2 - 1), MOD2);
        return p2Inverse[i];
    }
    int inversePow(int a, int n, int m) {
        int r = 1;
        while (n > 0) {
            if (n & 1) {
                --n;
                r = (long long)r * a % m;
            } else {
                a   = (long long)a * a % m;
                n >>= 1;
            }
        }
        return r;
    }
    int n;
    vector<int> h1, h2;
    vector<int> p1Inverse, p2Inverse;
    // constants
    const static int P1   = 239017;
    const static int P2   = 648391;
    const static int MOD1 = 1000000007;
    const static int MOD2 = 1000000009;
};

#endif