#!python

"""
A drop-in replacement for the `math` module in python using the java module. 

import as:
`import math_pyj as math`

All docs are from the oracle website:
https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Math.html

Ported by @No.

Feel free to contribute and add any functions you need and submit a pull request.


"""

_Math =  JavaClass("java.lang.Math") # type: ignore

## Constants

pi = _Math.PI

e = _Math.E

## misc

def signum(f: float) -> float:
    """
    eturns the signum function of the argument; zero if the argument is zero, 1.0 if the argument is greater than zero, -1.0 if the argument is less than zero.
    """
    return _Math.signum(f)



## Rounding

def ceil(x: float) -> float:
    """
    Returns the smallest (closest to negative infinity) double value that is greater than or equal to the argument and is equal to a mathematical integer.
    """
    return _Math.ceil(x)

def floor(x: float) -> float:
    """
    
    Returns the largest (closest to positive infinity) double value that is less than or equal to the argument and is equal to a mathematical integer.
    """
    return _Math.floor(x)


## Exponents



def sqrt(x: float) -> float:
    """
    Returns the correctly rounded positive square root of a double value.
    """
    return _Math.sqrt(x)

def cbrt(x: float) -> float:
    """
    Returns the cube root of a double value.
    """
    return _Math.cbrt(x)

def pow(a: float, b: float) -> float:
    """
    Returns the value of the first argument raised to the power of the second argument.
    """
    return _Math.pow(a, b)

def log(a: float) -> float:
    """
    Returns the natural logarithm (base e) of a double value.
    """
    return _Math.log(a)


def log10(a: float) -> float:
    """
    Returns the base 10 logarithm of a double value.
    """
    return _Math.log10(a)






## Trig

def hypot(x: float, y:float) -> float:
    """
    Returns sqrt(x^2 +y^2) without intermediate overflow or underflow.
    """
    return _Math.hypot(x, y)

# conversions

def degrees(x: float) -> float:
    """
    Converts an angle measured in radians to an approximately equivalent angle measured in degrees.
    """
    return _Math.toDegrees(x)

def radians(x: float) -> float:
    """
    Converts an angle measured in degrees to an approximately equivalent angle measured in radians.
    """
    return _Math.toRadians(x)


# sin

def sin(x: float) -> float:
    """
    Returns the trigonometric sine of an angle.
    
    """
    return _Math.sin(x)

def asin(x: float) -> float:
    """
    Returns the arc sine of a value; the returned angle is in the range -pi/2 through pi/2.
    """
    return _Math.asin(x)

def sinh(x: float) -> float:
    """
    Returns the hyperbolic sine of a double value.
    """
    return _Math.sinh(x)

#cos

def cos(x: float) -> float:
    """
    Returns the trigonometric cosine of an angle.
    """
    return _Math.cos(x)

def acos(x: float) -> float:
    """
    Returns the arc cosine of a value; the returned angle is in the range 0.0 through pi.
    """
    return _Math.acos(x)

def cosh(x: float) -> float:
    """
    Returns the hyperbolic cosine of a double value.
    """
    return _Math.cosh(x)

# tan

def tan(x: float) -> float:
    """
    Returns the trigonometric tangent of an angle.
    """
    return _Math.tan(x)

def atan(x: float) -> float:
    """
    Returns the arc tangent of a value; the returned angle is in the range -pi/2 through pi/2.
    """
    return _Math.atan(x)

def atan2(x: float,y: float) -> float:
    """
    Returns the angle theta from the conversion of rectangular coordinates (x, y) to polar coordinates (r, theta).
    """
    return _Math.atan2(x,y)

def tanh(x: float) -> float:
    """
    Returns the hyperbolic tangent of a double value.
    """
    return _Math.tanh(x)
