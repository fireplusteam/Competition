//
//  LogHelper.h
//  Solver
//
//  Created by Ievgenii Mykhalevskyi on 11.12.2023.
//

#ifndef LogHelper_h
#define LogHelper_h

#include <iostream>
#include <vector>
#include <sstream>
#include <tuple>
#include <optional>

using namespace std;

template<class T, size_t n> vector<T> arr(const T (&a)[n]) {
    vector<T> r(a, a + n); return r;
}
template<class T, size_t n, size_t m> vector<vector<T>> arr(const T (&a)[n][m]) {
    vector<vector<T>> r(n); 
    for(int i = 0;i < n; ++i)
        r[i] = arr(a[i]);
    return r;
}
template<class T, size_t n, size_t m, size_t k> vector<vector<vector<T>>> arr(const T (&a)[n][m][k]) {
    vector<vector<vector<T>>> r(n); 
    for(int i = 0;i < n; ++i) {
        r[i] = arr(a[i]);
    }
    return r;
}
template<class T, size_t n, size_t m, size_t k, size_t t> vector<vector<vector<vector<T>>>> arr(const T (&a)[n][m][k][t]) {
    vector<vector<vector<vector<T>>>> r(n); 
    for(int i = 0;i < n; ++i) {
        r[i] = arr(a[i]);
    }
    return r;
}
template < class c > struct rge { c b, e; };
template < class c > rge<c> range(c i, c j) { return rge<c>{i, j}; }
template < class c > auto dud(c* x) -> decltype(cerr << *x, 0);
template < class c > char dud(...);
struct debug {
    bool isend; 
    debug(bool _isend = true) {
        this->isend = _isend;
    }

    ~debug() { 
        if(isend)
            cerr << endl;
    }
    template < class c > 
    typename enable_if<sizeof dud<c>(0) != 1, debug&>::type operator<<(c i) {
        cerr << boolalpha << i;
        return * this;
    }
    template < class c >
    typename enable_if<sizeof dud<c>(0) == 1, debug&>::type operator<<(c i) {
        return * this << range(begin(i), end(i));
    }
    
    template < class c, class b, class f, class a > debug & operator <<(tuple < b, c, f, a > d) {
        return * this << "(" << get<0>(d) << ", " << get<1>(d) << ", " << get<2>(d) << ", " << get<3>(d) << ")";
    }
    
    template < class c, class b, class f > debug & operator <<(tuple < b, c, f > d) {
        return * this << "(" << get<0>(d) << ", " << get<1>(d) << ", " << get<2>(d) << ")";
    }
    
    template < class c, class b > debug & operator <<(tuple < b, c > d) {
        return * this << "(" << get<0>(d) << ", " << get<1>(d) << ")";
    }
    
    template < class c> debug & operator <<(tuple < c > d) {
        return * this << "(" << get<0>(d) << ")";
    }
 
    template < class c, class b > debug & operator <<(pair < b, c > d) {
        return * this << "(" << d.first << ", " << d.second << ")";
    }
    
    debug & operator <<( const string &a) {
        if (a.size() > 0 && (isspace(a[0]) || isspace(a.back()))) {
            cerr << "\"" << a.c_str() << "\"";
            return * this;
        } else {
            cerr << a.c_str();
            return * this;
        }
    }
    
    template < class c > debug & operator <<(rge<c> d) {
        *this << "[";
        for (auto it = d.b; it != d.e; ++it)
            if(it == d.b) {
                *this << *it;
            } else {
                *this << ", " << *it;
            }
        return * this << "]";
    }
    
    template< class c > debug & operator<<( const optional< c >& d) {
        *this << "optional(";
        if(d.has_value()) {
            *this << d.value();
        } else {
            *this << "null";
        }
        return *this << ")";
    }
};

#define imie(...) " [" << #__VA_ARGS__ ": " << (__VA_ARGS__) << "] "
#define endl "\n"

template<typename T, size_t n, typename std::enable_if<!std::is_same<T, char>::value, int>::type = 0>
debug& operator<<(const debug d, const T (&a)[n]) {
    return debug(false) << arr(a);
}
template<class T, size_t n, size_t m> debug& 
operator<<(const debug d, const T (&a)[n][m]) {
    return debug(false) << arr(a);
}
template<class T, size_t n, size_t m, size_t k> 
debug& operator<<(const debug d, const T (&a)[n][m][k]) {
    return debug(false) << arr(a);
}
template<class T, size_t n, size_t m, size_t k, size_t t>
debug& operator<<(const debug d, const T (&a)[n][m][k][t]) {
    return debug(false) << arr(a);
}
string tabs(int n) { 
    return string((size_t)n, ' ') + string((size_t)n, ' ');
}

#endif /* LogHelper_h */
