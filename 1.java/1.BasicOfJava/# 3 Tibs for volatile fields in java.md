# 3 Tibs for volatile fields in java

## 1. Volatile 이란?

* Java에서는 성능 향상을 위해 Main Memory에서 읽어온 변수 값을 CPU cache에 저장해놓고 사용하는데, 만약 Multi Thread 환경이라면 각 Thread가 변수 값을 읽어올 때 변수값 불일치 문제가 생길 수 있다. 이러한 문제를 해결하기 위해 나온 것이 volatile 키워드이다.

> volatile 키워드를 사용하게 되면 변수의 Read & Write 가 일어날 때 마다 변수의 값을 CPU cache가 아닌 Main Memory에 직접 접근하여 처리하게 한다.

> CPU cache 보다 Main Memory의 비용이 더 크므로 성능 저하가 발생할 수 있다.

## 2. 언제 쓰면 되나?
* Read 와 Write 의 Thread가 구분되어 있는 상황
* 변수의 값 일치가 보장되어야 하는 경우

## 3. 언제 쓰면 안되나?
* Multi Thread가 Write를 하는 상황

> 만약 여러 Thread가 Write를 해야하는 상황이라면 synchronized를 통해 변수의 Read & Write의 원자성을 보장해줘야 한다.

# 4.  Volatile 변수 사용을 위한 3가지 팁

## 1. 현재 값이 쓰기에 의존적이지 않고 독립적이게 쓰일 때, volatile 필드를 사용해라.
~~~java
public class WorkerThread extends Thread {
    private volatile boolean isRunning = true;
    @Override
    public void run() {
        while(isRunning)
        {
            // execute a task
        }
    }
    public void stopWorker()
    {
        isRunning = false;
    }
}
~~~

위 코드에서 만약 isRunning이 Volatile으로 선언되지 않았다면, stopWorker()의 요청으로 인해 Main Memory의 isRunning의 값은 false로 바뀌었지만 CPU cache의 값에 반영이 되지 않는 상황이 발생할 수 있고 그로인해 원하는 시점에 stopWorker()가 동작하지 않을 수 있다. 즉, isRunning 필드에 대한 변수 불일치가 발생할 수 있다.


## 2. 읽기에는 volatile을 쓰고 쓰기에는 lock을 사용해라.

아래 코드는 읽기에서 일관성 있는 상태 표시를 보장하고 쓰기는 Thread-safety를 보장한다.
~~~java
public class CopyOnWriteArrayList<E>
    implements List<E>, RandomAccess, Cloneable, java.io.Serializable {
    private transient volatile Object[] array;
    final Object[] getArray() {
          return array;
    }
    final void setArray(Object[] a) {
          array = a;
    }
    private E get(Object[] a, int index) {
          return (E) a[index];
    }
    public E get(int index) {
          return get(getArray(), index);
    }
    public E set(int index, E element) {
          final ReentrantLock lock = this.lock;
          lock.lock();
          try {
              Object[] elements = getArray();
              E oldValue = get(elements, index);
              if (oldValue != element) {
                  int len = elements.length;
                  Object[] newElements = Arrays.copyOf(elements, len);
                  newElements[index] = element;
                  setArray(newElements);
              } else {
                  // Not quite a no-op; ensures volatile write semantics
                  setArray(elements);
              }
              return oldValue;
          } finally {
              lock.unlock();
          }
      }
      // Other fields and methods omitted
}
~~~

> 단 너무 많은 읽기가 실행되면 쓰기의 기아 상태를 초래할 수 있다.



## 3. 원자적인 작업은 JDK 9 VarHandler와 함께 사용해라.

모든 최신 cpu는 원자적으로 값을 비교하고 설정하거나 값을 얻는 지침을 제공한다. 이러한 작업은 JVM에서 동기화된 잠금을 구현하기 위해 내부적으로 사용되었으며, JDK 1.9 이전에는 java.util.concurrent.atomic 패키지의 클래스 또는 개인 Java API에서만 사용할 수 있었다.

하지만 이제 JDK 9 VarHandler를 사용하면 Volatile 필드에서 직접 이러한 작업을 실행할 수 있다. VarHandler의 compareAndSet은 내부적으로 getVolatile과 setVolatile을 사용하여 변수의 값을 읽기 및 쓰기를 지원한다.

~~~java
public class AtomicBoolean implements java.io.Serializable {
  private static final VarHandle VALUE;
  static {
        try {
            MethodHandles.Lookup l = MethodHandles.lookup();
            VALUE = l.findVarHandle(AtomicBoolean.class, "value", int.class);
        } catch (ReflectiveOperationException e) {
            throw new Error(e);
        }
    }
    private volatile int value;
    public final boolean compareAndSet(boolean expectedValue, boolean newValue) {
        return VALUE.compareAndSet(this,
                                   (expectedValue ? 1 : 0),
                                   (newValue ? 1 : 0));
    }
    // Other fields and methods omitted
}
~~~

> 참조 - <http://vmlens.com/articles/3_tips_volatile_fields/>
