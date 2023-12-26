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
    string command;
    string next;
    
    string sing;
    int number;
    
    /*friend bool operator==(const M&a, const M& b) {
        return a.t == b.t && a.ind == b.ind && a.mask == b.mask;
    }*/

    friend ostream& operator<<(ostream &o, const M& a) {
        debug(false) << "(" << imie(a.command) imie(a.next) imie(a.sing) imie(a.number) << ")";
        return o;
    }
};


int main(int argc, const char * argv[]) {
    ifstream in("input.txt");
    
    string str;
    
    long long sum = 0;
   
    map<string, bool> flipFlop;
    map<string, map<string, bool>> conj;
    
    map<string, vector<string>> graph;
    
    while(getline(in, str)) {
        auto pp = splitByStrings(str, { " -> ", ", "});
        if (pp[0] == "broadcaster") {
            auto key = pp[0];
            pp.erase(pp.begin());
            graph[key] = pp;
            continue;
        }
        auto key = pp[0].substr(1);
        
        if(pp[0][0] == '%') {
            flipFlop[key] = false;
        } else {
            conj[key] = {};
        }
        pp.erase(pp.begin());
        graph[key] = pp;
    }
    for(auto u: graph)  {
        for(auto v: u.second) {
            if(conj.contains(v)) {
                conj[v][u.first] = false;
            }
        }
    }
    
    debug() << imie(graph);
    debug() << imie(flipFlop);
    debug() << imie(conj);
    int sum_low = 0;
    int sum_high = 0;
    bool is_found = false;
    int rep = 0;
    for(rep = 0;is_found == false;++rep) {
        queue<pair<string, bool>> q;
        q.push({"broadcaster", false});
        int r_high = 0;
        int r_low = 1;
        
        while(!q.empty() ) {
            
            auto count_move = [&](bool u_state) {
                r_high += u_state;
                r_low += !u_state;
            };
            
            auto make_move = [&](const string& u, const string &v, bool u_state) {
                if (flipFlop.contains(v)) {
                    bool v_state = flipFlop[v];
                    
                    if(!u_state) {
                        flipFlop[v] = !v_state;
                        
                        q.push({v, !v_state});
                    }
                } else if(conj.contains(v)) {
                    conj[v][u] = u_state;
                    bool is_high = true;
                    for(auto in: conj[v]) {
                        is_high = is_high && in.second;
                    }
                    q.push({v, !is_high});
                }
                if(v == "rx" && !u_state) {
                    is_found = true;
                }
                count_move(u_state);
            };
            
            const auto &[u, u_state] = q.front();
            q.pop();
            
            for(const auto &v : graph[u]) {
                make_move(u, v, u_state);
            }
            
        }
        
    }
    sum = sum_low * sum_high;
    debug() << imie(sum_low) imie(sum_high) imie((sum));
    debug() << imie(rep);
    return 0;
}
