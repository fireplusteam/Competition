#define LOCAL

#ifdef LOCAL
#include "Helper/LogHelper.h"
#endif

////-----SOLUTION STARTS HERE ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#include <iostream>
#include <fstream>
#include <map>
#include <set>
#include <algorithm>
#include <sstream>
#include <stdio.h>
#include <queue>
#include <cassert>
#include <functional>

#ifndef LOCAL
class debug {public: debug(bool isend = true){} template<class c> debug& operator<<(const c&) { return *this; }};
#define imie(...) ""
#define endl "\n"
#endif

/// START: Algos helper
#ifdef LOCAL
#include "Algo/Rational.h"
#include "Algo/max_flow_dinic.h"
#include "Helper/InputParserHelper.h"
#endif
/// END: Algos helpers

using namespace std;

struct M {
    long long x, vx, y, vy, z, vz;
    
    /*friend bool operator<(const M&a, const M& b) {
        if(a.cost != b.cost) return a.cost < b.cost;
        if(a.i != b.i) return  a.i < b.i;
        return a.j < b.j;
    }*/
    
    friend ostream& operator<<(ostream &o, const M& a) {
        //debug(false) << "(" << imie(a.i) imie(a.j) imie(a.cost) << ")";
        return o;
    }
};

int main(int argc, const char * argv[]) {
    
    ifstream in("input.txt");
    
    string str;
    
    long long sum = 0;
    while(getline(in, str)) {
        
    }
    
    // insert code here...
    debug() << imie((sum));
    
    return 0;
}
