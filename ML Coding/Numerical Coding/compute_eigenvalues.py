"""
Calculate Eigenvalues of a Matrix (medium)
Write a Python function that calculates the eigenvalues of a 2x2 matrix. The function should return a list containing the eigenvalues, sort values from highest to lowest.
Example
Example:
        input: matrix = [[2, 1], [1, 2]]
        output: [3.0, 1.0]
        reasoning: The eigenvalues of the matrix are calculated using the characteristic equation of the matrix, which for a 2x2 matrix is $\lambda^2 - 	ext{trace}(A)\lambda + 	ext{det}(A) = 0$, where $\lambda$ are the eigenvalues.
"""

def calculate_eigenvalues(matrix: list[list[float]]) -> list[float]:
    a, b, c, d = matrix[0][0], matrix[0][1], matrix[1][0], matrix[1][1]
    trace = a + d
    determinant = a * d - b * c
    # Calculate the discriminant of the quadratic equation
    discriminant = trace**2 - 4 * determinant
    # Solve for eigenvalues
    lambda_1 = (trace + discriminant**0.5) / 2
    lambda_2 = (trace - discriminant**0.5) / 2
    return [lambda_1, lambda_2]