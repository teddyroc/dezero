from core_simple.as_array import as_array


class Mul(Function):
    def forward(self, x0,x1):
        y = x0*x1
        return y
    
    def backward(self, gy):
        x0, x1 = self.inputs[0].data, self.inputs[1].data
        return x1*gy, x0*gy
    
    def mul(x0, x1):
        x1 = as_array(x1)
        return Mul()(x0,x1)
    

    

    
