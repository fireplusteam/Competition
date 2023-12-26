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

enum Transform {
    None,
    Swap,
    Reverese
};

struct M {
    Transform transform = Transform::None;
    pair<int, int> d_in;
    pair<int, int> d_out;
    pair<int, int> in_fieldIndex;
    pair<int, int> out_fieldIndex;

    friend ostream& operator<<(ostream &o, const M& a) {
        debug(false) << "(" << imie(a.transform) imie(a.d_in) imie(a.d_out) imie(a.in_fieldIndex) imie(a.out_fieldIndex) << ")";
        return o;
    }

};

vector< vector<M>> mapper(7, vector<M>(7));

int squareCoef = 50;
//int squareCoef = 4;


M inverse(M b) {
    swap(b.in_fieldIndex, b.out_fieldIndex);
    swap(b.d_in, b.d_out);
    b.d_in.first *= -1;
    b.d_in.second *= -1;
    b.d_out.first *= -1;
    b.d_out.second *= -1;
    return b;
}

pair<pair<int, int>, pair<int,int>> getNextPos(pair<int, int> fieldIndex, pair<int, int> direction) {
    pair<int, int> squareInd { fieldIndex.first / squareCoef, fieldIndex.second / squareCoef }; 
    
    M trans;
    bool valid = false;
    int currentSquare = -1;
    int nextSquare = -1;
    bool is_inv = false;
    for (int i = 0;i <= 6;++i) {
        for(int j = 0;j <= 6;++j) {
            if(mapper[i][j].in_fieldIndex == squareInd && mapper[i][j].d_in == direction) {
                trans = mapper[i][j];
                currentSquare = i;
                nextSquare = j;
                valid = true;
                goto end;
            }
            auto inv = inverse(mapper[i][j]);
            if(inv.in_fieldIndex == squareInd && inv.d_in == direction) {
                currentSquare = j;
                nextSquare = i;
                trans = inv;
                valid = true;
                is_inv = true;
                goto end;
            }
        }
    }
    end:
    debug() << tabs(2) << "BEGIN:" << imie(currentSquare) imie(nextSquare) imie(trans) imie(squareInd) imie(fieldIndex) imie(direction);
    
    assert(valid);
    
    fieldIndex.first -= trans.in_fieldIndex.first * squareCoef;
    fieldIndex.second -= trans.in_fieldIndex.second * squareCoef;
    
    int  n = squareCoef - 1;
    int i = fieldIndex.first;
    int j = fieldIndex.second;
    if(currentSquare == 1 && nextSquare == 6) {
        fieldIndex.first = j;
        fieldIndex.second = 0;
    } else if(currentSquare == 6 && nextSquare == 1) {
        fieldIndex.first = 0;
        fieldIndex.second = i;
    } else if(currentSquare == 1 && nextSquare == 4) {
        fieldIndex.first = n - i;
        fieldIndex.second = 0;
    } else if(currentSquare == 4 && nextSquare == 1) {
        fieldIndex.first = n - i;
        fieldIndex.second = 0;
    } else if(currentSquare == 3 && nextSquare == 4) {
        fieldIndex.first = 0;
        fieldIndex.second = i;
    } else if(currentSquare == 4 && nextSquare == 3) {
        fieldIndex.first = j;
        fieldIndex.second = 0;
    } else if(currentSquare == 6 && nextSquare == 5) {
        fieldIndex.first = n;
        fieldIndex.second = i;
    } else if(currentSquare == 5 && nextSquare == 6) {
        fieldIndex.first = j;
        fieldIndex.second = n;
    } else if(currentSquare == 3 && nextSquare == 2) {
        fieldIndex.first = n;
        fieldIndex.second = i;
    } else if(currentSquare == 2 && nextSquare == 3) {
        fieldIndex.first = j;
        fieldIndex.second = n;
    } else if(currentSquare == 5 && nextSquare == 2) {
        fieldIndex.first = n - i;
        fieldIndex.second = n;
    } else if(currentSquare == 2 && nextSquare == 5) {
        fieldIndex.first = n - i;
        fieldIndex.second = n;
    } else if(currentSquare == 6 && nextSquare == 2) {
        fieldIndex.first = 0;
        fieldIndex.second = j;
    } else if(currentSquare == 2 && nextSquare == 6) {
        fieldIndex.first = n;
        fieldIndex.second = j;
    } else {
        assert(false);
    }

    /*if(currentSquare == 2 && nextSquare == 6) {
        fieldIndex.first = 0;
        fieldIndex.second = n - i;
    } else if(currentSquare == 5 && nextSquare == 4) {
        fieldIndex.first = n;
        fieldIndex.second = n - j;
    } else if(currentSquare == 3 && nextSquare == 1) {
        fieldIndex.first = j;
        fieldIndex.second = 0;
    } else {
        assert(false);
    }*/

    fieldIndex.first += trans.out_fieldIndex.first * squareCoef;
    fieldIndex.second += trans.out_fieldIndex.second * squareCoef;
    
    direction = trans.d_out;
    
    squareInd = { fieldIndex.first / squareCoef, fieldIndex.second / squareCoef };
    debug() << tabs(4) << "TRANSFORMED:" imie(fieldIndex) imie(direction) imie(squareInd);
    
    return {fieldIndex, direction};
}

int main(int argc, const char * argv[]) {
    ifstream in("input.txt");
    
    string str;
    
    int64_t sum = 0;
    
    vector<string> field;
    int m = 0;
    while(getline(in, str)) {
        if(str == "") break;
        str = " " + str + " ";
        field.push_back(str);
        m = max(m, (int)field.size());
    }
    
    field.insert(field.begin(), string(m, ' '));
    field.push_back(string(m, ' '));
    
    for(int i = 0;i < field.size();++i){
        while(field[i].size() < m) field[i] += ' ';
    }
    
    for(int i = 0;i < field.size();++i) {
        cout << field[i] << endl ;
    }
    
    string path;
    in >> path;

    debug() << path;

    mapper[1][6] = {Transform::Swap, {-1, 0}, {0, 1}, { 0, 1 }, {3, 0}};
    mapper[1][4] = {Transform::Reverese, {0, -1}, {0, 1}, {0, 1}, {2, 0}};
    mapper[3][4] = {Transform::Swap, {0, -1}, {1, 0}, {1, 1}, {2, 0}};
    mapper[6][5] = {Transform::Swap, {0, 1}, {-1, 0}, {3, 0}, {2, 1}};
    mapper[3][2] = {Transform::Swap, {0, 1}, {-1, 0}, {1, 1}, {0, 2}};
    mapper[5][2] = {Transform::Reverese, {0, 1}, {0, -1}, {2, 1}, {0, 2}};
    mapper[6][2] = {Transform::None, {1, 0}, {1, 0}, {3, 0}, {0, 2}};
    
    /*mapper[2][6] = {Transform::Swap, {0, 1}, {1, 0}, { 1, 2 }, {2, 3}};
    mapper[5][4] = {Transform::Reverese, {1, 0}, {-1, 0}, { 2, 2 }, {1, 0}};
    mapper[3][1] = {Transform::Swap, {-1, 0}, {0, 1}, { 1, 1 }, {0, 2}};
    */
        
    pair<int, int> trip {0, squareCoef};
    //pair<int, int> trip {0, squareCoef * 2};
    
    int direction_i = 0;
    path += " ";
    
    int step_count = 0;

    for(int i = 0;i < path.size();++i) {
        pair<int,int> d[] = {{0, 1}, {1, 0}, {0, -1} , {-1, 0}};
        if(isdigit(path[i])) {
            step_count = step_count * 10 + dig(path[i]);
        } else {
            for(int step = 0; step < step_count;++step) {
                pair<int, int> next_step = { trip.first + d[direction_i].first, trip.second + d[direction_i].second };
                if(field[next_step.first + 1][next_step.second + 1] == ' ') {
                    auto p = getNextPos(trip, d[direction_i]);
                    next_step = p.first;
                    if(field[next_step.first + 1][next_step.second + 1] != '#') {
                        bool ok = false;
                        for(int d_i = 0;d_i < 4;++d_i) {
                            if(d[d_i] == p.second) {
                                direction_i = d_i;
                                ok = true;
                                break;
                            }
                        }
                        assert(ok);
                    }
                }

                if(field[next_step.first + 1][next_step.second + 1] == '#') {
                    break;
                }
                assert(field[next_step.first + 1][next_step.second + 1] == '.');
                trip = next_step;
            }
            
            if(path[i] == 'R') {
                direction_i++;
            } else if(path[i] == 'L') {
                direction_i--;
            }
            direction_i = (direction_i + 4) % 4;
            
            debug() << imie(step_count) imie(trip);
            step_count = 0;
        }
        
    }

    debug() << imie(trip) imie(direction_i);
    
    sum = (trip.first + 1) * 1000 + (trip.second + 1) * 4 + direction_i;
    
    // insert code here...
    debug() << imie((sum));
    
    return 0;
}
