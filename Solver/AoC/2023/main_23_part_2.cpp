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
#include <random>

#ifndef LOCAL
class debug {public: debug(bool isend = true){} template<class c> debug& operator<<(const c&) { return *this; }};
#define imie(...) ""
#define endl "\n"
#endif

using namespace std;

struct M {
    int i, j;
    int cost;
    
    /*friend bool operator<(const M&a, const M& b) {
        if(a.z1 != b.z1) return a.z1 < b.z1;
        return a.z2 < b.z2;
    }*/
    
    friend ostream& operator<<(ostream &o, const M& a) {
        debug(false) << "(" << imie(a.i) imie(a.j) imie(a.cost) << ")";
        return o;
    }
};
int n;
int m;

vector<pair<int,int>> dir = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};
vector<char> slopes = {'>', '<', 'v', '^'};
vector<string> field;
set<pair<int, int>> vis;
map<pair<int, int>, int> minPath;
int res = 0;

map<pair<int,int>, map<pair<int,int>, int> > graph;
set<tuple<int,int, int, int>> intersection;

bool isCoreVertex(int i, int j) {
    if( i < 0 || i >= n || j < 0 || j >= m)
        return false;
    if(i == 0 && j == 1)
        return true;
    if(i == n - 1 && j == m - 2)
        return true;
    int c = 0;
    int c2 = 0;
    if(field[i][j] != '#')
        for(auto& d: dir) {
            int n_i = i + d.first;
            int n_j = j + d.second;
            if( n_i < 0 || n_i >= n || n_j < 0 || n_j >= m)
                continue;
            c += field[n_i][n_j] != '#';
            c2 += field[n_i][n_j] != '.';
        }
    if(c >= 3){
        assert(c2 == 4);

        return true;
    }
    return false;
}

bool isIntersected(vector<int>& path) {
    if((int)path.size() - 3 < 1) {
        return false;
    }
    int b1 = path[path.size() - 1];
    int b2 = path[path.size() - 2];
    for(int i = path.size() - 3;i >= 1;i--) {
        int c1 = path[i];
        int c2 = path[i - 1];
        if(intersection.contains({b1, b2, c1, c2}))
            return true;
    }
    return false;
}

int dfs(int i, int j, vector<int>& path) {
    if(i == n - 1 && j == m - 2) {
        //debug() << imie(res);
        return 0;
    }
    if(vis.contains({i, j}))
        return INT_MIN;
    vis.insert({i,j});
   
    int r = INT_MIN;
    for(auto& val : graph[{i, j}]) {
        path.push_back({val.first.first * m + val.first.second});
        if(!isIntersected(path)) {
            r = max(r, dfs(val.first.first, val.first.second, path) + val.second);
        }
        path.pop_back();
    }
    
    vis.erase({i, j});
    return r;
}

vector<vector<int>> maskInd;

map<tuple<int,int, int, int>, set<int>> intersectionMap;

int startI, startJ;

map<pair<int,int>, int> dd(int i, int j, int pi, int pj, int len, set<int> path) {
    if(!(i >= 0 && i < n && j >= 0 && j < m))
        return {};
    
    if(field[i][j] == '#')
        return {};
    
    map<pair<int,int>, int> res;
    for(auto d: dir) {
        int next_i = i + d.first;
        int next_j = j + d.second;
        
        if(!(next_i == pi && next_j == pj)) {
            if(isCoreVertex(next_i, next_j)) {
                path.insert({next_i * m + next_j});
                
                res[{next_i, next_j}] = {len + 1};
                
                intersectionMap[{startI, startJ, next_i, next_j}] = path;
                
                path.erase({next_i * m + next_j});
            } else {
                path.insert({next_i * m + next_j});
                auto r = dd(next_i, next_j, i, j, len + 1, path);
                for(auto v: r)
                    res.insert(v);
                path.erase({next_i * m + next_j});
            }
        }
    }
    return res;
}

int main(int argc, const char * argv[]) {
    ifstream in("input.txt");
    
    string str;
    
    int64_t sum = 0;
    
    while(getline(in, str)) {
        field.push_back(str);
    }
    
    n = field.size();
    m = field[0].size();
    debug() << imie(n) imie(m);
    
    maskInd = vector<vector<int>>(n, vector<int>(m, -1));
    int mIndex = 0;
    
    for(int i = 0;i < n;++i)
        for(int j = 0;j < m;++j)
        {
            if(isCoreVertex(i, j)) {
                maskInd[i][j] = mIndex;
                ++mIndex;
                startI = i;
                startJ = j;
                graph[{i, j}] = dd(i, j, i, j, 0, {i * m + j});
            }
        }

    for(auto [u_key, u_path]: intersectionMap) {
        for(auto [v_key, v_path]: intersectionMap) {
            if(u_key == v_key)
                continue;
            
            std::set<int> intersectionSet;

                // Use std::set_intersection to find the intersection
            set_intersection(
                    u_path.begin(), u_path.end(),
                    v_path.begin(), v_path.end(),
                    inserter(intersectionSet, intersectionSet.begin())
            );
            if(intersectionSet.size() > 0) {
                auto [i, j, i1, j1] = u_key;
                auto [_i, _j, _i1, _j1] = v_key;
                intersection.insert({i * m + j, i1*m + j1, _i * m + _j, _i1 * m + _j1});
            }
        }
    }
    
    debug() << imie(intersection);
    
    debug() << imie(graph);
    debug() << imie(graph.size());
    vector<int> path { 0 * m + 1 };
    debug() << imie(dfs(0, 1, path));
    
    // insert code here...
    debug() << imie((sum));
    
    return 0;
}
