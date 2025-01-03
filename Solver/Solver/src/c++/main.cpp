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

#include "Ext_Templates.h"

using namespace std;

class Solver {

public:
    string solve(const string &testCase) {
        // solution is here
        string s;
        long long ans = 0;
        while (getline(cin, s)) {
        }

        return to_string(ans);
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

    auto testSamples = [&config](const string &i, string expected = "") {
        cout << "----------------------------------------------" << endl;
        cout << "Test Case #" << i << ":" << endl;
        const auto fileName = string("input_") + i + ".txt";
        config(fileName);
        Solver solver;
        auto ans = solver.solve(i);
        cout << "  #" << i;
        if (expected == "") {
            cout << " Answer = " << ans << " ," << " No expected answer Provided" << endl;
        } else {
            if (expected == ans) {
                cout << " Answer Correct = " << ans << "" << endl;
            } else {
                cout << " Wrong Answer = " << ans << " , Expected: " << expected << endl;
            }
        }
    };
    // Test Cases
    testSamples("1");
    // testSamples("2");

    testSamples("puzzle");

    return 0;
}
