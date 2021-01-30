개요

N샷 러닝 모델
N : 범주
K : 데이터셋

퓨샷 러닝 모델의 성능은 N과 반비례, K와는 비례한다.

모델이 훈련 데이터에만 지나치게 적응해 테스트 데이터 또는 새로운 데이터에는 제대로 반응하지 못하는 현상을 해결하고자



배경

최초 소개된 것은 1990년대로 서명 검증을 위한 신경망으로 제안되었다.

이미지 인식 분야에서 각 label 의 이미지 수가 적을 때 이를 인식하고 분류하는 것은 challenging 합니다. 
예를 들어 얼굴 인식 분야에서는 단 몇 장의 이미지만을 통해 동일인인지 여부를 구분해야하는 문제가 있습니다. 
물론 augmentation 과 같은 방법으로 샘플 수를 늘려서 CNN 으로 multi-class classification 문제를 풀도록 학습시키는 방법이 가능합니다. 
하지만 이 경우, 새로운 사람이 데이터 베이스에 추가되었을 때, 모델을 새로 학습해야한다는 문제가 생깁니다. 
즉, 실시간 시스템에 적합하지 않은 방법입니다. 

이러한 아이디어의 의미는 face recognition 에서는 누구인지 구분하는 것보다 "동일인지 여부" 가 중요하다는 것입니다



샴 네트워크 구조

1. 두 이미지에 대해 CNN 을 통과시켜 나온 두 representation 의 l1 vector 를 구합니다 (l1 vector는 CNN 으로 변환된 벡터의 absolute distance 를 원소로 갖는 vector 입니다).
2. l1 vector 를 hidden layer 에 통과시킨후 output layer 에서 sigmoid 변환을 합니다. 
3. Binary cross entropy 를 loss function 으로 모델을 학습합니다. 
4. 모델은 0-1 사이의 값을 갖는 output 내보냅니다. 이 값은 크면 클 수록 두 이미지가 비슷하다라는 것이므로 "similarity" 라고 할 수 있습니다. 
5. 이 과정을 거치면 X1, X2 에 대한 CNN 의 output representation f(X1), f(X2) 는 같은 사람에 대해서 distance가 작게, 다른 사람에 대해서는 distance 가 크게 나오게 됩니다.


* 활용 분야

1. 손 제스처 인식

샴 네트워크는 이미지의 유사도를 판단할 때 이미지 전체를 고려하여 판단한다는 단점이 존재
=> 이미지 상의 손 검출을 위한 손실함수를 추가하고 이를 위한 네트워크를 추가 결합하고 이 네트워크는 학습시에만 사용한다.
=> 테스트시에는 기존의 샴네트워크만을 사용한다.

http://www.riss.kr/search/detail/DetailView.do?p_mat_type=be54d9b8bc7cdb09&control_no=6a41a1c8db049df3ffe0bdc3ef48d419&outLink=K

2. 화자 인식


* 개선 방향

1. 다양한 네트워크와 결합하여 사용

Siam Unet
https://www.semanticscholar.org/paper/Siam-U-Net%3A-encoder-decoder-siamese-network-for-in-Dunnhofer-Antico/d841747cab31a9531c2d7755fc9067b862fdfcbe

Siam Gan
https://arxiv.org/pdf/1807.08370.pdf

Siam LSTM 
https://www.dbpia.co.kr/Journal/articleDetail?nodeId=NODE07503165

2. 유사도 측정 방법은 거리 계산이 핵심
거리를 계산하는 다양한 방법 존재 - 데이터 특정에 맞게 사용

=> 맨하탄 거리, 코사인 유사도 등 다양한 계산법 적용 가능


