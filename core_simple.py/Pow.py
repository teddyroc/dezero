from calendar import c


class Pow(Function):
    def __init__(self, c):
        self.c = c
    
    def forward(self, x):
        return x**self.c
    
    def backward(self, gy):
        x = self.inputs[0].data
        c = self.c
        gx = c*x**(c-1)*gy
        return gx
    
def pow(x,c):
    return Pow()(x,c)

