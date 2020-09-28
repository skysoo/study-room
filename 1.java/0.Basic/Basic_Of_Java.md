## Java Fields

* primitive fileds
    + boolean, byte, short, int, long, char, float, and double

* reference fileds
    + interface, arrays, etc


## Java Scope

* public
* protected (상속 클래스 패키지 접근 가능)
* default
* private


## 자바 기동 원리

1. java 파일
2. javac가 바이트 코드로 변환시킨다.
3. .java -> .class
4. class loader가 class파일을 jvm 메모리 영역으로 올린다.
5. 실행기가 jvm 메모리 영역(run time영역)의 바이트 코드를 해석하며 실행한다.

![jvm 구조](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2FS6oXr%2FbtqCly0BxOl%2FeQMn2i1qHlGUk9mMkCJ3dk%2Fimg.png)


## 메모리 영역

1. 메서드 = 클래스 = static
	: 클래스 로더에 의해 로딩된 클래스, 메소드, static(클래스변수), 전역변수(<->필드변수)
	: 가장 먼저 데이터가 저장되는 공간
	: 클래스 변수나 전역변수를 무분별하게 많이 사용하면 메모리가 부족할 수 있다

2. 힙
	: 런타임시 결정되는 참조형 데이터 타입이 저장되는 공간
	: new 연산자를 통해 생성된 객체

3. 스택
	: 런타임시 결정되는 기본형 데이터 타입이 저장되는 공간
	: 지역변수, 매개변수, 리턴값, 참조변수 등이 저장됨
	: 메서드 호출 때 메모리에 filo로 하나씩 생성


스택에는 원시 타입 변수와 참조 변수의 주소 값이 저장된다.

힙에는 참조값이 저장된다.

GC는 힙 영역에 대해 이뤄진다.

	> 참조 - <https://yaboong.github.io/java/2018/05/26/java-memory-management/>


## 추상클래스 vs 인터페이스

* 추상 클래스 : 상속받아 사용하며 부모 클래스의 기능을 이용하거나 확장하기 위해 사용
* 인터페이스 : 구현한 객체들에 대해서 동일한 동작을 약속하기 위해 존재하며 함수의 구현을 강제한다.

## Interface vs Class

Interface :  리턴값을 구현 해야한다.

Class : 새로운 객체로 생성할 수 있다.

## 변수

지역 변수 : 함수 안에 선언

전역 변수 : 함수 밖에 선언, 필드 변수

클래스 변수 : static 변수

인스턴스 변수


## JDBC

java에서 db에 접근하기 위해 사용하는 라이브러리
=> sql문 작성 및 db에 종속적이기 때문에 table,column 변경시 코드 다 변경

=> db에 종속적이지 않게 java 코드를 작성할 수 있다는 것이 큰 장점
jpa(hibernetes)

## Integer vs int

: java는 auto boxing/unboxing 지원함
	Integer : 객체
	int : 자료형

	int -> Wrapping -> Integer(Wrapper 클래스) - auto boxing
	Integer -> UnWrapping -> int(자료형) - auto unboxing

	Integer는 산술 연산이 불가능하나 auto boxing/unboxing으로 인해 가능한거처럼 보임
	Integer는 null값 처리 가능

# Collections



## Java 8 Stream

=> 배열과 컬렉션을 함수형으로 처리할 수 있다.

filter() :
map() :


## Thread

* Thread Status
  객체 생성 NEW
	실행 대기 RUNNABLE
	일시 정지  WAITING - wait(), join(), sleep()
								TIMED_WAITING - wait(), join(), sleep() WAITING 상태와의 차이점은 외부적인 변화뿐 아니라 시간에 의해서도 WAITING 상태가 해제 될 수 있다
								BLOCKED - monitor를 획득하기 위해 다른 스레드가 락을 해제하기를 기다리는 상태(스레드 동기화와 관련)
	실행 				RUN
	종료				TERMINATED

1. Thread 구현 방법
   1. Thread 상속
      1. start() 메서드 호출 가능

   2. Runnable 구현한 뒤, Thread 객체 생성
      1. start() 메서드 호출 불가능, 반드시 Thread 객체에 담아서 사용

	 3. Lambda를 사용하여 runnable 구현


2. start()와 run()의 차이점?

	start() : New 상태 -> Runnable 상태 (실행 가능한 대기 큐에 들어간 것을 의미한다.)
					메타 정보를 넣고 run()한다.

	run() :  메타 정보를 넣지 않고 run()한다. 제대로된 thread 정보를 가져오지 못할 수 도 있다.

> run()은 단순히 메소드를 실행하는 것이고(싱글스레드), start()는 스택을 만들고 스택안에서 run()하는 것이다.(멀티스레드)



3. Callable<V> 와 Runnable의 차이점?
=> 둘 다 구현된 함수를 수행한다는 공통점이 있지만 다음과 같은 차이점이 있다.

Callable : 특정 타입의 객체를 리턴한다. (null일 수도) Exception을 발생시킬 수 도 있다.
	구현 메소드 : call()
	Thread에 인자로 전달 될 수 없다. => ExecutorService 객체에 submit() 메소드를 사용하여 전달한다. (스레드 풀을 사용)
JAVA 1.5

Runnable : 어떤 객체도 리턴하지 않는다. Exception을 발생시키지 않는다.
	구현 메소드 : run()
	Thread에 인자로 전달되어 사용된다.
JAVA 1.0






## Java Object Pattern

public interface CrawlingWorker extends Callable<Void>

public class DataCrawlingWorker implements CrawlingWorker
  @Override
    public Void call() {}
public class HostCrawlingWorker implements CrawlingWorker
  @Override
    public Void call() {}


abstract class AbstractCrawler<T extends CrawlingWorker> implements Closeable
  protected abstract List<T> createRunners(Collection<String> urls);


public class RvDataCrawler extends AbstractCrawler<DataCrawlingWorker>
  @Override
    protected List<DataCrawlingWorker> createRunners(Collection<String> urls) {}
    List<DataCrawlingWorker> result = Lists.newArrayListWithExpectedSize(urls.size());
      => result.add(new DataCrawlingWorker(rvWebBulkService, url, exList, rvWebCacheManager)); => new DataCrawlingWorker()에서 call() 메서드 실행 결과

      => List<T> collectorRunners = createRunners(urls);
              List<Future<Void>> futures = collectService.invokeAll(collectorRunners); => invokeAll(Collections(Callable))

public class RvHostCrawler extends AbstractCrawler<HostCrawlingWorker>
  @Override
    protected List<HostCrawlingWorker> createRunners(Collection<String> urls) {}
    List<HostCrawlingWorker> collectorRunners = Lists.newArrayListWithExpectedSize(urls.size()); => callable 객체 생성해서 담기
      => collectorRunners.add(new HostCrawlingWorker(urlTargetFactory, url, serviceCrawlFailCounter, rvWebBulkService)); => new HostCrawlingWorker()에서 call() 메서드 실행 결과

        => List<T> collectorRunners = createRunners(urls);
              List<Future<Void>> futures = collectService.invokeAll(collectorRunners); => invokeAll(Collections(Callable))