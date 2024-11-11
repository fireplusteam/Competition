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
    debug &operator<<(c &) {
        return *this;
    }
    debug &operator<<(ostream &(*f)(ostream &)) {
        return *this;
    }
};
    #define imie(...) ""
    #define tabs(a)   ""
#else
    #include "Helpers.h"
#endif

// #include "Ext_Templates.h"

using namespace std;

class Solver {

public:
    void solve() {
        // solution is here
        int T;
        cin >> T;
        cout << imie(T) << endl;
        for (int t = 0; t < T; ++t) {
            // cout << t << endl;
        }
    }
};

// ------------ CONFIGURATION -------------------------

int main(int argc, const char *argv[]) {
    ios_base::sync_with_stdio(true);
#ifdef LOCAL
    ifstream inLocal;
    auto config = [&](const std::string &filename) {
        inLocal = ifstream(filename);
        std::cin.tie(0);
        std::cin.rdbuf(inLocal.rdbuf());
    };
#endif

    auto testSamples = [&config](const string &i) {
        cout << "----------------------------------------------" << endl;
        cout << "Test Case #" << i << ":" << endl;
        const auto fileName = string("../input/input_") + i + ".txt";
        config(fileName);
        Solver solver;
        solver.solve();
    };
    // Test Cases
    testSamples("1");
    testSamples("2");

    return 0;
}
