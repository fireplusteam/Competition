#ifndef convex_hull_dp_h
#define convex_hull_dp_h

#include <stdio.h>
#include <algorithm>
#include <cassert>
#include <complex>
#include <fstream>
#include <functional>
#include <iostream>
#include <map>
#include <numbers>
#include <queue>
#include <set>
#include <sstream>

using namespace std;

typedef int ftype;

#define inf 1e100

/// @brief  add lines of form m * x + b,
/// query returns min by default value at x, but can be configured at Constructing of object
struct chtDynamicMin {
private:
    struct line {
        ftype m, b;
        long double x;
        ftype om, ob;
        ftype val;
        bool isQuery;
        int id;
        line(ftype _m = 0, ftype _b = 0, ftype _om = 0, ftype _ob = 0, int _id = 0) {
            m       = _m;
            b       = _b;
            om      = _om;
            ob      = _ob;
            val     = 0;
            x       = -inf;
            id      = _id;
            isQuery = false;
        }

        ftype eval(ftype _x) const {
            return m * _x + b;
        }
        bool parallel(const line &l) const {
            return m == l.m;
        }
        long double intersect(const line &l) const {
            return parallel(l) ? inf : 1.0 * (l.b - b) / (m - l.m);
        }
        bool operator<(const line &l) const {
            if (l.isQuery)
                return x < l.val;
            else
                return m < l.m;
        }
    };

    set<line> hull;
    bool isMinimum;
    typedef set<line>::iterator iter;

    bool cPrev(iter it) {
        return it != hull.begin();
    }
    bool cNext(iter it) {
        return it != hull.end() && next(it) != hull.end();
    }

    bool bad(const line &l1, const line &l2, const line &l3) {
        return l1.intersect(l3) <= l1.intersect(l2);
    }
    bool bad(iter it) {
        return cPrev(it) && cNext(it) && bad(*prev(it), *it, *next(it));
    }

    iter update(iter it) {
        if (!cPrev(it))
            return it;
        long double x = it->intersect(*prev(it));
        line tmp(*it);
        tmp.x = x;
        it    = hull.erase(it);
        return hull.insert(it, tmp);
    }

public:
    chtDynamicMin(bool _isMinimum = true)
        : isMinimum(_isMinimum) {
    }

    void addLine(ftype m, ftype b, int id) {
        ftype om = m, ob = b;
        if (isMinimum) {
            m *= -1;
            b *= -1;
        }
        line l(m, b, om, ob, id);
        iter it = hull.lower_bound(l);
        if (it != hull.end() && l.parallel(*it)) {
            if (it->b < b)
                it = hull.erase(it);
            else
                return;
        }

        it = hull.insert(it, l);
        if (bad(it))
            return (void)hull.erase(it);

        while (cPrev(it) && bad(prev(it)))
            hull.erase(prev(it));
        while (cNext(it) && bad(next(it)))
            hull.erase(next(it));

        it = update(it);
        if (cPrev(it))
            update(prev(it));
        if (cNext(it))
            update(next(it));
    }

    // return value, index of line with optimum result
    // return inf, -1, if not found
    pair<ftype, int> query(ftype x) const {
        if (hull.empty())
            return {isMinimum ? inf : -inf, -1};
        line q;
        q.val = x, q.isQuery = 1;
        iter it = --hull.lower_bound(q);
        return {isMinimum ? -it->eval(x) : it->eval(x), it->id};
    }
};

#endif