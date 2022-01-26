from audioop import add, mul

from numpy import rad2deg
from core_simple.rsub import rsub

from core_simple.sub import sub


class Variable:
    
    __array_priority__ = 200    # 연산의 좌항이 nd.array일때, Variable의 __rmul__ 메서드가 불렸으면 좋겠을 때, 연산자 우선순위를 높게 설정한다.
    
    def __init__(self, data, name=None):    # 앞으로 수많은 변수들을 처리할 것이라서 변수들을 서로 구분할 필요가 있다.
        if data is not None:
            if not isinstance(data, np.ndarray):
                raise TypeError('{}은 지원하지 않습니다.'.format(type(data)))
                
        self.data = data
        self.grad = None
        self.creator = None
        self.name = name
        self.generation = 0   # 세대수를 기록하는 변수. 분기가 있는 계산그래프에서 역전파를 제대로 하기 위해선.
        
    def set_creator(self, func):
        self.creator = func
        self.generation = func.generation + 1    # func보다는 genteration이 항상 1크다. Variable이
        
    def backward(self, retain_grad = False):    # gy를 안받네,, f에서 구현한 output을 통해 변수를 따로 선언할 것이다. gys,gxs
        if self.grad is None:
            self.grad = np.ones_like(self.data)
            
        funcs = []
        seen_set = set()
        
        def add_func(f):
            if f not in seen_set:
                funcs.append(f)
                seen_set.add(f)
                funcs.sort(key=lambda x: x.generation)
                
        add_func(self.creator)
        
        
        
        while funcs:
            f = funcs.pop()
            # 수정전 gys = [output.grad for output in f.outputs]    # f의 output들의 grad를 뽑아서
            gys = [output().grad for output in f.outputs]
            gxs = f.backward(*gys)    # 위에서 리스트로 받았으니, 넘겨줄땐 unpacking 해서 넘겨준다.
            if not isinstance(gxs, tuple):
                gxs = (gxs,)
                
            for x, gx in zip(f.inputs, gxs):
                if x.grad is None:
                    x.grad = gx
                else:
                    x.grad = x.grad + gx
                
                if x.creator is not None:    # 각 input으로 들어왔던 애들의 mother creator가 있을때, 다 넣어줘,
                    add_func(x.creator)
                    
            if not retain_grad:
                for y in f.outputs:
                    y().grad = None    # y는 약한참조(weakref) -> retain_grad = False(기본값)이면, 마지막 입력값의 grad빼고 다 None이됨. 참조카운트가 사라지므로,
            
                    
    def cleargrad(self):
        self.grad = None
        
        
    ''' 
    Variable은 데이터를 담는 '상자' 역할을 한다. 그러나 사용하는 사람입장에서 중요한 것은 상자가 아니라 그 안의 '데이터'이다. 그래서 Variable이 데이터인 것처럼 보이게하는 장치,
    즉, .shape처럼 했을 때 (2,3)처럼 나오면서 이 인스턴스가 ndarray 처럼 생겼구나 하고 사용자에게 알려줄 의도로 추가한다. 이때 메서드를 추가해 인스턴스 변수처럼 사용할 수 있도록
    할 것이다.
    '''
    

    
    @property    # 이 한줄 덕분에 shape메서드를 shape()이 아니라 .shape으로, 마치 인스턴스 변수처럼 사용할 수 있게 된다. Variable().shape 처럼.
    def shape(self):
        return self.data.shape
                    
    @property
    def ndim(self):
        return self.data.ndim
    
    @property
    def size(self):
        return self.data.size
    
    @property
    def dtype(self):
        return self.data.dtype
    
    '''
    len 함수와 print 함수
    '''
    
    def __len__(self):
        return len(self.data)
    
    def __repr__(self):    # print 함수가 출력해주는 문자열을 입맛에 맞게 정의할 때 쓴다.
        if self.data is None:
            return 'Variable(None)'
        p = str(self.data).replace('\n', '\n' + ' '*9)
        return 'Variable(' + p + ')'   
                    
                    
'''
    def __mul__(self, other):
        return mul(self, other)
    를 간단히 쓰면 아래처럼 쓸 수 있다. x*2.0은 수행할 수 있었다(x가 Variable 인스턴스). x1에 as_array를 적용하여 x1이 float이나 int 인경우 대응가능.
    이때는 x의 mul 메써드를 쓰게되는데, 만약 2.0*x 으로하면 2.0의 __mul__메써드를 구현하려함. float에는 이 메서드가 없기 때문에, x의 __rmul__(self, other)을 쓰려한다.
    참고) 이 경우에 self는 자신인 x에 대응하고, other는 다른쪽 항인 2.0에 대응한다. 
'''

Variable.__add__ = add
Variable.__radd__ = add    # add하면 앞에 있는 인수의 add 메서드를 불러오는데, 만약 앞에 add가 없다면 오른쪽의 radd를 가져온다. other가 
Variable.__rmul__ = mul
Variable.__mul__ = mul
Variable.__sub__ = sub
Variable.__rsub__ = rsub
Variable.__truediv__ = div
Variable.__rtruediv__ = rdiv
Variable.__pow__ = pow
# 별도 함수를 구성하고나서, 얘까지 안하면 Variable 사이에 +나 * 못쓴다고 나온다.
