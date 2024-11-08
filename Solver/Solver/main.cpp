#if !defined(__clang__) && defined(__GNUC__)
#    include <bits/stdc++.h>
using namespace std;
#endif

#ifndef LOCAL
class debug {
public:
    debug(bool = false) {
    }
    template <class c>
    debug &operator<<(c &) {
        return *this;
    }
    debug &operator<<(ostream &(*f)(ostream &)) {
        return *this;
    }
};
#    define imie(...) ""
#    define tabs(a) ""
#else
#    include "Helpers.h"
#endif

using namespace std;
void solve() {
    // solution is here
}

int main(int argc, const char *argv[]) {
    ios_base::sync_with_stdio(true);
#ifdef LOCAL
    ifstream in("input.txt");
    std::cin.tie(0);
    std::cin.rdbuf(in.rdbuf());
#endif

    int T;
    cin >> T;
    cout << imie(T) << endl;
    for (int t = 0; t < T; ++t) {
        solve();
    }
    return 0;
}
