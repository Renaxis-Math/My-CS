/*
Simplify Path - LeetCode 71 (Medium)

Transform absolute Unix path to canonical form.
- '.' = current dir (ignore), '..' = parent (pop)
- '...' and '....' = valid names
- Consecutive '//' → single '/'
- Result: starts with '/', no trailing '/' except root

IDEA:
1. Remove '//' → '/'
2. Split by '/'
3. Stack: ignore '.', pop on '..', push valid names
*/

void _remove_doubleSlash(string& path) {
    size_t write_i = 0;
    for (size_t read_i = 0; read_i < path.size(); ++read_i) {
        if (path[read_i] == '/' && write_i > 0 && path[write_i - 1] == '/') continue;
        else path[write_i++] = path[read_i];
    }
    path.resize(write_i);
}

vector<string> _split(string& path, char delim = '/') {
    vector<string> answers;

    size_t start_i = 0;
    for (size_t past_end_i = 0; past_end_i < path.size() + 1; ++past_end_i) {
        if (past_end_i == path.size() || path[past_end_i] == delim) {
            answers.push_back(path.substr(start_i, past_end_i - start_i));
            start_i = past_end_i + 1;
        }
    }

    return answers;
}

string _join(vector<string>& stack, string& ans, char delim = '/') {
    for (int i = 0; i < stack.size(); ++i) ans += (i) ? (delim + stack[i]) : stack[i];
    return ans;
}

string solve(string& path) {
    _remove_doubleSlash(path);
    string ans;

    
    // check ending '/' (path starts with "/" -- must stay)
    if (path.size() > 1 && path.back() == '/') path.pop_back();

    // split by '/'
    vector<string> strings = _split(path);
    vector<string> stack; stack.reserve(strings.size());
    for (string& str: strings) {
        if (str == "..") {
            if (!stack.empty()) stack.pop_back();
        } else if (str != ".") {
            stack.push_back(str);
        }
    }

    _join(stack, ans);

    // check if ans starts with '/'
    if (!ans.starts_with("/")) ans = "/" + ans;
    return ans;
}