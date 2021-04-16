# 비교 연산자 == 와 ===의 차이는?

1. == 는 동등 연산자
   피연산자가 서로 다른 타입이면 타입을 강제로 변환하여 비교한다.
2. === 는 일치 연산자
   두 피연산자의 데이터 타입까지 같아야지 같은 값으로 보기때문에 보다 정확한 비교가 가능하다.

```js
alert(1=='1') // true
alert(1==='1') // false
```

> 특별한 경우가 아니라면 === 사용을 권장한다.