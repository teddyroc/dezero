class Sub(Function):
    def forward(self, x0, x1):
        y = x0 - x1
        return y
    
    def backward(self, gy):
        return gy*1, gy*(-1)
    
def sub(x0,x1):
    x1 = as_array(x1)
    return Sub()(x0,x1)
