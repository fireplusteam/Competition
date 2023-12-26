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
#include <numeric>
#include <tuple>

#ifndef LOCAL
class debug {public: debug(bool isend = true){} template<class c> debug& operator<<(const c&) { return *this; }};
#define imie(...) ""
#define endl "\n"
#endif

using namespace std;

struct M {
    vector<string> link;
    int rate;
    
    /*friend bool operator==(const M&a, const M& b) {
        return a.t == b.t && a.ind == b.ind && a.mask == b.mask;
    }*/

    friend ostream& operator<<(ostream &o, const M& a) {
        debug(false) << "(" << imie(a.link) imie(a.rate) << ")";
        return o;
    }
};

int maxT = 26;

map<string, M> road;
map<tuple<string, int, set<string> >, int> dp;

queue<tuple<string, int, set<string>>> q;

int rec(set<string> path, string root, int t) {
    
    q.push( {root, t, path});
    dp[{root, t, path}] = 0;
    
    while(!q.empty()) {
        auto top = q.front();
        q.pop();
        int t = get<1>(top);
        if(t >= maxT) {
            continue;
        }
        auto root = get<0>(top);
        auto path = get<2>(top);
        int currentVal = dp[{root, t, path}];
        
        
        //debug() << tabs(path.size()) << imie(root) imie(t);
        auto next = road[root];
        
        int r = (maxT - (t + 1)) * next.rate;
        
        int rate = next.rate;
        for(auto n: next.link) {
            if(!path.contains(root) && rate != 0) {
                path.insert(root);
                
                tuple<string, int, set<string>> key {n, t + 2, path};
                if(dp.contains(key) == false || dp[key] < r + currentVal) {
                    dp[key] = r + currentVal;
                    q.push(key);
                }
                //int r1 = max(rr, r + rec(path, n, t + 2));
                path.erase(root);
            }
            
            tuple<string, int, set<string>> key {n, t + 1, path};
            
            if(dp.contains(key) == false || dp[key] < currentVal) {
                dp[key] = currentVal;
                q.push(key);
            }
            //rr = max(rr, rec(path, n, t + 1));
        }
    }
    
    return 0;
}


int main(int argc, const char * argv[]) {
    ifstream in("input.txt");
    
    string str;
    
    long long sum = 0;
    
    while(getline(in, str)) {
        auto s = splitByStrings(str, {"Valve ", " has flow rate=", "; tunnels lead to valves ", "; tunnel leads to valve "});
        auto key = s[0];
        int rate = atoi(s[1].c_str());
        auto links = splitByStrings(s[2], {", "});
        road[key] = { links, rate };
        
        debug() << imie(s);
    }
    debug() << imie(road);
    
    set<string> notZero;
    for(auto key : road) {
        if(key.second.rate != 0) {
            notZero.insert(key.first);
        }
    }
    
    debug() << imie(notZero);
    
    map<string, int> indMapper;
    int i = 0;
    for(auto m: notZero) {
        indMapper[m] = i;
        ++i;
    }
    
    debug() << imie(indMapper);
    
    debug() << imie(rec({}, "AA", 0));
        
    vector<int> fastDp(1 << indMapper.size(), 0);
    for(auto p : dp) {
        int dp_ind = 0;
        for(auto path: get<2>(p.first)) {
            dp_ind += 1 << indMapper[path];
        }
        fastDp[dp_ind] = max(fastDp[dp_ind], p.second);
    }
    debug() << imie(fastDp);
    for(int i = 1;i < (1 << indMapper.size());++i)
        for(int j = 1;j < (1 << indMapper.size());++j) {
            if((i & j) == 0) {
                sum = max(sum, (long long)fastDp[i] + fastDp[j]);
            }
        }
    
    // insert code here...
    debug() << imie((sum));

    return 0;
}
