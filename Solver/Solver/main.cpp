#define LOCAL

#ifdef LOCAL
#include "LogHelper.h"
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

#ifndef LOCAL
class debug {public: debug(bool isend = true){} template<class c> debug& operator<<(const c&) { return *this; }};
#define imie(...) ""
#define endl "\n"
#endif

using namespace std;

struct M {
    int i, j;
    int cost;
    
    friend bool operator<(const M&a, const M& b) {
        if(a.cost != b.cost) return a.cost < b.cost;
        if(a.i != b.i) return  a.i < b.i;
        return a.j < b.j;
    }
    
    friend ostream& operator<<(ostream &o, const M& a) {
        debug(false) << "(" << imie(a.i) imie(a.j) imie(a.cost) << ")";
        return o;
    }
};


int main(int argc, const char * argv[]) {
    ifstream in("input.txt");
    
    string str;
    
    int64_t sum = 0;
    
    while(getline(in, str)) {
        
    }
    
    // insert code here...
    debug() << imie((sum));
    
    return 0;
}
