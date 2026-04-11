/*
Problem Statement

Given an array of meeting time interval objects consisting of start and end times 
[[start_1,end_1],[start_2,end_2],...] (start_i < end_i), 
find the minimum number of rooms required to schedule all meetings without any conflicts.
*/

/**
 * Definition of Interval:
 * class Interval {
 * public:
 *     int start, end;
 *     Interval(int start, int end) {
 *         this->start = start;
 *         this->end = end;
 *     }
 * }
 */

 using pii = pair<int, int>;

 vector<pii> get_line_search_interval(vector<Interval>& intervals) {
     vector<pii> answers; answers.reserve(2 * intervals.size());
 
     for (auto& interval : intervals) {
         answers.push_back({interval.start, 1});
         answers.push_back({interval.end, -1});
     }
 
     sort(
         answers.begin(), answers.end(), 
         [](pii& a, pii& b) { 
             // end before start
             if (a.first == b.first) return a.second < b.second;
             return a.first < b.first; // sort asc time
         }
     );
     return answers;
 }
 
 class Solution {
 public:
     int minMeetingRooms(vector<Interval>& intervals) {
         vector<pii> line_search_intervals = get_line_search_interval(intervals);
         int ans = 0;
 
         int max_needed_room = 0;
         for (auto& interval : line_search_intervals) {
             max_needed_room += interval.second;
             ans = max(ans, max_needed_room);
         }
         return ans;
     }
 };
 