# Thread-safe 클래스 정의를 위해 다음의 7가지를 실천해라.

## 1. No State
> 여러 스레드가 동일한 instance or static 변수에 접근하는 경우 이를 막는 가장 좋은 방법은 상태값을 가지는 변수를 만들지 않는 것이다.
> 클래스에 instance와 static 변수를 사용하지 않고, 로컬 변수와 인자값만을 사용해라.

  ~~~java
  public static int subtractExact(int x, int y) {
    int r = x - y;
    if (((x ^ y) & (x ^ r)) < 0) {
        throw new ArithmeticException("integer overflow");
    }
    return r;
  }
  ~~~


## 2. No Shared State
> 꼭 상태값을 가지는 변수가 필요하다면, 상태값을 공유하지 않도록 해라. => Thread Local 변수 사용

Thread 클래스를 상속 받고 instance 변수를 선언하여 스레드 로컬 instance 변수를 얻을 수 있다.

  ~~~java
package java.util.concurrent;
public class ForkJoinWorkerThread extends Thread {
    final ForkJoinPool pool;
    final ForkJoinPool.WorkQueue workQueue;
}
  ~~~

스레드 로컬 변수를 얻는 다른 방법은 스레드 로컬로 만들려는 필드에 java.lang.ThreadLocal 클래스를 사용하는 것이다.

  ~~~java
public class CallbackState {
public static final ThreadLocal<CallbackStatePerThread> callbackStatePerThread =
    new ThreadLocal<CallbackStatePerThread>()
   {
      @Override
        protected CallbackStatePerThread  initialValue()
      {
       return getOrCreateCallbackStatePerThread();
      }
   };
}
  ~~~
java.lang.ThreadLocal 안에 instance 변수 유형을 래핑하여 사용하고, initialValue() 함수로 초기 값을 제공할 수 있다.

다음은 선언된 ThreadLocal instance 변수를 사용하는 방법이다.
  ~~~java
CallbackStatePerThread callbackStatePerThread = CallbackState.callbackStatePerThread.get();
  ~~~

> ThreadLocal은 높은 메모리 소비를 유발하기 때문에, 요청 처리가 많은 클래스에서는 권장하지 않는다.

## 3. Message Passing
2번의 내용대로 상태값을 공유하지 않으면서도 스레드간 통신을 할 방법이 필요하다.

> 이는 java.util.concurrent 패키지에서 동시 큐를 사용하여 메세지 전달을 구현할 수 있다.
> 또는 동시성 프레임워크인 Akka를 사용하는 것도 좋은 방법이다.

Akka 로 메세지를 보내는 방법
~~~
target.tell(message, getSelf());
~~~

메세지를 받는 방법
~~~java
@Override
public Receive createReceive() {
     return receiveBuilder()
        .match(String.class, s -> System.out.println(s.toLowerCase()))
        .build();
}
~~~

## 4. Use the Data Structures From java.util.concurrent

스레드간 통신을 위해 동시 큐를 사용한다. 동시 큐는 java.util.concurrent에 제공된 데이터 구조 중 하나이다.

이 패키지는 스레드 안정성이 보장된 concurrent maps, queues, dequeues, sets, lists 와 같은 클래스를 제공한다.


## 5. Immutable State

여러 스레드가 동일한 변수에 접근할 때, A스레드의 변수 값이 B스레드에 의해 변경되면 안된다.

> Immutable 상태의 클래스를 구현하려면 모든 필드를 final로 선언해야 한다.

~~~java
public class ExampleFinalField
{
    private final int finalField;
    public ExampleFinalField(int value)
    {
        this.finalField = value;
    }
}
~~~


## 6. Synchronized Blocks

위의 5가지 방안을 사용할 수 없는 경우 동기화된 잠금 (synchronized locks) 을 사용해라.

> synchronized blocks안에는 한번에 하나의 스레드만 접근할 수 있다.

~~~java
synchronized(lock)
{
    i++;
}
~~~

> 여러 개의 중첩된 synchronized blocks를 사용하는 경우 교착 상태 (daedlocks)가 발생할 수 있다.


## 7. Volatile Fields

일반 필드는 레지스터나 캐시 영역에 캐시 될 수 있다.

Volatile 변수는 JVM과 컴파일러에 항상 최신 값을 반환하도록 지시한다.

~~~java
public class ExampleVolatileField
{
    private volatile int  volatileField;
}
~~~

A 스레드가 Volatile 변수에 값을 쓰고 이후 B 스레드가 동일한 변수를 읽을 때, A가 변수의 값을 쓰기를 마쳤을 때 Volatile 변수를 읽은 값이 B에 표시된다.

## Conclusion

Thread-safe를 지키는 가장 좋은 방법은 공유 상태 자체를 피하는 것이다.

그것이 불가피한 경우 Immutable Class를 만들고 동시성(Synchronized)과 가시성(Visbility)을 사용하는 데이터 구조를 이용해라.


> 참조 - <https://dzone.com/articles/7-techniques-for-thread-safe-classes>