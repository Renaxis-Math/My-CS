#include<bits/stdc++.h>
using namespace std;

struct Block {
    int person_id;
    int start_day;
    int end_day;
};

using pii = pair<int, int>;

vector<pii> _union_intervals(vector<pii>& intervals);
map<int, int> _build_sweep_lines(vector<Block>& blocks);

// 1. Find all days where everyone is available
vector<vector<int>> solve(int people_count, vector<Block>& blocks) {

    // build sweep lines
    map<int, int> lines = _build_sweep_lines(blocks);

    vector<vector<int>> answers;
    if (lines.empty()) return answers;

    int cum_unavail_count = 0;

    for (auto iter = lines.begin(); iter != lines.end(); ++iter) {
        int segment_start = iter->first;
        
        cum_unavail_count += iter->second;

        auto next_iter = next(iter);
        int segment_end = (next_iter != lines.end()) ? 
            next_iter->first : segment_start - 1;

        // if a valid [start, end) segment
        if (segment_start < segment_end) {
            int available_count = people_count - cum_unavail_count;

            if (available_count == people_count) {
                answers.push_back({segment_start, segment_end - 1});
            }
        }
    }

    return answers;
}

map<int, int> _build_sweep_lines(vector<Block>& blocks) {
    unordered_map<int, vector<pii>> person_blocks_map;
    for (auto& block : blocks) {
        person_blocks_map[block.person_id].push_back(
            {block.start_day, block.end_day}
        );
    }
    
    // auto sort asc., by first 'int' aka start_day
    map<int, int> lines; // day -> delta unavailable people

    for (auto& [person_id, intervals] : person_blocks_map) {
        vector<pii> merged_blocks = _union_intervals(intervals);

        for (auto& [start, end] : merged_blocks) {
            lines[start]++;
            lines[end + 1]--;
        }
    }

    return lines;
}

vector<pii> _union_intervals(vector<pii>& intervals) {
    vector<pii> answers;
    if (intervals.empty()) return answers;

    sort(intervals.begin(), intervals.end());
    
    for (auto& interval : intervals) {
        if (answers.empty()) answers.push_back(interval);
        else {
            pii& last_interval = answers.back();

            if (last_interval.second >= interval.first) {
                // union
                last_interval.first = min(interval.first, last_interval.first);
                last_interval.second = max(interval.second, last_interval.second);
            }
            else answers.push_back(interval);
        }
    }

    return answers;
}

/* FOLLOW UPS Always put under helper functions */

// 2. find all the days where at least P people are available.
vector<vector<int>> solve2(int people_count, vector<Block>& blocks, int p) {

    // build sweep lines
    map<int, int> lines = _build_sweep_lines(blocks);

    vector<vector<int>> answers;
    if (lines.empty()) return answers;

    int cum_unavail_count = 0;

    for (auto iter = lines.begin(); iter != lines.end(); ++iter) {
        int segment_start = iter->first;
        
        cum_unavail_count += iter->second;

        auto next_iter = next(iter);
        int segment_end = (next_iter != lines.end()) ? 
            next_iter->first : segment_start - 1;

        // if a valid [start, end) segment
        if (segment_start < segment_end) {
            int available_count = people_count - cum_unavail_count;
            
            if (available_count >= p) {
                answers.push_back({segment_start, segment_end - 1});
            }
        }
    }

    return answers;
}

// 3. find all the periods where P people are available for atleast X consective days
vector<vector<int>> solve3(int people_count, vector<Block>& blocks, int p, int x) {
    vector<vector<int>> segments = solve2(people_count, blocks, p);
    
    vector<vector<int>> answers;
    for (auto& seg : segments) {
        int first_avail_day = seg[0], last_avail_day = seg[1];
        if (last_avail_day - first_avail_day + 1 >= x) {
            answers.push_back({first_avail_day, last_avail_day});
        }
    }

    return answers;
}