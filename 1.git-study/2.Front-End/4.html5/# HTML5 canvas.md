# HTML5 canvas

이렇게 css에서도 크기 값을 줄 수 있다. 우선 적용
단, 아래 script에서 크기를 적용한 값이 화면에 반영이 안되는 것은 아니다.

그렇다면 왜 굳이 script로 크기를 지정하면 되는데, css에서 크기를 지정하나?

고해상도로 표현하기 위해서 아래와 같은 방식을 많이 쓴다.

1. script 에서 실제 표현할 크기의 두배로 크기 지정
2. css 에서 실제 크기로 압축해서 크기 지정

그러나 위의 방식은 픽셀 수가 많아지고 성능상의 이슈가 발생할 수 있다.

// fillRect - 붓으로 물감을 붇는 것
// clearRect - 지우개
// strokeRect - 붓으로 선을 긋는 것
const canvas = document.querySelector('.canvas');
const context = canvas.getContext('2d');
console.log(context);

// canvas는 그림을 그린다고 생각해야 한다.
// fillStyle 선언부는 물감을 묻힌 붓을 들었다고 생각하면 된다. 따라서 fillStype 아래로는 물감을 칠한 붓이 계속 적용되는 것이다.
// 새로운 붓을 들기 전까지

// beginPath - 선 그리기 시작을 의미
// moveTo - 붓을 옮긴다.
// lineTo - 선을 그린다.
// closePath - 선 그리기의 끝을 의미
const canvas = document.querySelector('.canvas');
const context = canvas.getContext('2d');

      context.beginPath();
      context.moveTo(100,100);
      context.lineTo(50,50);
      context.stroke();
      // context.fill(); 색 채우기
      context.closePath();




      function 라디안(각도) {
        return 각도 * Math.PI / 180;
      }
      // beginPath
      // arc
      // closePath
      const canvas = document.querySelector('.canvas');
      const context = canvas.getContext('2d');

      context.beginPath();
      // arc(x,y,지름 크기, a도, b도, 방향)
      context.arc(300,200,50,0, 라디안(360), false);

Animation의 타이밍을 제어하는 방법은 크게 두가지가 있다.

1. setInterval(func(), time);
   간단하게 작업을 반복해서 스케줄링할 수 있다.

하지만 성능 이슈라던지 작업에 제약이 발생할 때, 작업 대기, 프레임이 유실 등의 문제가 발생할 가능성이 높다.

2. requestAnimationFrame(func()) 반복
   requestAnimationFrame()을 사용할 경우 1번에서 발생하는 이슈들에 대한 대응이 가능하다라는 장점이 존재한다.

===========

애니메이션을 멈추게 하는 방법

1. 특정 조건에 맞을 때

2. cancleAnimationFrame() 을 이용하는 방법
   requestAnimationFrame() 을 호출하면 Id 값이 리턴되는데, 그 리턴 값을 이용해서 멈춰라.

=================

이벤트 객체의 위치 정보를 찾는 두가지 메서드

1. event.clientY
2. event.layerY
