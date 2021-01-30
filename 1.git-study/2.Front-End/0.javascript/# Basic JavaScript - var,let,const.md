# Basic JavaScript - var,let,const

# ES6 이란?

ECMAScript 이며, JavaScript 언어의 표준이다.

# var, let, const 차이점은?

ES6 이전에는 변수를 선언하는 방법이 var를 이용하는 방법 밖에 없었다. 하지만 var에 대한 여러가지 문제들이 있었고 이를 해결하고자 let과 const가 나오게 되었다.

먼저 var가 가진 문제점을 알아보자.

## var(function-scoped)

1. var로 변수 선언 시 var 키워드 생략 가능

```js
chicken = "nice";
console.log(chicken); // nice
```

2. var로 변수 선언 후 중복 선언 가능

```js
var chicken = "nice";
console.log(chicken); // nice

var chicken = 1;
console.log(chicken); // 1
```

3. 변수가 선언되지도 않았는데 참조 가능 (변수 호이스팅)

```js
console.log(chicken); // undefined
var chicken = "nice";
console.log(chicken); // nice
```

4. function-scoped로 코드 블록만 Scope로 인정
   함수 외부에서 선언된 모든 var 변수는 전역 변수로 사용된다.

```js
var chicken = "good";
console.log(chicken); // good
{
  chicken = "nice";
}
console.log(chicken); // nice

for (var i = 0; i <= 5; i++) {
  console.log(i); // 0~5까지 출력
}
console.log(i); //6

function testVar() {
  var moon = "dal";
}
console.log(moon); // 참조 에러 발생
```

### 변수 호이스팅 이란?

일반적으로 변수를 참조해서 사용하려면 선언 -> 초기화 -> 할당 이 3단계에 걸친다.

하지만 var는 변수 선언과 초기화가 동시에 이뤄진다. 사용자가 초기화를 하지 않더라도 변수는 undefined으로 초기화 된다.

따라서 초기화되지 않은 변수를 사용하게되는 문제가 발생할 수 있는 것이다.

- var는 function-scoped
- let, const는 block-scoped

## let (block-scoped)

let을 이용한 변수 선언은 Block Scope 내에 변수를 선언한다.

## const (block-scoped)

const를 이용하여 선언한 변수는 let과 거의 동일하지만 재할당을 할 수 없다. (java의 final?)

# 결론

block-scoped 이면서 변수 중복 선언 불가, 호이스팅 불가한 let과 const를 사용하자.

> 변수 재할당이 필요하면 let, 재할당이 불필요하면 const를 사용하자.
