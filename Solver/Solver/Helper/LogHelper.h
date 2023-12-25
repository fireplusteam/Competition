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
#include <set>
#include <sstream>
#include <tuple>

using namespace std;

#define LOCAL

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
    debug(bool isend = true) {
        this->isend = isend;
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

//---INPUT-FOUNDATION-----------------------------------------------
vector<string> splitByStrings(const string& input, set<string> delimiter) {
    vector<string> tokens; string token;
    for(size_t pos = 0;pos < input.size();++pos) {
        bool contains = false;
        for(auto del : delimiter) {
            if (input.substr(pos, del.size()) == del) {
                if(!token.empty()) tokens.emplace_back(token);
                token = "";contains = true;pos += del.size() - 1; break;
            }
        }
        if(!contains) token += input[pos];
    }
    if(!token.empty()) tokens.emplace_back(token);
    return tokens;
}
vector<string> splitByChars(const string& input, set<char> delimiter) {
    set<string> sDel; 
    for(auto del : delimiter) {
        sDel.insert(string(1, del));
    }
    return splitByStrings(input, sDel);
}
vector<string> splitByChar(const string& input, char delimiter) {
    return splitByChars(input, set<char> { delimiter });
}
int dig(char s) { 
    return s - '0';
}
template<class T>
vector<T> read(const string &str) {
    istringstream in(str);
    vector<T> r;
    T val;
    while(in >> val) {
        r.emplace_back(val);
    }
    return r;
}
//----END-FOUNDATION-----------------------------------------------------------


#endif /* LogHelper_h */
