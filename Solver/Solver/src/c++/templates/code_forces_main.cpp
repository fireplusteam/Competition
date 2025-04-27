#if !defined(__clang__) && defined(__GNUC__)
    #include <bits/stdc++.h>
using namespace std;
#endif

#ifndef LOCAL
class debug {
public:
    debug(bool = false) {
    }
    template <class c>
    debug& operator<<(c&) {
        return *this;
    }
    debug& operator<<(ostream& (*f)(ostream&)) {
        return *this;
    }
};
    #define imie(...) ""
    #define tabs(a)   ""
#else
    #include "Helpers.h"
#endif


void precalculate() {
    // data needed for all test cases
}

void solve() {
}

int main(int argc, const char* argv[]) {
    ios_base::sync_with_stdio(false);
#ifdef LOCAL
    ifstream in("input_1.txt");
    // freopen("input_1.txt", "r", stdin);
    std::cin.tie(0);
    std::cin.rdbuf(in.rdbuf());

    clock_t start = clock();
#endif
    precalculate();

    int T;
    cin >> T;
    for (int t = 0; t < T; ++t) {
        debug() << "Test Case #" << t << "       ---------------------------------------";
        solve();
    }

#ifdef LOCAL
    clock_t end         = clock();
    double elapsed_time = double(end - start) / CLOCKS_PER_SEC;
    std::cout << "Execution time: " << elapsed_time << " seconds" << std::endl;
#endif

    return 0;
}
