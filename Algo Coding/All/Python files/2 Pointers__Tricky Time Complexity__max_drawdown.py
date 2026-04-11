def maximum_drawdown(prices):
    # Time: O(len(prices))

    ans = 0

    max_price = float('-inf')
    for price in prices:
        if price > max_price:
            max_price = price

        drawdown = max_price - price
        if drawdown > ans:
            ans = drawdown

    return ans

# Example usage:
prices = [1, 9, 6, 7, 5, 8]
assert maximum_drawdown(prices) == 4