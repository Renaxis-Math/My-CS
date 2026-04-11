"""
Perfect Squares
LeetCode 279 - Difficulty: Medium

Given an integer 'n', return the least number of perfect square numbers that sum to 'n'.

A perfect square is an integer that is the square of an integer; in other words, it is the product of some integer with itself. For example, '1', '4', '9', and '16' are perfect squares while '3' and '11' are not.



Constraints:

• '1 <= n <= 10^4'
"""

int solve_dp(int n) {

    vector<int> answers(n + 1, n);

    for (size_t num = 0; num < answers.size(); ++num) {
        size_t dp_num = num;

        int ans = answers[dp_num];

        if (dp_num == 0) ans = 0;
        else {
            size_t prev_num = 1;
            while (prev_num * prev_num <= num) {
                ans = min(ans, answers[num - prev_num * prev_num] + 1);
                prev_num++;
            }
        }
        
        answers[dp_num] = ans;
    }

    return answers[n];
}

int solve_number_theory(int n) {

    auto is_square = [&](int num){
        int temp = (int) sqrt(num);
        return temp * temp == num;
    };

    auto is_mod_equal_to = [&](size_t target_remainder, int mod) {
        return ((n % mod) + mod) % mod == target_remainder;
    };

    // Remove factors of 4
    while (is_mod_equal_to(0, 4)) n /= 4; // or n >>= 2;

    // Check Legendre condition
    if (is_mod_equal_to(7, 8)) return 4;

    // Check if perfect square
    if (is_square(n)) return 1;

    // Check if sum of two squares
    int sqrt_n = (int) sqrt(n);
    for (int i = 1; i <= sqrt_n; i++){
        if (is_square(n - i*i)) return 2;
    }

    // Otherwise answer is 3
    return 3;
}