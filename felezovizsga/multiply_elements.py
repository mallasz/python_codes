# imports
from functools import reduce


def product_calculator(numbers):
    """
    calculates the product of a list of numbers
    :param numbers: list of numbers of which the function calculates the product
    :return: product
    """
    product = reduce((lambda x, y: x * y), numbers)
    return product


lst = [1, 2, 3, 4]

print(f'{lst} => {(" * ".join([str(i) for i in lst]))} = {product_calculator(lst)}')
