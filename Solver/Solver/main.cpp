#if !defined(__clang__) && defined(__GNUC__)
#include <bits/stdc++.h>
#include <ext/pb_ds/assoc_container.hpp> // Common file
#include <ext/pb_ds/tree_policy.hpp> // Including tree_order_statistics_node_update
#include <ext/pb_ds/detail/standard_policies.hpp>
using namespace std;
using namespace __gnu_pbds;
template <typename K, typename V, typename Comp = std::less<K>> using ordered_map = tree< K, V, Comp, rb_tree_tag, tree_order_statistics_node_update >; 
template <typename K, typename Comp = std::less<K>> using ordered_set = ordered_map<K, null_type, Comp>;
#endif

#ifndef LOCAL
class debug{public:debug(bool isend=true){}template<class c>debug&operator<<(c&){return *this;}debug&operator<<(ostream&(*f)(ostream&)){return *this;}};
#define imie(...) ""
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
