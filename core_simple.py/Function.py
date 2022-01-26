import weakref

class Function:    # init은 인스턴스 초기화 할 때 불러와지고, call은 인스턴스가 호출되었을 때 실행.
    def __call__(self, *inputs):    # 여기서 inputs는 tuple로 반환된다. 
        xs = [as_variable(x) for x in inputs]    # Add나 Mul처럼 이 Function을 상속하는 함수들에서 float이나 int를 nd.array형태로 처리해주면 여기서 Variable로 바꿔서 처리함.
        ys = self.forward(*xs)    # np.ndarray type은 어떤 계산이후에 type이 바뀔 수 있으므로, 
        if not isinstance(ys, tuple):
            ys = (ys,)
        outputs = [Variable(as_array(y)) for y in ys]    # outputs는 현재 리스트, return문에서 참고.
        
        if Config.enable_backprop:
            self.generation = max([x.generation for x in inputs])    # 여기서 inputs는 입력변수를 뜻함. 입력변수와 Function의 세대는 같으니까, Function의 generation 설정.
            
            for output in outputs:
                output.set_creator(self)    # 연결을 동적으로 만드는 기법의 핵심. 계산 그래프를 거꾸로 거슬러 올라갈 수 있다.(backward) -> forward시에는 필요없음.
                
            self.inputs = inputs    # backward할때 입력했던 입력변수가 필요하니, 저장.
            self.outputs = [weakref.ref(output) for output in outputs]
        return outputs if len(outputs)>1 else outputs[0]    # outputs에 원소가 하나뿐이면 리스트가 아니라 그 원소만을 반환한다. 
    
    def forward(self, x):
            raise NotImplementedError()
        
    def backward(self, gy):
        raise NotImplementedError()