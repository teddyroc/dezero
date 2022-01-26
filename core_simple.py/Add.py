class Add(Function):
    def forward(self, x0,x1):
        y = x0+x1
        return y
    
    def backward(self, gy):
        return gy,gy
    
    def add(x0, x1):
        x1 = as_array(x1)
        return Add()(x0, x1)    # Function을 상속했으니, __call__ 메서드가 있어서 인스턴스를 부를때 forward가 실행됨..
    
    '''
    x0가 Variable이라고 생각했는데 만약 x0 자리에 ndarray 인스턴스가 왔을 경우에는, 
    Variable 인스턴스의 연산자 우선순위를 ndarray 인스턴스의 연산자 우선순위보다 높여 해결한다.
    __array_priority__ = 높게 설정.
    '''

def add(x0,x1):
    x1 = as_array(x1)
    return Add()(x0,x1)