//
//  InputParserHelper.h
//  Solver
//
//  Created by Ievgenii Mykhalevskyi on 26.12.2023.
//

#ifndef InputParserHelper_h
#define InputParserHelper_h

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

#endif /* InputParserHelper_h */
