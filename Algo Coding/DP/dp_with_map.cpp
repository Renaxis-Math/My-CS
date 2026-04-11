int solve(vector<int>& nums) {
    if (nums.empty()) return 0;

    map<int, int> num_freq_map;
    for (int num : nums) num_freq_map[num]++;

    vector<int> answers(2, 0);
    int dp_i = 0;

    for (auto it = num_freq_map.rbegin(); it != num_freq_map.rend(); ++it) {
        int num = it->first, freq = it->second;

        int ans;

        if (it == num_freq_map.rbegin()) {
            ans = num * freq;
        } else {
            int lose_ans = answers[(dp_i - 1) % 2];

            int pick_ans = num * freq;
            if (prev(it)->first - num == 1) {
                if (dp_i >= 2) {
                    pick_ans += answers[(dp_i - 2) % 2];
                }
            } else {
                pick_ans += answers[(dp_i - 1) % 2];
            }

            ans = max(pick_ans, lose_ans);
        }

        answers[dp_i % 2] = ans;
        ++dp_i;
    }

    return answers[(dp_i - 1) % 2];
}