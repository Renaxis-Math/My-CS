/*
Maximum Total Damage With Spell Casting
LeetCode 3437 - Difficulty: Medium

A magician has various spells.

You are given an array 'power', 
where each element represents the damage of a spell. 
Multiple spells can have the same damage value.

It is a known fact that if a magician decides to cast a spell with a damage of 'power[i]', 
they cannot cast any spell with a damage of 'power[i] - 2', 'power[i] - 1', 'power[i] + 1', or 'power[i] + 2'.

Each spell can be cast only once.

Return the maximum possible total damage that a magician can cast.



Constraints:

• '1 <= power.length <= 10^5'

• '1 <= power[i] <= 10^9'
*/

#include<iostream>
#include<vector>
#include<algorithm>
#include<unordered_map>
using namespace std;

using ll = long long;

template<class Pred>
int binary_search(int start_i, int end_i, Pred in_right_region) {
    int left_i = start_i, right_i = end_i;

    while (left_i <= right_i) {
        int mid_i = left_i + (right_i - left_i) / 2;
        if (in_right_region(mid_i)) right_i = mid_i - 1;
        else left_i = mid_i + 1;
    }

    return right_i;
}

ll dp(vector<int>& unique_powers, unordered_map<int, ll>& unique_total_map) {
    int n = unique_powers.size();
    vector<ll> answers(n, 0);
    
    for (int i = 0; i < n; ++i) {
        int power = unique_powers[i];

        auto in_right_region = [&](int mid_i) {
            return !(unique_powers[mid_i] <= power - 3);
        };

        // Find rightmost value <= unique_powers[i] - 3 (safe to combine).
        int prev_i = binary_search(0, i - 1, in_right_region);

        ll pick_ans = unique_total_map.at(power) + (prev_i >= 0 ? answers[prev_i] : 0LL);
        ll lose_ans = (i > 0 ? answers[i - 1] : 0LL);
        answers[i] = max(pick_ans, lose_ans);
    }

    return answers[n - 1];
}

ll solve(vector<int>& powers) {

    // Build unique_total_map: unique power -> unique power * count
    unordered_map<int, ll> unique_total_map;
    for (auto power : powers) unique_total_map[power] += power;

    // Convert 'unique_total_map' to list[tuple]
    vector<int> unique_powers;
    unique_powers.reserve(unique_total_map.size());

    for (auto& kv : unique_total_map) unique_powers.push_back(kv.first);

    sort(unique_powers.begin(), unique_powers.end());
    return dp(unique_powers, unique_total_map);
}