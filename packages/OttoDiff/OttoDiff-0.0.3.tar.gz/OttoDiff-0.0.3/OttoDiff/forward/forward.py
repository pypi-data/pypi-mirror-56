import numpy as np

class Variable:
    def __init__(self, val, der=1):
        '''
        val: int/float, (or np.array in the future if multiple input allowed)
            values of variables for differentiation
        der: int/float or np.array if mutiple variable
             (it is just a scalar for this milestone),
             partial derivatives of variables for differentiation
             each entry represents an partial derivatives (∂u/∂x, ∂u/∂y, ∂u/∂z, ...)
        '''
        self.val = val
        self.der = der

    def __add__(self, other):
        """Returns self + other.

            INPUTS
            =======
            self: Variable object
            other: Variable or float/int

            RETURNS
            ========
            a new Variable represents self + other
            new val = self.val + other.val
            new der = self.der + other.der
            (Error exception is raised when the input is not valid)

            EXAMPLES
            =========
            >>> x = Variable(2)
            >>> y = x + 1
            Variable(3, 1)
        """
        if isinstance(other, (int, float)):
            # other is a number
            return Variable(self.val + other, self.der)
        # assume other is a valid Variable, otherwise raise Error
        try:
            return Variable(self.val + other.val, self.der + other.der)
        except:
            # other error: derivatives dimensions does not match
            raise TypeError("other is not a valid Variable or number.")

    def __radd__(self, other):
        """Returns other + self.

            INPUTS
            =======
            self: Variable object
            other: Variable or float/int

            RETURNS
            ========
            a new Variable represents other + self
            new val = self.val + other.val
            new der = self.der + other.der
            (Error exception is raised when the input is not valid)

            EXAMPLES
            =========
            >>> x = Variable(2)
            >>> y = 1 + x
            Variable(3, 1)
        """
        return self + other

    def __neg__(self):
        """Returns -self.

            INPUTS
            =======
            self: Variable object

            RETURNS
            ========
            a new Variable represents -self.
            new val = -self.val
            new der = -self.der

            EXAMPLES
            =========
            >>> x = Variable(2)
            >>> y = -x
            Variable(-2, -1)
        """
        return Variable(-self.val, -self.der)

    def __sub__(self, other):
        """Returns self - other.

            INPUTS
            =======
            self: Variable object
            other: Variable or float/int

            RETURNS
            ========
            a new Variable represents self - other
            new val = self.val - other.val
            new der = self.der - other.der
            (Error exception is raised when the input is not valid)

            EXAMPLES
            =========
            >>> x = Variable(2)
            >>> y = x - 1
            Variable(1, 1)
        """
        return self + (-other)

    def __rsub__(self, other):
        """Returns other - self.

            INPUTS
            =======
            self: Variable object
            other: Variable or float/int

            RETURNS
            ========
            a new Variable represents other - self
            new val = other.val - self.val
            new der = other.der - self.der
            (Error exception is raised when the input is not valid)

            EXAMPLES
            =========
            >>> x = Variable(2)
            >>> y = 1 - x
            Variable(-1, -1)
        """
        return other + (-self)

    def __mul__(self, other):
        """Returns self * other.

            INPUTS
            =======
            self: Variable object
            other: Variable or float/int

            RETURNS
            ========
            a new Variable represents self * other
            new val = self.val * other.val
            new der = self.der * other (if other is number)
            new der = f'(x)g(x) + f(x)g'(x) (if other is Variable)
            (Error exception is raised when the input is not valid)

            EXAMPLES
            =========
            >>> x = Variable(2)
            >>> y = x * 2
            Variable(4, 2)
        """
        try:
            # other is a number
            if isinstance(other, (int, float)):
                return Variable(self.val * other, self.der * other)
            # assume other is a valid Variable, otherwise raise Error
            else:
                # product rule for derivative of functions
                # d/dx(f(x)g(x)) = f'(x)g(x) + f(x)g'(x)
                return Variable(self.val * other.val, self.der * other.val + self.val * other.der)
        except:
            # other error: derivatives dimensions does not match
            raise TypeError("other is not a valid Variable or number.")

    def __rmul__(self, other):
        """Returns other * self.

            INPUTS
            =======
            self: Variable object
            other: Variable or float/int

            RETURNS
            ========
            a new Variable represents self * other
            new val = self.val * other.val
            new der = self.der * other (if other is number)
            new der = f'(x)g(x) + f(x)g'(x) (if other is Variable)
            (Error exception is raised when the input is not valid)

            EXAMPLES
            =========
            >>> x = Variable(2)
            >>> y = x * 2
            Variable(4, 2)
        """
        return self * other

    def __truediv__(self, other):
        """Returns self / other.

            INPUTS
            =======
            self: Variable object
            other: Variable or float/int

            RETURNS
            ========
            a new Variable represents self / other
            new val = self.val / other.val
            new der = self.der / other (if other is number)
            new der = f'(x)g(x) - f(x)g'(x)) / (g(x)^2 (if other is Variable)
            (Error exception is raised when the input is not valid)

            EXAMPLES
            =========
            >>> x = Variable(2)
            >>> y = x / 2
            Variable(1, 1/2)
        """
        try:
            # other is a number
            if isinstance(other, (int, float)):
                return Variable(self.val / other, self.der / other)
            # assume other is a valid Variable, otherwise raise Error
            else:
                # Quotient rule for derivative of functions
                # d/dx(f(x)/g(x)) = f'(x)g(x) - f(x)g'(x)) / (g(x)^2
                return Variable(self.val / other.val,
                                (self.der * other.val - self.val * other.der) / (other.val)**2)
        except ZeroDivisionError:
            raise ZeroDivisionError("Failed when dividing by 0")
        except:
            # other error: derivatives dimensions does not match
            raise TypeError("other is not a valid Variable or number.")

    def __rtruediv__(self, other):
        """Returns other / self.

            INPUTS
            =======
            self: Variable object
            other: Variable or float/int

            RETURNS
            ========
            a new Variable represents other / self
            new val = other.val / self.val
            new der = -f'/(f^2) (if other is number)
            new der = f'(x)g(x) - f(x)g'(x)) / (g(x)^2 (if other is Variable)
            (Error exception is raised when the input is not valid or the Denominator is 0)

            EXAMPLES
            =========
            >>> x = Variable(2)
            >>> y = 2/x
            Variable(1, -1/2)
        """
        try:
            # other is a number
            if isinstance(other, (int, float)):
                # Reciprocal Rule: 1/f = -f'/(f^2)
                return Variable(other / self.val,
                                (- other * self.der) / (self.val) ** 2)
                # assume other is a valid Variable, otherwise raise Error
            else:
                # Quotient rule for derivative of functions
                # d/dx(f(x)/g(x)) = f'(x)g(x) - f(x)g'(x)) / (g(x)^2
                return Variable(other.val / self.val,
                                (other.der * self.val - other.val * self.der) / (self.val)**2)
        except ZeroDivisionError:
            raise ZeroDivisionError("Failed when dividing by 0")
        except:
            # other error: derivatives dimensions does not match
            raise TypeError("other is not a valid Variable or number.")

    def __pow__(self, power):
        """Returns self^power (x^p).

            INPUTS
            =======
            self: Variable object
            power: float/int

            RETURNS
            ========
            a new Variable represents x^p
            new val = self.val^power
            new der = d/dx(f(x)^n) = n(f(x)^(n-1)) * f'(x)

            EXAMPLES
            =========
            >>> x = Variable(2)
            >>> y = x**2
            Variable(4, 4)
        """
        return Variable(self.val ** power, power * self.val ** (power - 1) * self.der)

    def sqrt(self):
        """Returns sqrt(self) (x^0.5).

            INPUTS
            =======
            self: Variable object
            power: float/int

            RETURNS
            ========
            a new Variable represents x^0.5
            new val = self.val^0.5
            new der = d/dx(f(x)^n) = n(f(x)^(n-1)) * f'(x)

            EXAMPLES
            =========
            >>> x = Variable(4)
            >>> y = np.sqrt(x)
            Variable(2, 1/4)
        """
        return Variable(self.val, self.der) ** 0.5

    def __rpow__(self, base):
        """Returns base^(self) (a^x).

            INPUTS
            =======
            self: Variable object
            base: float/int

            RETURNS
            ========
            a new Variable represents a^x
            new val = base^self.val
            new der =  d/dx(a^f(x)) = ln(a) * a^f(x) * f'(x)

            EXAMPLES
            =========
            >>> x = Variable(2)
            >>> y = 2**x
            Variable(4, 2.7725)
        """
        return Variable(base**self.val, np.log(base) * (base ** self.val) * self.der)

    def exp(self):
        """Returns e^(self) (e^x).

            INPUTS
            =======
            self: Variable object
            base: float/int

            RETURNS
            ========
            a new Variable represents e^x
            new val = e^self.val
            new der =  d/dx(a^f(x)) = e^f(x) * f'(x)

            EXAMPLES
            =========
            >>> x = Variable(2)
            >>> y = np.exp(x)
            Variable(7.389, 7.389)
        """
        return Variable(np.exp(self.val), np.exp(self.val) * self.der)

    def log(self):
        """Returns ln(self) (ln(x)).

            INPUTS
            =======
            self: Variable object

            RETURNS
            ========
            a new Variable represents ln(x)
            new val = ln(self.val)
            new der =  ln'(x) = 1/x * x'

            EXAMPLES
            =========
            >>> x = Variable(2)
            >>> y = np.log(x)
            Variable(0.693, 0.5)
        """
        return Variable(np.log(self.val), 1 / (self.val) * (self.der))

    def sin(self):
        """Returns sin(self) (sin(x)).

            INPUTS
            =======
            self: Variable object

            RETURNS
            ========
            a new Variable represents sin(x)
            new val = sin(self.val)
            new der = sin'(x) = cos(x) * x'

            EXAMPLES
            =========
            >>> x = Variable(2)
            >>> y = np.sin(x)
            Variable(0.909, -0.416)
        """
        return Variable(np.sin(self.val), np.cos(self.val) * self.der)

    def cos(self):
        """Returns cos(self) (cos(x)).

            INPUTS
            =======
            self: Variable object

            RETURNS
            ========
            a new Variable represents cos(x)
            new val = sin(self.val)
            new der = cos'(x) = sin(x) * x'

            EXAMPLES
            =========
            >>> x = Variable(2)
            >>> y = np.cos(x)
            Variable(-0.416, -0.909)
        """
        return Variable(np.cos(self.val), -np.sin(self.val) * self.der)

    def tan(self):
        """Returns tan(self) (tan(x)).

            INPUTS
            =======
            self: Variable object

            RETURNS
            ========
            a new Variable represents cos(x)
            new val = tan(self.val)
            new der = tan'(x) = 1/(cos(x))^2 * x'

            EXAMPLES
            =========
            >>> x = Variable(2)
            >>> y = np.tan(x)
            Variable(-2.185, 5.774)
        """
        if self.val % np.pi == np.pi / 2:
            raise ValueError("input of tan should not be value of k * pi + pi/2")
        return Variable(np.tan(self.val), 1 / (np.cos(self.val)) ** 2 * self.der)

    def arcsin(self):
        """Returns arcsin(self) (arcsin(x)).

            INPUTS
            =======
            self: Variable object

            RETURNS
            ========
            a new Variable represents arcsin(x)
            new val = arcsin(self.val)
            new der = arcsin'(x) = 1/sqrt(1-x^2) * x'
            (Error would be raised if val is not within (-1,1))

            EXAMPLES
            =========
            >>> x = Variable(0.5)
            >>> y = np.arcsin(x)
            Variable(0.523, 1.154)
        """
        if self.val <= -1 or self.val >= 1:
            raise ValueError("input of arcsin should within (-1, 1)")
        return Variable(np.arcsin(self.val), 1/np.sqrt(1 - self.val**2) * self.der)

    def arccos(self):
        """Returns arccos(self) (arccos(x)).

            INPUTS
            =======
            self: Variable object

            RETURNS
            ========
            a new Variable represents arccos(x)
            new val = arccos(self.val)
            new der = arccos'(x) = -1/sqrt(1-x^2) * x'
            (Error would be raised if val is not within (-1,1))

            EXAMPLES
            =========
            >>> x = Variable(0.5)
            >>> y = np.arccos(x)
            Variable(1.047, -1.154)
        """
        if self.val <= -1 or self.val >= 1:
            raise ValueError("input of arccos should within (-1, 1)")
        return Variable(np.arccos(self.val), -1/np.sqrt(1 - self.val**2) * self.der)

    def arctan(self):
        """Returns arctan(self) (arctan(x)).

            INPUTS
            =======
            self: Variable object

            RETURNS
            ========
            a new Variable represents arctan(x)
            new val = arccos(self.val)
            new der = arctan'(x) = 1/(1+x^2) * x'

            EXAMPLES
            =========
            >>> x = Variable(0.5)
            >>> y = np.arctan(x)
            Variable(0.463, 0.8)
        """
        return Variable(np.arctan(self.val), 1/(1 + self.val**2) * self.der)

    def __str__(self):
        """Returns a string shows the val and der of the current Variable.

            INPUTS
            =======
            self: Variable object

            RETURNS
            ========
            "val: x der: x'"

            EXAMPLES
            =========
            >>> x = Variable(0.5)
            >>> print(x)
            val: 0.5 der: 1
        """
        return "val: " + str(self.val) + " der: " + str(self.der)

    def get_jacobian(self):
        '''
            Get the Jacobian matrix of partial derivatives.
            For this milestone, the Jacobian will just be a scalar.
            Will support muti input function in the future (would get a matrix)
        '''
        return self.der
