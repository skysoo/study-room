# 1. 메모리 영역
1. 메서드 = 클래스 = static
	: 클래스 로더에 의해 로딩된 클래스, 메소드, static(클래스변수), 전역변수(<->필드변수)
	: 가장 먼저 데이터가 저장되는 공간
	: 클래스 변수나 전역변수를 무분별하게 많이 사용하면 메모리가 부족할 수 있다

2. 힙
	: 런타임시 결정되는 참조형 데이터 타입이 저장되는 공간
	: new 연산자를 통해 생성된 객체
	: GC가 일어나는 영역

3. 스택
	: 런타임시 결정되는 기본형 데이터 타입이 저장되는 공간
	: 지역변수, 매개변수, 리턴값, 참조변수(주소값) 등이 저장됨
	: 메서드 호출 때 메모리에 filo로 하나씩 생성

![jvm 구조](https://github.com/skysoo/study-basic/blob/master/1.java/99.Img/JVMMemoryStructure.png)


	> 참조 <https://yaboong.github.io/java/2018/05/26/java-memory-management/>

### 1-1. 자바 기동 원리
1. java 파일
2. javac가 바이트 코드로 변환시킨다.
3. .java -> .class
4. class loader가 class파일을 jvm 메모리 영역으로 올린다.
5. 실행기가 jvm 메모리 영역(run time영역)의 바이트 코드를 해석하며 실행한다.


### 1-2. Java variables
* 지역 변수 : 함수 안에 선언 / 함수 실행될 때
* 전역 변수 : 함수 밖에 선언, 필드 변수
  * 클래스 변수 : static 변수 / 클래스 올라갈 때
  * 인스턴스 변수 : 객체 변수 / 인스턴스 생성될 때


### 1-3. Java Scope
* public
* protected (상속 클래스 패키지 접근 가능)
* default
* private

### 1-4. Java Data type Fields
* primitive fileds (기본형 데이터) - 스택 영역
    + boolean, byte, short, int, long, char, float, and double , 참조형 데이터 주소값
* reference fileds (참조형 데이터) - 힙 영역
    + interface, arrays, etc

![Java 자료형 크기](https://github.com/skysoo/study-basic/blob/master/1.java/99.Img/JavaDataTypesize.png)


# 2. GC 구조