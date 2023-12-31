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
#include <optional>
#if !defined(__clang__) && defined(__GNUC__)
#include <ext/pb_ds/assoc_container.hpp> // Common file
#include <ext/pb_ds/tree_policy.hpp> // Including tree_order_statistics_node_update
#include <ext/pb_ds/detail/standard_policies.hpp>
using namespace __gnu_pbds;
#endif
using namespace std;

#if !defined(__clang__) && defined(__GNUC__)
template<class A> using ordered_set = tree<A, null_type, less<A>, rb_tree_tag, tree_order_statistics_node_update>;
template<class Key, class Value> using ordered_map = tree<Key, Value, less<Value>, rb_tree_tag, tree_order_statistics_node_update>;
#endif

#ifndef LOCAL
class debug {public: debug(bool isend = true){} template<class c> debug& operator<<(const c&) { return *this; }};
#define imie(...) ""
#define endl "\n"
#define tabs(a) ""
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
