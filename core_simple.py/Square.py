class Square(Function):
    def forward(self, x):
        return x**2
    
    def backward(self, gy):
        x = self.inputs[0].data    # 수정된것.  원래는 x = self.input.data 였다.
        gx = 2*x*gy
        return gx
    
def square(x):
    return Square()(x)

Variable.__square__ = square
        