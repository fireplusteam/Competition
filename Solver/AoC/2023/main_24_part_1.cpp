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

bool findIntersection(
                                                long long x1,
                                                long long y1,
                                                long long z1,
                                                long long vx1,
                                                long long vy1,
                                                long long vz1,
                                                
                                                long long x2,
                                                long long y2, 
                                                long long z2,
                                                long long vx2,
                                                long long vy2,
                                                long long vz2
                                                ) {
    long long det = (vx1 * vy2 * vz2) + (vy1 * vz2 * vx2) + (vz1 * vx2 * vy2)
                       - (vz1 * vy2 * vx2) - (vx1 * vz2 * vy2) - (vy1 * vx2 * vz2);

    if (std::abs(det) == 0) {
        // Lines are parallel, no intersection
        return true;
    }
    return false;
    
    long double t1 = ((x2 - x1) * (vy2 * vz1 - vz2 * vy1) +
                       (y2 - y1) * (vz2 * vx1 - vx2 * vz1) +
                       (z2 - z1) * (vx2 * vy1 - vy2 * vx1)) / det;

    long double t2 = ((x2 - x1) * (vy1 * vz2 - vz1 * vy2) +
                       (y2 - y1) * (vz1 * vx2 - vx1 * vz2) +
                       (z2 - z1) * (vx1 * vy2 - vy1 * vx2)) / det;
    
    if (t1 < 0 || t2 < 0) {
        // Intersection is in the past (t < 0)
        //return {LLONG_MIN, LLONG_MIN};
    }
    debug() << imie(t1) imie(t2);

    long double x = x1 + vx1 * t1;
    long double y = y1 + vy1 * t1;

    //return {x, y};
    return false;
}

bool haveSameDirection(int v1x, int v1y, int v1z, int v2x, int v2y, int v2z) {
    // Check if the ratios of corresponding components are equal
    double ratioX = (double)v2x / v1x;
    double ratioY = (double)v2y / v1y;
    double ratioZ = (double)v2z / v1z;

    // Tolerance for floating-point comparisons
    double tolerance = 1e-9;

    return std::abs(ratioX - ratioY) < tolerance && std::abs(ratioX - ratioZ) < tolerance && std::abs(ratioY - ratioZ) < tolerance;
}

int main(int argc, const char * argv[]) {
    ifstream in("input.txt");
    
    string str;
    
    int64_t sum = 0;
    vector<M> lines;
    while(getline(in, str)) {
        auto p = splitByStrings(str, {",", " ", "@"});
        M line;
        line.x = atoll(p[0].c_str());
        line.y = atoll(p[1].c_str());
        line.z = atoll(p[2].c_str());
        line.vx = atoll(p[3].c_str());
        line.vy = atoll(p[4].c_str());
        line.vz = atoll(p[5].c_str());
        lines.push_back(line);
    }
    
    //long long low = 7, upper = 27;
    long double low = 200000000000000LL;
    long double upper = 400000000000000LL;
    debug() << imie(low) imie(upper);
    
    for(int  i = 0;i < lines.size();++i)
        for(int j = i + 1;j < lines.size();++j) {
            auto p = findIntersection(lines[i].x, lines[i].y, lines[i].z, lines[i].vx, lines[i].vy, lines[i].vz, lines[j].x, lines[j].y, lines[j].z, lines[j].vx, lines[j].vy, lines[j].vz);
            assert(p);
            
            bool haveSameDir = haveSameDirection(lines[i].vx, lines[i].vy, lines[i].vz, lines[j].vx, lines[j].vy, lines[j].vz);
            debug() << imie(haveSameDir) imie(i) imie(j);
            
            //if(low <= p.first && p.first <= upper && low <= p.second && p.second <= upper) {
            //    ++sum;
            //} else {
            //    debug() << "fuck";
            //}
        }
    
    // insert code here...
    debug() << imie((sum));
    
    return 0;
}
