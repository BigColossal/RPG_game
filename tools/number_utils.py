import math

def round_to_3_leading_digits(n):
    if n == 0:
        return 0

    digits = int(math.log10(n)) + 1
    zeros = digits - 3

    factor = 10 ** zeros
    rounded = math.ceil(n / factor) * factor
    return rounded