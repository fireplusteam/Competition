//
//  main.cpp
//  Solver
//
//  Created by Ievgenii Mykhalevskyi on 01.12.2023.
//

#include <iostream>
#include <fstream>
#include <map>
#include <set>
#include <algorithm>
#include <sstream>
#include <stdio.h>
#include <queue>

#define LOCAL

#ifdef LOCAL
#include "LogHelper.h"
#else
class debug {
public:
    debug(bool isend = true){}
    template<class c> debug& operator<<(const c&) { return *this; }
};
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
        debug(false) << imie(a.i) imie(a.j) imie(a.cost);
        return o;
    }
};


int main(int argc, const char * argv[]) {
    ifstream in("input.txt");
    
    string str;
    
    int64_t sum = 0;
    
    while(getline(in, str)) {
        
    }
    
    vector<int> a = {0, 1, 2, 3};

    vector<M> v = {{0, 1, 2}, {10,20, 30}};
    
    debug() << imie(v);
    
    debug() << imie(a);
    
    // insert code here...
    debug() << imie((sum));
    
    return 0;
}
