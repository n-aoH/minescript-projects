#!python
"""
A drop-in replacement for the `random` module in python using the java module. 

import as:
`import random_pyj as random`

All docs are from the oracle website:
https://docs.oracle.com/javase/8/docs/api/java/util/Random.html

& python.org website for randint + Uniform:
https://docs.python.org/3/library/random.html

Ported by @No.

Feel free to contribute and add any functions you need and submit a pull request.


"""

_Random =  JavaClass("java.util.Random") # type: ignore

random = _Random()


def set_seed(seed: int):
    """
    Sets the seed of this random number generator using a single long seed.
    """
    random.setSeed(seed)


def gauss():
    """
    Returns: the next pseudorandom, Gaussian ("normally") distributed double value with mean 0.0 and standard deviation 1.0 from this random number generator's sequence
    """
    return random.nextGaussian()

def randint(a: int, b: int):
    """
    Return a random integer N such that a <= N <= b.
    """
    if a > b:
        raise Exception(" \n\n\n[random_pyj] : Maximum must be greater than mimumum! \n")
    
    return a + (random.nextInt((b - a) + 1))

def uniform(a: float, b: float):
    """
    Return a random floating-point number N such that a <= N <= b for a <= b and b <= N <= a for b < a.
    """

    if a > b:
        raise Exception(" \n\n\n[random_pyj] : Maximum must be greater than mimumum! \n")
    
    scale = b-a
    
    return a + (random.nextFloat() * scale)
