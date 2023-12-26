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
#include <cassert>
#include <functional>

#ifndef LOCAL
class debug {public: debug(bool isend = true){} template<class c> debug& operator<<(const c&) { return *this; }};
#define imie(...) ""
#define endl "\n"
#endif

using namespace std;

struct M {
    bool isOn;
    int x1, x2, y1, y2, z1, z2;
    
    /*friend bool operator<(const M&a, const M& b) {
        if(a.cost != b.cost) return a.cost < b.cost;
        if(a.i != b.i) return  a.i < b.i;
        return a.j < b.j;
    }*/
    
    friend ostream& operator<<(ostream &o, const M& a) {
        debug(false) << "(" << imie(a.x1) imie(a.x2) imie(a.y1) imie(a.y2) imie(a.z1) imie(a.z2) imie(a.isOn) << ")";
        return o;
    }
};


int main(int argc, const char * argv[]) {
    ifstream in("input.txt");
    
    string str;
    
    int64_t sum = 0;
    
    vector<M> states;
    while(getline(in, str)) {
        auto p = splitByStrings(str, {" x=", "..", ",", "y=" ,"z="});
        M val;
        if(p[0] == "on")
            val.isOn = true;
        else val.isOn = false;
        
        val.x1 = atoi(p[1].c_str());
        val.x2 = atoi(p[2].c_str());
        val.y1 = atoi(p[3].c_str());
        val.y2 = atoi(p[4].c_str());
        val.z1 = atoi(p[5].c_str());
        val.z2 = atoi(p[6].c_str());
        states.push_back(val);
    }
    int minZ = 0;
    int maxZ = 0;
    for(auto state : states) {
        minZ = min(state.z1, minZ);
        maxZ = max(state.z2, maxZ);
    }
    
    debug() << imie(minZ) imie(maxZ) imie(states.size());
    
    for(int x = -50;x <= 50;++x)
        for(int y = -50;y <= 50;++y)
            for(int z = -50;z <= 50;++z) {
                bool is_on = false;
                for(auto step : states) {
                    if(step.x1 <= x && x <= step.x2 && step.y1 <= y && y <= step.y2 && step.z1 <= z && z <= step.z2)
                        is_on = step.isOn;
                }
                sum += is_on;
            }
    
    // insert code here...
    debug() << imie((sum));
    
    return 0;
}
