<<<<<<< HEAD
# Chapter 3. Sharing Objects

명시적으로 synchronization을 사용하거나 동기화 클래스에 내장된 라이브러리를 사용하여 객체의 Thread-safety를 지켜라.

## 3.1 Visibility

Listing 3.1은 스레드가 동기화 없이 데이터를 공유하는 잘못된 사용법을 보여준다.

42를 print하기를 기대하지만 실제로는 0을 찍거나 종료하지 않을 수도 있다.

### Listing 3.1
~~~java
public class NoVisibility {

    private static boolean ready;
    private static int number;

    private static class ReaderThread extends Thread {
        public void run() {
            while (!ready) Thread.yield();
            System.out.println(number);
        }
    }

    public static void main(String[] args) {
        new ReaderThread().start();
        number = 42;
        ready = true;
    }
}
~~~

> 데이터가 스레드간에 공유되기 전에 항상 동기화 상태를 유지시켜라.

~~~java
@NotThreadSafe
public class MutableInteger {
    private int value;

    public int get() {
        return value;
    }

    public void set(int value) {
        this.value = value;
    }
}
~~~

~~~java
@ThreadSafe
class SynchronizedInteger {
    @GuardedBy("this")
    private int value;

    public synchronized int get() {
        return value;
    }

    public synchronized void set(int value) {
        this.value = value;
    }
}
~~~

> 동기화를 하는것 만으로는 stale data 문제를 해결하기에 충분하지 않다. get을 호출하는 코드는 여전히 오래된 데이터를 볼 수 있다.

* 그림 3.1에서처럼 Intrinsic locking-고유 락(monitor lock, monitor,)을 사용하여 하나의 스레드가 다른 스레드의 영향도를 예측 가능하는 것을 보장할 수 있다.

![concurrency3.1](./../99.Img/Concurrency3.1.png)

> Lock은 단지 상호 배제만을 위한 것은 아니다. Lock은 메모리 가시성을 위한 것이 될 수 있다.
> 모든 스레드가 공유된 최신 가변 변수를 읽고 쓸수 있도록 공통 lock에서 동기화 되어야 한다.

### Volatile Variables

* volatile : 약한 synchronization 방식
> SynchroinzedInteger 클래스와 매우 유사하게 동작하면서도 volatile 변수에 접근할 때 Lock을 사용하지는 않기 때문에 synchronized 를 사용하는 것보다 가볍다.

1. volatile 변수 쓰기 : 동기화된 Block을 해제하는 것
2. volatile 변수 읽기 : 동기화된 Block을 입력하는 것

> volatile은 동기화 정책을 단순하게 구현할 때만 사용해라. 정확성을 검증하는 곳에서는 사용하지 마라.

> volatile 사용의 가장 좋은 예는 완료, 중단과 같은 상태 플래그이다.
  * 증감 연산과 같은 작업을 원자적으로 처리하기에 충분하지 않다.

> Locking은 가시성과 원자성을 모두 보장할 수 있으며 volatile은 가시성만 보장한다.

* 다음 기준을 모두 충족할 때 volatile 변수를 사용할 수 있다.
  * 변수의 write / read 스레드가 구분되어 있을 때
  * 멀티 스레드 환경에서 synchronized 되어 있을 때

## 3.2 Publication and Escape

객체를 게시한다는 것은 현재 범위 밖에서 코드를 작성할 수 있게 하는 것을 의미한다.

내부 상태 변수를 게시하면 캡슐화가 손상되고 Immutable을 보존하기 힘들어진다.

이 장은 안전하게 객체를 게시하는 방법을 다룰 것이다.

### Listing 3.5 Publishing an Object
~~~java
public static Set<Secret> knownSecrets;

public void initialize() {
  knownSecrets = new HashSet<Secret>();
}
~~~

> 위 처럼 public static 필드에 참조 값을 게시하는 것은 가장 뻔뻔한? 짓이다.


### Listing 3.6. Allowing Internal Mutable State to Escape. Don't Do this.
~~~java
class UnsafeStates {
  private String[] states = new String[] {
    "AK", "AL" ...
    };
  public String[] getStates() {
    return states;
    }
}
~~~

> 위처럼 쓰지마라. 내부 Mutable 변수가 밖에서도 사용되도록 허용하지 마라. 위 코드라면 호출자가 states 변수를 수정할 수 있기 때문에 좋지 않다.

> 비록 states를 private으로 선언했지만 getStates()를 어디서든 호출가능하기 때문에 의미가 없어졌다.



### Listing 3.7 this 참초를 통한 탈출을 허용하지 마라.
~~~java
public class ThisEscape {
    public ThisEscape(EventSource source) {
        source.registerListener(new EventListener() {
            public void onEvent(Event e) {
                doSomething(e);
            }
        });
    }
}
~~~


### Listing 3.8 Factory Method를 사용하여 this 참조를 통한 탈출을 막아라.
~~~java
public class SafeListener {
    private final EventListener listener;

    private SafeListener() {
        listener = new EventListener() {
            public void onEvent(Event e) {
                doSomething(e);
            }
        };
    }

    public static SafeListener newInstance(EventSource source) {
        SafeListener safe = new SafeListener();
        source.registerListener(safe.listener);
        return safe;
    }
}
~~~

## 3.3 Thread Confinement, 스레드 제한

### 3.9 기본형 참조형 지역 변수의 스레드 제한
~~~java
public int loadTheArk(Collection<Animal> candidates) {
      SortedSet<Animal> animals;
      int numPairs = 0;
      Animal candidate = null;

      // animals confined to method, don't let them escape!
      animals = new TreeSet<Animal>(new SpeciesGenderComparator());
      animals.addAll(candidates);
      for (Animal a : animals) {
          if (candidate == null || !candidate.isPotentialMate(a))
            candidate = a;
          else {
              ark.load(new AnimalPair(candidate, a));
              ++numPairs;
              candidate = null;
          }
      }
      return numPairs;
}
~~~

### 3.10 ThreadLocal을 사용하여 스레드 제한
~~~java
private static ThreadLocal<Connection> connectionHolder
        = new ThreadLocal<Connection>() {
            public Connection initialValue() {
                return DriverManager.getConnection(DB_URL);
            }
        };

public static Connection getConnection() {
    return connectionHolder.get();
}
~~~

## 3.4 Immutability

> Immutable 객체는 언제나 Therad-safety하다.

final 필드라도 변경 가능한 객체에 대한 참조를 보유할 수 있으므로 final 필드 역시 변경 가능하다.

* Immutable 객체
  * 일단 생성된 후에 상태를 수정할 수 없다.
  * 모든 필드가 final이어야 한다.
  * this 참조가 탈출하지 않는다.?

> 가능하면 모든 변수는 private, final로 선언해라.


### Listing 3.12
~~~java
@Immutable
class OneValueCache {
    private final BigInteger lastNumber;
    private final BigInteger[] lastFactors;

    public OneValueCache(BigInteger i, BigInteger[] factors) {
        lastNumber = i;
        lastFactors = Arrays.copyOf(factors, factors.length);
    }

    public BigInteger[] getFactors(BigInteger i) {
        if (lastNumber == null || !lastNumber.equals(i)) return null;
        else return Arrays.copyOf(lastFactors, lastFactors.length);
    }
}
~~~

## 3.5 Safe Publication

~~~java
@ThreadSafe
public class VolatileCachedFactorizer implements Servlet {
    private volatile OneValueCache cache = new OneValueCache(null, null);

    public void service(ServletRequest req, ServletResponse resp) {
        BigInteger i = extractFromRequest(req);
        BigInteger[] factors = cache.getFactors(i);
        if (factors == null) {
            factors = factor(i);
            cache = new OneValueCache(i, factors);
        }
        encodeIntoResponse(resp, factors);
    }
}
~~~

아래 코드는 동기화가 사용되지 않았기 때문에 다른 스레드에서 잘못된 값을 참조할 수 있다. holder 필드의 오래된 값을 보거나 null 값을 볼 수 도 있다.

~~~java
// Unsafe publication
public Holder holder;
public void initialize() {
  holder = new Holder(42);
}
~~~

~~~java
public class Holder {
    private int n;

    public Holder(int n) {
        this.n = n;
    }

    public void assertSanity() {
        if (n != n) throw new AssertionError("This statement is false.");
    }
}
~~~

* 객체를 안전하게 게시하는 방법 - 객체에 대한 참조와 상태가 모두 다른 스레드에 동시에 표시되어야 한다.
  * static으로 선언된 initializer에서 참조 객체를 초기화해라.
  * volatile 필드 or AtomicReference에 참조값을 저장해라.
  * 올바르게 구성된 객체의 final 필드에 참조값을 저장해라.
  * lock에 의해 올바르게 보호되는 필드에 참조값을 저장해라.


Thread-safety 컬렉션의 내부 동기화라는 것은 vector나 synchronizedList와 같은 Thread-safety 컬렉션안의 객체를 저장하는 것을 의미한다.

> Thread-safety 컬렉션은 명시적인 동기화가 없더라도 다음과 같은 안전한 상황을 보장한다.
* Hashtable, synchronizedMap, Concurrent-Map을 사용해라.
* Vector, CopyOnWriteArrayList, CopyOnWrite-ArraySet, synchronizedList, synchronizedSet을 사용해라.
* BlockingQueue or ConcurrentLinkedQueue를 사용해라.

> static 초기화는 JVM에 의해 실행되므로 JVM 내부 동기화 메커니즘으로 안전한 초기화가 보장된다.

> 안전하게 게시된 불변 객체는 모든 스레드에서 추가 동기화 없이 사용할 수 있다.

~~~java
public Map<String, Date> lastLogin =
          Collections.synchronizedMap(new HashMap<String, Date>());
~~~


# 정리

## 1. Visibility

객체의 가시성을 확보하는 방법 2가지

> synchronized vs volatile
1. synchronized : Lock을 사용하므로 무겁다. Multi 접근이 안됨->성능 저하 가능성
2. volatile : 가벼운 synchronized, But 원자성을 보장할 순 없다.

> volatile을 안전하게 사용하려면, 공유 변수에 대한 읽기 / 쓰기 스레드가 구분되어 있어야 한다.

## 2. 객체의 Publication and Escape

> 내부 mutable 변수를 외부에서 호출 가능하도록 만들지 마라.

> 팩토리 메서드를 사용하자.

## 3. 스레드 제한

> ThreadLocal을 사용하자.

## 4. 불변성

> Immutable 객체를 사용하자.

> 객체에 대한 참조 상태가 모든 스레드에서 동시에 표시되도록 하자.

> 가능하면 모든 변수는 private, final로 선언해라.

=======
# Chapter 3. Sharing Objects

명시적으로 synchronization을 사용하거나 동기화 클래스에 내장된 라이브러리를 사용하여 객체의 Thread-safety를 지켜라.

## 3.1 Visibility

Listing 3.1은 스레드가 동기화 없이 데이터를 공유하는 잘못된 사용법을 보여준다.

42를 print하기를 기대하지만 실제로는 0을 찍거나 종료하지 않을 수도 있다.

### Listing 3.1
~~~java
public class NoVisibility {

    private static boolean ready;
    private static int number;

    private static class ReaderThread extends Thread {
        public void run() {
            while (!ready) Thread.yield();
            System.out.println(number);
        }
    }

    public static void main(String[] args) {
        new ReaderThread().start();
        number = 42;
        ready = true;
    }
}
~~~

> 데이터가 스레드간에 공유되기 전에 항상 동기화 상태를 유지시켜라.

~~~java
@NotThreadSafe
public class MutableInteger {
    private int value;

    public int get() {
        return value;
    }

    public void set(int value) {
        this.value = value;
    }
}
~~~

~~~java
@ThreadSafe
class SynchronizedInteger {
    @GuardedBy("this")
    private int value;

    public synchronized int get() {
        return value;
    }

    public synchronized void set(int value) {
        this.value = value;
    }
}
~~~

> 동기화를 하는것 만으로는 stale data 문제를 해결하기에 충분하지 않다. get을 호출하는 코드는 여전히 오래된 데이터를 볼 수 있다.

* 그림 3.1에서처럼 Intrinsic locking-고유 락(monitor lock, monitor,)을 사용하여 하나의 스레드가 다른 스레드의 영향도를 예측 가능하는 것을 보장할 수 있다.

![concurrency3.1](./../99.Img/Concurrency3.1.png)

> Lock은 단지 상호 배제만을 위한 것은 아니다. Lock은 메모리 가시성을 위한 것이 될 수 있다.
> 모든 스레드가 공유된 최신 가변 변수를 읽고 쓸수 있도록 공통 lock에서 동기화 되어야 한다.

### Volatile Variables

* volatile : 약한 synchronization 방식
> SynchroinzedInteger 클래스와 매우 유사하게 동작하면서도 volatile 변수에 접근할 때 Lock을 사용하지는 않기 때문에 synchronized 를 사용하는 것보다 가볍다.

1. volatile 변수 쓰기 : 동기화된 Block을 해제하는 것
2. volatile 변수 읽기 : 동기화된 Block을 입력하는 것

> volatile은 동기화 정책을 단순하게 구현할 때만 사용해라. 정확성을 검증하는 곳에서는 사용하지 마라.

> volatile 사용의 가장 좋은 예는 완료, 중단과 같은 상태 플래그이다.
  * 증감 연산과 같은 작업을 원자적으로 처리하기에 충분하지 않다.

> Locking은 가시성과 원자성을 모두 보장할 수 있으며 volatile은 가시성만 보장한다.

* 다음 기준을 모두 충족할 때 volatile 변수를 사용할 수 있다.
  * 변수의 write / read 스레드가 구분되어 있을 때
  * 멀티 스레드 환경에서 synchronized 되어 있을 때

## 3.2 Publication and Escape

객체를 게시한다는 것은 현재 범위 밖에서 코드를 작성할 수 있게 하는 것을 의미한다.

내부 상태 변수를 게시하면 캡슐화가 손상되고 Immutable을 보존하기 힘들어진다.

이 장은 안전하게 객체를 게시하는 방법을 다룰 것이다.

### Listing 3.5 Publishing an Object
~~~java
public static Set<Secret> knownSecrets;

public void initialize() {
  knownSecrets = new HashSet<Secret>();
}
~~~

> 위 처럼 public static 필드에 참조 값을 게시하는 것은 가장 뻔뻔한? 짓이다.


### Listing 3.6. Allowing Internal Mutable State to Escape. Don't Do this.
~~~java
class UnsafeStates {
  private String[] states = new String[] {
    "AK", "AL" ...
    };
  public String[] getStates() {
    return states;
    }
}
~~~

> 위처럼 쓰지마라. 내부 Mutable 변수가 밖에서도 사용되도록 허용하지 마라. 위 코드라면 호출자가 states 변수를 수정할 수 있기 때문에 좋지 않다.

> 비록 states를 private으로 선언했지만 getStates()를 어디서든 호출가능하기 때문에 의미가 없어졌다.



### Listing 3.7 this 참초를 통한 탈출을 허용하지 마라.
~~~java
public class ThisEscape {
    public ThisEscape(EventSource source) {
        source.registerListener(new EventListener() {
            public void onEvent(Event e) {
                doSomething(e);
            }
        });
    }
}
~~~


### Listing 3.8 Factory Method를 사용하여 this 참조를 통한 탈출을 막아라.
~~~java
public class SafeListener {
    private final EventListener listener;

    private SafeListener() {
        listener = new EventListener() {
            public void onEvent(Event e) {
                doSomething(e);
            }
        };
    }

    public static SafeListener newInstance(EventSource source) {
        SafeListener safe = new SafeListener();
        source.registerListener(safe.listener);
        return safe;
    }
}
~~~

## 3.3 Thread Confinement, 스레드 제한

### 3.9 기본형 참조형 지역 변수의 스레드 제한
~~~java
public int loadTheArk(Collection<Animal> candidates) {
      SortedSet<Animal> animals;
      int numPairs = 0;
      Animal candidate = null;

      // animals confined to method, don't let them escape!
      animals = new TreeSet<Animal>(new SpeciesGenderComparator());
      animals.addAll(candidates);
      for (Animal a : animals) {
          if (candidate == null || !candidate.isPotentialMate(a))
            candidate = a;
          else {
              ark.load(new AnimalPair(candidate, a));
              ++numPairs;
              candidate = null;
          }
      }
      return numPairs;
}
~~~

### 3.10 ThreadLocal을 사용하여 스레드 제한
~~~java
private static ThreadLocal<Connection> connectionHolder
        = new ThreadLocal<Connection>() {
            public Connection initialValue() {
                return DriverManager.getConnection(DB_URL);
            }
        };

public static Connection getConnection() {
    return connectionHolder.get();
}
~~~

## 3.4 Immutability

> Immutable 객체는 언제나 Therad-safety하다.

final 필드라도 변경 가능한 객체에 대한 참조를 보유할 수 있으므로 final 필드 역시 변경 가능하다.

* Immutable 객체
  * 일단 생성된 후에 상태를 수정할 수 없다.
  * 모든 필드가 final이어야 한다.
  * this 참조가 탈출하지 않는다.?

> 가능하면 모든 변수는 private, final로 선언해라.


### Listing 3.12
~~~java
@Immutable
class OneValueCache {
    private final BigInteger lastNumber;
    private final BigInteger[] lastFactors;

    public OneValueCache(BigInteger i, BigInteger[] factors) {
        lastNumber = i;
        lastFactors = Arrays.copyOf(factors, factors.length);
    }

    public BigInteger[] getFactors(BigInteger i) {
        if (lastNumber == null || !lastNumber.equals(i)) return null;
        else return Arrays.copyOf(lastFactors, lastFactors.length);
    }
}
~~~

## 3.5 Safe Publication

~~~java
@ThreadSafe
public class VolatileCachedFactorizer implements Servlet {
    private volatile OneValueCache cache = new OneValueCache(null, null);

    public void service(ServletRequest req, ServletResponse resp) {
        BigInteger i = extractFromRequest(req);
        BigInteger[] factors = cache.getFactors(i);
        if (factors == null) {
            factors = factor(i);
            cache = new OneValueCache(i, factors);
        }
        encodeIntoResponse(resp, factors);
    }
}
~~~

아래 코드는 동기화가 사용되지 않았기 때문에 다른 스레드에서 잘못된 값을 참조할 수 있다. holder 필드의 오래된 값을 보거나 null 값을 볼 수 도 있다.

~~~java
// Unsafe publication
public Holder holder;
public void initialize() {
  holder = new Holder(42);
}
~~~

~~~java
public class Holder {
    private int n;

    public Holder(int n) {
        this.n = n;
    }

    public void assertSanity() {
        if (n != n) throw new AssertionError("This statement is false.");
    }
}
~~~

* 객체를 안전하게 게시하는 방법 - 객체에 대한 참조와 상태가 모두 다른 스레드에 동시에 표시되어야 한다.
  * static으로 선언된 initializer에서 참조 객체를 초기화해라.
  * volatile 필드 or AtomicReference에 참조값을 저장해라.
  * 올바르게 구성된 객체의 final 필드에 참조값을 저장해라.
  * lock에 의해 올바르게 보호되는 필드에 참조값을 저장해라.


Thread-safety 컬렉션의 내부 동기화라는 것은 vector나 synchronizedList와 같은 Thread-safety 컬렉션안의 객체를 저장하는 것을 의미한다.

> Thread-safety 컬렉션은 명시적인 동기화가 없더라도 다음과 같은 안전한 상황을 보장한다.
* Hashtable, synchronizedMap, Concurrent-Map을 사용해라.
* Vector, CopyOnWriteArrayList, CopyOnWrite-ArraySet, synchronizedList, synchronizedSet을 사용해라.
* BlockingQueue or ConcurrentLinkedQueue를 사용해라.

> static 초기화는 JVM에 의해 실행되므로 JVM 내부 동기화 메커니즘으로 안전한 초기화가 보장된다.

> 안전하게 게시된 불변 객체는 모든 스레드에서 추가 동기화 없이 사용할 수 있다.

~~~java
public Map<String, Date> lastLogin =
          Collections.synchronizedMap(new HashMap<String, Date>());
~~~


# 정리

## 1. Visibility

객체의 가시성을 확보하는 방법 2가지

> synchronized vs volatile
1. synchronized : Lock을 사용하므로 무겁다. Multi 접근이 안됨->성능 저하 가능성
2. volatile : 가벼운 synchronized, But 원자성을 보장할 순 없다.

> volatile을 안전하게 사용하려면, 공유 변수에 대한 읽기 / 쓰기 스레드가 구분되어 있어야 한다.

## 2. 객체의 Publication and Escape

> 내부 mutable 변수를 외부에서 호출 가능하도록 만들지 마라.

> 팩토리 메서드를 사용하자.

## 3. 스레드 제한

> ThreadLocal을 사용하자.

## 4. 불변성

> Immutable 객체를 사용하자.

> 객체에 대한 참조 상태가 모든 스레드에서 동시에 표시되도록 하자.

> 가능하면 모든 변수는 private, final로 선언해라.

>>>>>>> 199dcd17923b9ab64d081d598e2eca5a8f415615
> 참조 객체는 Thread-safety한 컬렉션을 사용하자.