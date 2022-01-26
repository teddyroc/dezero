# 2-x
def rsub(x0,x1):
    x1 = as_array(x1)
    return Sub()(x1,x0)   # Sub는 기본적으로 앞에꺼 - 뒤에꺼 이므로 반대로 전해준다.