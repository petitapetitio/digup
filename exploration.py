import parso

func = """
x = 0

def fibonacci(n: int, memo: dict[int, int] = None) -> int:
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    result = fibonacci(n - 1, memo) + fibonacci(n - 2, memo)
    memo[n] = result
    return result
"""

x = parso.parse(func)

print(x)
