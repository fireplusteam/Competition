#ifndef RandomDataGenerator_h
#define RandomDataGenerator_h
#include <functional>
#include <random>
#include <vector>
using namespace std;

/// Generate Tree data in form of (u, v) pairs of n vertices
vector<pair<int, int>> generateTree(int n) {
    auto gen = n - 1;
    int v    = 1;
    vector<pair<int, int>> ans;

    function<void(int, int)> genDfs = [&](int u, int p) {
        if (gen == 0)
            return;
        int r = rand() % (gen + 1);
        vector<int> edgs;
        for (int i = 0; i < r; ++i) {
            ans.push_back({u, v});
            edgs.push_back(v);
            ++v;
        }
        gen -= r;
        for (auto i : edgs) {
            if (p == i)
                continue;
            genDfs(i, u);
        }
    };
    genDfs(0, -1);
    return ans;
}

#endif