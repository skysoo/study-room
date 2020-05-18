# 1. 메모리 영역
1. 메서드 = 클래스 = static
	* 클래스 로더에 의해 로딩된 클래스, 메소드, static(클래스변수), 전역변수(<->필드변수)
	* 가장 먼저 데이터가 저장되는 공간
	* 클래스 변수나 전역변수를 무분별하게 많이 사용하면 메모리가 부족할 수 있다

2. 힙
	* 런타임시 결정되는 참조형 데이터 타입이 저장되는 공간
	* new 연산자를 통해 생성된 객체
	* GC가 일어나는 영역

3. 스택
	* 런타임시 결정되는 기본형 데이터 타입이 저장되는 공간
	* 지역변수, 매개변수, 리턴값, 참조변수(주소값) 등이 저장됨
	* 메서드 호출 때 메모리에 filo로 하나씩 생성

![jvm 구조](../99.Img/JVMStructureJava8.png)

Java7 이전에는 Permanent 영역이 존재했었지만 Java8 부터 해당 영역은 사라졌고 Permanet 영역에 저장되었던 아래 내용들은 Metaspace 영역에 저장된다.

* Constant pool information(String) -> Heap
* Methods of class -> Native
* Names of the classes -> Native
* Static variables -> Heap

![메모리 구조 변경사항](../99.Img/JVMJava8.png)

Java7 이전에는 new로 선언된 String만 Heap 영역에 저장되었고 literal로 선언된 String은 String Constant Pool 에 저장되었으며(Perm영역) GC의 대상이 아니었지만

> Java8 부터 Constant Pool의 저장 영역이 Heap으로 바뀌면서 literal로 선언된 String 역시 GC 대상이 된다.


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

![Java 자료형 크기](../99.Img/JavaDataTypesize.png)


# 2. GC(Garbage Collection) 구조

  GC란? Java에서 메모리 누수를 방지하기 위해 사용하는 방법으로 JVM의 힙 영역에 존재하는 오브젝트들 중에서 더이상 사용되지 않는 오브젝트들을 지우고 해당 오브젝트에 할당 되었던 메모리를 반환 받는 작업을 일컫는다.

### 2.1 GC 예제
아래 간단하 예제 코드를 통해 Java에서 메모리를 할당하는 과정과 GC가 일어나는 과정에 대해 알아보자.

~~~java
public class Main {
	public static void main(String[] args) {
		String url = "https://";							// 지역 변수, 참조형 데이터
		url += "skysoo1111.github.io";
		System.out.println(url);
	}
}
~~~

url 변수는 main() 함수 안에 선언되었으므로 지역 변수로써 Stack 영역에 메모리가 할당되며, 그 값은 참조형 데이터로 Heap 영역에 할당 될 것이다.

~~~java
String url = "https://";
~~~
![Memory 할당1](../99.Img/MemoryAllocation1.png)


또한 url 에 붙여진 문자열은 기존 데이터가 아닌 새롭게 Heap 영역에 할당 될 것이다.

~~~java
url += "skysoo1111.github.io";
~~~
![Memory 할당2](../99.Img/MemoryAllocation2.png)


그로인해 이전 참조값이었던 String https:// 는 더이상 사용되지 않는 데이터가 되었다. 이를 Stack 영역에서 도달 불가능한 값이라 하여 Unreachable 오브젝트라고 한다.

![Memory 할당3](../99.Img/MemoryAllocation3.png)


이렇게 발생하는 Unreachable 데이터들은 GC 대상이 된다.


### 2.2 GC 과정

![GC](../99.Img/GCSpaceJava8.png)

Java8에서 메모리 관련하여 가장 두드러진 변화는 Heap영역에서 Permanent Generation 이 사라지고 이를 Native Memory 영역의 Metaspace가 대체한 것이다.

* Heap 영역
  * Young Generation
    * Eden : 새로 생성된 오브젝트들이 할당되는 영역
    * Suvivor0 : MinorGC에서 살아남은(Reachable) 오브젝트들이 Eden영역으로부터 이동하는 영역
    * Suvivor1 : S0에 존재하는 오브젝트들 중 MinorGC에서 살아남은 오브젝트들이 이동하는 영역

> Eden 영역이 가득찰 때 마다 MinorGC가 일어난다. MinorGC가 반복될 때 마다 살아남은 오브젝트들은 S0과 S1 영역을 번갈아가며 이동하고 이동할 때 마다 오브젝트들의 Age가 증가한다.

  * Old Generation
    * Old : Survivor 영역에 존재하는 오브젝트들의 Age 값이 특정값을 넘겼을 때 이동하는 영역으로 이 단계를 Promotion 이라고 한다.

> Old Generation이 가득차게 되면 MajorGC가 발생한다.


> 참조 <https://yaboong.github.io/java/2018/06/09/java-garbage-collection/>