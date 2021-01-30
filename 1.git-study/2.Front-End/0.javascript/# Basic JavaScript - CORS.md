# CORS란?

CORS는 SOP 정책을 깨고 Cross-Origin Resource Sharing의 약어로 외부 도메인에서의 요청(접근)을 허용해주는 규약을 말한다.

> SOP : Same Origin Policy 동일 출처 정책으로 같은 도메인에서만 접근 가능하다라는 정책이다. 여기서 같은 출처란 프로토콜, 호스트명, 포트가 같다는 의미이다.

## CORS 종류

1. Simple
2. Preflight
3. Credential
4. Non-Credential

5. Simple Request

   - 필수 조건

   1. GET, HEAD, POST 중 1가지 방식을 사용해야 한다.
   2. POST일 경우 셋 중 하나여야 한다.
      _ application/x-www-from-urlencoded
      _ multipart/form-data \* text/plain
   3. 커스텀 헤더를 전송하면 안됨

6. Preflight Request
   Simple Request 조건에 해당하지 않으면 브라우저는Preflight Request방식으로 요청함

7. Credential Request
   HTTP Cookie와 HTTP Authentication 정보를 인식할 수 있게 해주는 요청

서버는 Response Header에 반드시 Access-Control-Allow-Credentials: true를 포함해야함

Access-Control-Allow-Origin 헤더의 값에 명확히 http://abc.com 같이 명확한 값을 줘야함

4. CORS 요청은 기본적으로 Non-Credential 요청임

## 요청 허용 방법

1. 요청을 받는 쪽에서 크로스 도메인 요청을 허용

서버의 헤더에 아래 코드를 넣어줘야 한다.

> Accss-Control-allow-origin : \*

2. 요청을 보내는 쪽에서 크로스 도메인 허용

> crossDomain: true 옵션 필수

```js
$.ajax({
  type: "POST",
  crossDomain: true,
  url: url,
  dataType: "json",
  success: function (data, textStatus, xhr) {
    $("#bidValue").val(JSON.stringify(data));
  },
});
```

# 만약 요청 받는 쪽의 코드를 수정할 수 없다면?

> JSONP를 사용하자.

# JSONP란

CORS가 활성화 되기 이전의 데이터 요청 방법이다.

주로 다른 도메인으로부터 데이터를 가져오기 위해 사용하는 방법이다.

그리고 GET으로 넘어가기 때문에 보안상 중요한 값을 이 방식으로 데이터를 주고 받으면 안된다.
