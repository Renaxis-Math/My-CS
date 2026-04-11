"""
Time Complexity: n * log(log n)
log log n comes from n/2 + n/5 + n/7 + ...
"""

/* Make an array is_prime initially true for every number 2..n-1. 
Then for each i until sqrt(n) > i, mark all multiples of i as not prime.
multiples = i*i, i(i+1) = i*i + i, i(i+2) = i*i + i + i, ...
*/
int solve(int n) {
    if (n <= 2) return 0;

    vector<bool> is_primes(n, true);
    is_primes[0] = false; is_primes[1] = false;


    /*
    Why start from i * i? Example:
    For i = 5, you do not need to mark 10, 15, 20;
    They were already handled by 2 and 3. So start at 25.    
    */
    for (int i = 2; i * i < n; ++i) {
        for (int mult = i * i; mult < n; mult += i) {
            is_primes[mult] = false;
        }
    }

    int ans = 0;
    for (int num = 2; num < n; ++num) ans += int(is_primes[num]);
    return ans;
}