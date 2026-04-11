bool solve(string& s, string& p) {
    vector<vector<int>> answers(s.size() + 1, vector<int>(p.size() + 1));

    for (int s_i = s.size(); s_i >= 0; s_i--) {
        for (int p_i = p.size(); p_i >= 0; p_i--) {
            bool ans;

            if (p_i == p.size() && s_i == s.size()) ans = true;
            else if (s_i == s.size()) {
                ans = (
                    p_i+1 < p.size() && 
                    p[p_i+1] == '*' && answers[s_i][p_i+2]
                ); // x* skips as empty
            }
            else if (p_i == p.size()) ans = false;
            else {

                bool charMatch = s[s_i] == p[p_i] || p[p_i] == '.';

                if (charMatch) {
                    ans = answers[s_i+1][p_i+1];
                    if (p_i+1 < p.size() && p[p_i+1] == '*') {
                        ans |= (answers[s_i][p_i+2] || answers[s_i+1][p_i]);
                    }
                }
                else {
                    ans = false;
                    if (p_i+1 < p.size() && p[p_i+1] == '*') {
                        ans |= answers[s_i][p_i+2];
                    }                    
                }
            }

            answers[s_i][p_i] = ans;
        }
    }
    return answers[0][0];
}

bool solve_optimized(string& s, string& p) {
    vector<vector<int>> answers(2, vector<int>(p.size() + 1));

    for (int s_i = s.size(); s_i >= 0; --s_i) {
        for (int p_i = p.size(); p_i >= 0; --p_i) {
            bool ans;

            if (p_i == p.size() && s_i == s.size()) ans = true;
            else if (s_i == s.size()) {
                ans = (
                    p_i+1 < p.size() && p[p_i+1] == '*' && answers[s_i % 2][p_i+2]
                ); // x* skips as empty
            }
            else if (p_i == p.size()) ans = false;
            else {

                bool charMatch = s[s_i] == p[p_i] || p[p_i] == '.';

                if (charMatch) {
                    ans = answers[(s_i+1) % 2][p_i+1];
                    if (p_i+1 < p.size() && p[p_i+1] == '*') {
                        ans |= (answers[s_i % 2][p_i+2] || answers[(s_i+1) % 2][p_i]);
                    }
                }
                else {
                    ans = false;
                    if (p_i+1 < p.size() && p[p_i+1] == '*') {
                        ans |= answers[s_i % 2][p_i+2];
                    }                    
                }
            }

            answers[s_i % 2][p_i] = ans;
        }
    }
    
    return answers[0 % 2][0];
}