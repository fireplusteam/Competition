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

vector<pair<int, int>> dir {{0,1}, {0,-1}, {1, 0}, {-1, 0}};

int modulesBy1(int a) {
    if(a < 0) return -1;
    if(a > 0) return 1;
    return 0;
}

long long smart(vector<string> field, int steps) {
    queue<pair<int,int>> q;
    
    int n = field.size();
    map<pair<int, int>, int> dp;
    
    int start_pos = 0;
    
    for(int i = 0;i < n;++i) {
        for(int j = 0;j < n;++j)
            if(field[i][j] == 'S') {
                q.push({i, j});
                field[i][j] = '.';
                dp[{i, j}] = 0;
                start_pos = i;
            }
    }
    
    int max_brute_force_steps = n * 2 + 1;
    
    set<pair<int, int>> visible;
    
    long long res2 = 0;
    while(!q.empty()) {
        auto [i, j] = q.front();
        q.pop();
        int path = dp[{i, j}];
        
        for(auto dk : dir) {
            int ni = i + dk.first;
            int nj = j + dk.second;
            
            ni = (ni % n + n) %n;
            nj = (nj % n + n) % n;
            if(field[ni][nj] == '.' && !dp.contains({i + dk.first, j + dk.second}) && max_brute_force_steps >= path + 1) {
                dp[{i + dk.first, j + dk.second}] = path + 1;
                q.push({i + dk.first, j + dk.second});
            }
        }
        // calculate
        {
            int i_dir = modulesBy1(i - start_pos);
            int j_dir = modulesBy1(j - start_pos);
            bool wasProccessed = visible.contains({i, j});
            if(wasProccessed) {
                continue;
            }

            for(int k1 = 0;k1 < 4;++k1)
                for(int k2 = 0;k2 < 4;++k2) {
                    visible.insert({  i + n * i_dir * k1, j + n * j_dir * k2 });
                }
            
            if(i_dir != 0 && j_dir != 0) {
                for(int b = 0;steps - n * b - path >= 0;++b) {
                    int a = (steps - n * b - path) / n;
                    if((path + n * b) % 2 == 0) {
                        res2 += a / 2 + a % 2;
                    } else {
                        res2 += a / 2 + 1;
                    }
                }
            }
        }
    }
    
    return res2 + steps  / 2 * 4 + 4;
}

int main(int argc, const char * argv[]) {
    ifstream in("input.txt");
    
    string str;
    
    long long sum = 0;
    vector<string> field;
    while(getline(in, str)) {
        field.push_back(str);
    }
    
    debug() << field;
    
    int n = 26501365;
    
    sum = smart(field, n);
    debug() << imie(sum) ;//imie(smart(field, 11)) imie(smart(field, 51)) imie(smart(field, 101));
   
    
    debug() << imie((sum));
    return 0;
}
