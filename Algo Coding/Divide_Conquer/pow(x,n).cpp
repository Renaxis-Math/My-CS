using ll = long long;

double solve_recursive(double x, int n) {
    /*
    For int, the range is asymmetric:
    - minimum: -2147483648
    - maximum: 2147483647
    So when n == INT_MIN, -n would be 2147483648, which over-range int
    => Use long long
    */
    ll N = n;
    if (N < 0) { x = 1.0 / x; N = -N; }

    unordered_map<int, double> memo;

    auto dfs = [&](auto&& dfs, long long n) -> double {
        if (n == 0) return 1.0;
        if (n == 1) return x;

        if (memo.find(n) != memo.end()) return memo[n];
        
        // if n odd -> n / 2 = (n-1) / 2
        double half_ans = dfs(dfs, n / 2);

        double ans = half_ans * half_ans;
        if (n % 2 != 0) ans *= x;

        memo[n] = ans;
        return ans;
    };

    return dfs(dfs, N);
}

double solve_optimal(double x, int n) {
    ll N = n;
    if (N < 0) { x = 1.0 / x; N = -N; }

    double ans = 1.0;
        
    while (N) {
        if (N % 2 != 0) ans *= x;
        x *= x;
        N >>= 1; /* N //= 2 */
    }

    return ans;
}

class Solution {
public:
    double myPow(double x, int n) {
        return solve_optimal(x, n);
    }
};