//
//  Ext_Templates.h
//  Solver
//
//  Created by Ievgenii Mykhalevskyi on 01.01.2024.
//

#ifndef Ext_Templates_h
#define Ext_Templates_h

// ORDERED DATA STRUCTURES
#include <ext/pb_ds/assoc_container.hpp>
#include <ext/pb_ds/detail/standard_policies.hpp>
#include <ext/pb_ds/tree_policy.hpp>
using namespace __gnu_pbds;
template <typename K, typename V, typename Comp = std::less<K>>
using ordered_map = tree<K, V, Comp, rb_tree_tag, tree_order_statistics_node_update>;
template <typename K, typename Comp = std::less<K>>
using ordered_set = ordered_map<K, null_type, Comp>;

//  RANDOM
std::random_device rd;
std::mt19937 g(rd());

#endif /* Ext_Templates_h */
