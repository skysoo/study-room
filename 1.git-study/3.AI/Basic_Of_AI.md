# 용어

Convolutional Layer - 모든 Input이 거쳐가는 첫번째 수행 Layer, 피쳐를 뽑아내는 역할
Activation Layer - ReLU
Pooling Layer - 없음
Fully Connected Layer
Dropout

Filter Size - 이미지의 특징을 찾아내기 위한 파라미터, Kernel과 같은 의미
Stride
Padding

Input Size 100 _ 100
filer size 3 _ 3
stride 1
padding 1 - filter와 stride의 영향으로 피쳐맵 크기는 입력 값보다 작다. Convolution Layer의 출력 값이 줄어드는 것을
방지하기 위한 것이 패딩이다. 데이터의 외각에 특정 값을 채워 넣는 것을 의미한다.

input size 39
filter 4 4
stride 1

# loss 함수

: 모델의 출력값과 사용자가 원하는 출력값의 차이.

- 같은 모델을 대상으로 하더라도 데이터의 특성에 따라 loss 함수는 변경될 수 있다. => 모델의 성능을 올리기 위해서
-

## 1. MSE ( Mean of Squared Error ) - 평균 제곱 오차

![MSE 함수](https://mblogthumb-phinf.pstatic.net/MjAxNzA2MTBfMjk3/MDAxNDk3MDc3MTMwOTQ2.GgGlorZevi3xnKcBFHqCrG6JKGaWMa-IvVv-927bzecg.8JF52k5hIgKhdEbkzcoo_yPW6Hac3WIucgThhTGvFnsg.JPEG.wideeyed/MSE_formula.jpg?type=w2)

```py
# MSE(Mean Squared Error) : (오차)값이 작을수록  정답에 가깝다.
# yi는 신경망의 출력, ti는 정답 레이블(One-Hot인코딩)
def mean_squared_error(y, t):
    return ((y-t)**2).mean(axis=None)
```

## 2. CEE ( Cross Entropy Error ) - 크로스 엔트로피 - 교차 엔트로피 오차

![크로스엔프로피 함수](https://mblogthumb-phinf.pstatic.net/MjAxNzA2MTBfMjI4/MDAxNDk3MDc3MTMwNzM1.3daOicpC7-jE5mdbBRO25T6rHZxlh5YhCB8-Q5YsrE4g.d_g_7KF-4pUsqaQuu1nh9j_4COwCH5_msdNdt3HEPTsg.JPEG.wideeyed/CEE_formula.jpg?type=w2)

```py
# CEE(Cross Entropy Error) : (오차)값이 작을수록  정답에 가깝다.
# yi는 신경망의 출력, ti는 정답 레이블(One-Hot인코딩)
def cross_entropy_error(y, t):
    if 1 == y.ndim: # y의 차원수가 1이면 1차원이면 2차원으로 변환
        y = y.reshape(1, y.size)
        t = t.reshape(1, t.size)
    delta = 1e-7
    return -np.sum(np.log(y+delta) * t)/y.shape[0]
```

margin loss

# Optimizer

## 1. Adam Optimizer
