#include <iostream>
#include <fstream>
#include <map>
#include <set>
#include <algorithm>
#include <sstream>
#include <cstdio>
#include <queue>
#include <cassert>
#include <functional>
#include <unordered_map>
#include <deque>
#include <unordered_set>
#include <complex>
#include <list>
#include <bitset>
#include <ctime>
#include <random>
#include <stack>

#ifndef LOCAL
class debug {public: debug(bool isend = true){} template<class c> debug& operator<<(const c&) { return *this; }};
#define imie(...) ""
#define endl "\n"
#else
#include "Helpers.h"
#endif

using namespace std;
void solve() {
    // solution is here
    
}

int main(int argc, const char * argv[]) {
    ios_base::sync_with_stdio(false);
#ifdef LOCAL
    ifstream in("input.txt");
    std::cin.tie(0);
    std::cin.rdbuf(in.rdbuf());
#endif
    
    int T;
    cin >> T;
    for(int t = 0;t < T;++t) {
        solve();
    }
    return 0;
}
