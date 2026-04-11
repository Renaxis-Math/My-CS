"""
Climbing Stairs
LeetCode 70 - Difficulty: Easy

You are climbing a staircase. It takes 'n' steps to reach the top.

Each time you can either climb '1' or '2' steps. In how many distinct ways can you climb to the top?



Constraints:

• '1 <= n <= 45'
"""

"""
f(n)        = 1 * f(n - 1) + 1 * f(n - 2)
f(n - 1)    = 1 * f(n - 1) + 0 * f(n - 2)

=> [f(n) f(n-1)]    = [[1, 1], [1, 0]] * [f(n-1) f(n-2)]
                    = ...
                    = [[1, 1], [1, 0]]^{n-1} * [f(1) f(0)]
"""
def solve(n):

    def mat_mul(A, B):
        return [
            [
                A[0][0] * B[0][0] + A[0][1] * B[1][0],
                A[0][0] * B[0][1] + A[0][1] * B[1][1]
            ],
            [
                A[1][0] * B[0][0] + A[1][1] * B[1][0],
                A[1][0] * B[0][1] + A[1][1] * B[1][1]
            ]
        ]
    
    def mat_pow(matrix, power):
        answers = [[1, 0], [0, 1]]  # identity

        while power > 0:
            if power % 2 == 1: answers = mat_mul(answers, matrix)
            matrix = mat_mul(matrix, matrix)
            power >>= 1             # power //= 2

        return answers
    
    M = mat_pow([[1, 1], [1, 0]], n - 1)
    return M[0][0] * 1 + M[0][1] * 1    # [[1, 1], [1, 0]]^{n-1} * [f(1) f(0)]
