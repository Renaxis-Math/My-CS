"""
KL Divergence Between Two Normal Distributions
Task: Implement KL Divergence Between Two Normal Distributions
Your task is to compute the Kullback-Leibler (KL) divergence between two normal distributions. KL divergence measures how one probability distribution differs from a second, reference probability distribution.

Write a function kl_divergence_normal(mu_p, sigma_p, mu_q, sigma_q) that calculates the KL divergence between two normal distributions, where 
 and 
.

The function should return the KL divergence as a floating-point number.

Example
Example:
import numpy as np

mu_p = 0.0
sigma_p = 1.0
mu_q = 1.0
sigma_q = 1.0

print(kl_divergence_normal(mu_p, sigma_p, mu_q, sigma_q))

# Expected Output:
# 0.5
"""

import numpy as np

def kl_divergence_normal(mu_p, sigma_p, mu_q, sigma_q):
    term1 = np.log(sigma_q / sigma_p)
    term2 = (sigma_p ** 2 + (mu_p - mu_q) ** 2) / (2 * sigma_q ** 2)
    kl_div = term1 + term2 - 0.5
    return kl_div
