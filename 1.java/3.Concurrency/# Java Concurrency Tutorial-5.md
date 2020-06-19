# Chapter 5. Building Blocks


# 5.1 Synchronized Collections

synchronized collection 클래스에는 JDK의 일부인 Vector 및 Hashtable과 Collections.synchronized~ 팩토리 메소드로 작성된 동기화된 wrapper 클래스가 포함된다.

이런 클래스는 상태를 캡슐화하고 모든 public 메소드를 동기화하여 Thread-safety를 보장한다.

## 5.1.1. Problems with Synchronized Collections

동기화된 컬렉션을 사용하더라도 여러 스레드가 동시에 컬렉션을 수정할 수 있는 경우 예상한대로 동작하지 않을 수 있다.

### Listing 5.1
~~~java
public static Object getLast(Vector list) {
      int lastIndex = list.size() - 1;
      return list.get(lastIndex);
}

public static void deleteLast(Vector list) {
     int lastIndex = list.size() - 1;
     list.remove(lastIndex);
}
~~~

여러 스레드가 예제 5.1의 코드에서 getLast() 와 deleteLast() 를 거의 동시에 호출한다면 ArrayIndexOutOfBoundsException을 발생 시킬 수 있다.

### Listing 5.2
~~~java
public static Object getLast(Vector list) {
  synchronized (list) {
    int lastIndex = list.size() - 1;
    return list.get(lastIndex);
    }
}

public static void deleteLast(Vector list) {
  synchronized (list) {
    int lastIndex = list.size() - 1;
    list.remove(lastIndex);
    }
}
~~~

따라서 예제 5.2와 같이 동시에 수정 가능한 컬렉션을 synchronized()로 묶어서 각 작업을 원자적으로 쓰도록 해라.

예제 5.3의 for문에서 예외가 발생할 수 있지만 이것이 Vector가 Thread-safety 하지 않다는 의미는 아니다.

단, 예외가 발생할 수 있는 가능성이 있다는 것이다.

이를 해결하기 위해서는 예제 5.4와 같이 컬렉션을 synchronized() 로 묶어라.

### Listing 5.3
~~~java
for (int i = 0; i < vector.size(); i++)
    doSomething(vector.get(i));
~~~

### Listing 5.4
~~~java
synchronized (vector) {
  for (int i = 0; i < vector.size(); i++)
      doSomething(vector.get(i));
}
~~~


## 5.1.2 Iterators and Concurrentmodificationexception

* 컬렉션을 반복하는 표준 방법 2가지
1. Iterator를 사용하는 것
2. forEach (java 1.5)를 사용하는 것

예제 5.5에서처럼 forEach를 사용하여 컬렉션을 반복 처리하는 도중에 컬렉션의 내용이 수정된다면 ConcurrentModificationException이 발생할 것이다.

* 반복하는 작업에서 여러 스레드가 컬렉션의 수정을 가능하도록 하는 방법
1. synchronized() 를 이용하여 컬렉션의 작업을 원자적으로 유지한다.
2. 반복 작업을 수행할 컬렉션을 복사하여 복사된 컬렉션을 사용한다.

* 단 위의 2가지 방법은 바람직한 방법은 아니다.
1. 1번의 방법은 컬렉션에 접근해야 하는 다른 스레드가 차단되며, 각 수행 태스크가 길어지면 오래 기다려야 한다. 이는 Deadlock, 기아 상태의 위험도가 증가하게 될 가능성이 높아진다.

2. 또한 1번과 같은 경우 컬렉션이 반복될 수 있는 모든 위치에 적용을 해야 하기 때문에 까다롭다.

3. 2번의 방법은 컬렉션을 복제하는데 성능적으로 많은 비용이 발생한다.


### Listing 5.5
~~~java
List<Widget> widgetList
                           = Collections.synchronizedList(new ArrayList<Widget>());
...
// May throw ConcurrentModificationException
for (Widget w : widgetList)
      doSomething(w);
~~~


# 5.2 Concurrent Collections

java 1.5에서는 여러가지 synchronized collections를 제공한다.

synchronized collections은 모든 컬렉션에 대한 접근을 직렬화하여 Thread-safety를 달성한다.

단, synchronized collection은 동시성이 좋지 않으므로 여러 스레드가 컬렉션 경합을 하며 처리량이 저하될 수 있는 문제가 있다.

java에서는 위와 같은 문제를 해결하기 위해 concurrenct collections를 추가했다.

ConcurrentHashMap은 synchronized hashMap을 CopyOnWriteArrayList는 synchronized List를 대체하여 개선된 성능과 안전성을 보장한다.

synchronized SortedMap or SortedSet 대신에 java 1.6부터 지원되는 ConcurrentSkipListMap 과 ConcurrentSkipListSet을 사용해라

> synchronized collection 대신 concurrenct collections를 사용해라. 위험도는 낮추고 성능은 향상 시킬수 있다.


## 5.2.1. ConcurrenctHashMap

모든 개선 사항과 마찬가지로 몇가지 단점이 아직 존재한다.

1. 크기 및 isEmpty 에 대한 결과는 추정치이므로 정확한 수치가 아닌 근사값을 반환할 수 있다.


## 5.2.2. Additional Atomic Map Operations

그냥 ConcurrenctMap 써라.

## 5.2.3. CopyOnWriteArrayList

수정 될 때마다 컬렉션의 새 복사본을 만들고 다시 게시한다. 반복 시작시 현재의 백업 배열을 사용하고, 절대 변경되지 않으므로 잠깐 동안만 동기화하면 된다.

결과적으로 스레드 간 간섭이나 방해없이 컬렉션의 반복 작업을 수행할 수 있다.

### Listing 5.7
~~~java
public interface ConcurrentMap<K,V> extends Map<K,V> {
    // Insert into map only if no value is mapped from K
    V putIfAbsent(K key, V value);
    // Remove only if K is mapped to V
    boolean remove(K key, V value);
    // Replace value only if K is mapped to oldValue
    boolean replace(K key, V oldValue, V newValue);
    // Replace value only if K is mapped to some value
    V replace(K key, V newValue);
 }
~~~

단, CopyOnWriteArrayList는 컬렉션이 수정될 때마다 특히 컬렉션이 큰 경우 백업 배열을 복사하는데 약간의 비용이 든다.

> CopyOnWriteArrayList는 수정보다 반복 작업이 많을 때 사용하는 것이 합리적이다.

# 5.3. Blocking Queues and the Producer-consumer Pattern

> 블로킹 큐는 프로듀서-컨슈머 패턴을 구현하기에 좋다. 작업을 생성하고 처리하는 부분을 명확히 분리함으로써 각 부분이 받을 수 있는 부하를 조절할 수 있다. 모든 컨슈머가 하나의 블로킹 큐를 바라보다.

블로킹 큐는 일반적으로 병렬 프로그램 환경에서 성능이 좋다.

PriorityBlockingQueue - 우선 순위를 기준으로 동작하는 큐
SynchronousQueue - 충분한 개수의 컨슈머가 대기하고 있는 경우 사용하면 좋다

### Listing 5.8 프로듀서-컨슈머 패턴을 활용한 검색 어플리케이션 구조
~~~java
public class FileCrawler implements Runnable {
    private final BlockingQueue<File> fileQueue;
    private final FileFilter fileFilter;
    private final File root;     ...

    public void run() {
        try {
            crawl(root);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    private void crawl(File root) throws InterruptedException {
        File[] entries = root.listFiles(fileFilter);
        if (entries != null) {
            for (File entry : entries)
                if (entry.isDirectory()) crawl(entry);
                else if (!alreadyIndexed(entry)) fileQueue.put(entry);
        }
    }
}

public class Indexer implements Runnable {
    private final BlockingQueue<File> queue;

    public Indexer(BlockingQueue<File> queue) {
        this.queue = queue;
    }

    public void run() {
        try {
            while (true) indexFile(queue.take());
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
~~~

### Listing 5.9 검색 어플리케이션 동작시키기
~~~java
public static void startIndexing(File[] roots) {
    BlockingQueue<File> queue = new LinkedBlockingQueue<File>(BOUND);
    FileFilter filter = new FileFilter() {
        public boolean accept(File file) {
            return true;
        }
    };
    for (File root : roots) new Thread(new FileCrawler(queue, filter, root)).start();
    for (int i = 0; i < N_CONSUMERS; i++) new Thread(new Indexer(queue)).start();
}
~~~

> Deque(덱)을 사용하면 작업 가로채기 패턴을 그대로 구현할 수 있다. 모든 컨슈머가 각자의 Deque를 갖고 자신이 가지고 있던 작업을 모두 처리하면 다른 컨슈머의 Deque에 쌓여있는 데이터를 가져와서 처리한다.

* 작업 가로채기 패턴을 적용하면 좋은 상황
  * 일반적으로 규모가 큰 시스템
  * 컨슈머가 프로듀서의 역할도 갖고 있는 경우 (ex, 하나의 작업을 처리하고 나면 더 많은 작업이 생기는 경우)
  * 멀티스레드를 사용하게 될 경우 (쉽게 병렬화 할 수 있다.)


# 5.4. 블로킹 메소드, 인터럽터블 메소드

* BlockingQueue 인터페이스의 put(), take()는 Thread.sleep()과 같이 InterruptedException을 발생시킬 수 있다.
* InterruptedException이 발생한다는 것은 블로킹 메소드라는 뜻이고, 블로킹 메소드는 인터럽트에서 풀려날 수 있도록 해당 스레드를 중단 시킬수 있는 interrupt 메소드를 제공한다.

* InterrunptedException 처리하는 방법 2가지
  * InterruptedExection을 전달 - 해당 Exception을 호출한 메소드에게 그대로 throw하는 방법
  * 인터럽트를 무시하고 복구 - 해당 Exception을 캐치하여 현재 스레드의 interrupt 메소드를 호출하여 상태를 설정하고 상황 발생을 알려야한다.

> InterruptedException이 발생했을 때 하지 말아야 되는 것은 Exception을 캐치하고도 아무 대응을 하지 않는 것이다. 따라서 Listing 5.10 과 같은 처리가 필요하다.

### Listing 5.10 인터럽트가 발생했음을 저장해 인터럽트 상황을 잊지 않도록 한다.
~~~java
public class TaskRunnable implements Runnable {
    BlockingQueue<Task> queue;
    ...

    public void run() {
        try {
            processTask(queue.take());
        } catch (InterruptedException e) {
            // restore interrupted status
            Thread.currentThread().interrupt();
        }
    }
}
~~~

# 5.5. 동기화 클래스

블로킹 큐는 작업 흐름을 조절할 수 있도록 만들어졌는데 이런 모든 클래스를 동기화 클래스라고 한다.

세마포어, 배리어, 래치 모두 동기화 클래스의 예이다.

## 5.5.1 래치(Latch)

* 특정 자원을 확보하기 전에는 작업을 시작하지 말아햐 하는 경우
* 의존성을 갖는 다른 서비스가 시작하기 전에는 특정 서비스가 실해되지 않도록 막아야 하는 경우
* 특정 작업에 필요한 모든 객체가 실행할 준비를 갖출 때까지 기다리는 경우

>CountDownLatch 는 위 모든 상황에 쉽게 적용할 수 있는 구조이다.

* await() - count 값이 0이 될 때가지 작업 대기
* countDown() - count 값 감소

> 래치는 여러 작업을 하나로 묶어 다음 작업으로 진행할 수 있는 관문과 같이 사용할 수 있다. 일회성 객체이다.


### Listing 5.11 CountDownLatch를 사용해 스레드의 실행과 종료를 확인해 전체 실행 시간을 확인
~~~java
public class TestHarness {
    public long timeTasks(int nThreads, final Runnable task) throws InterruptedException {
        final CountDownLatch startGate = new CountDownLatch(1);
        final CountDownLatch endGate = new CountDownLatch(nThreads);
        for (int i = 0; i < nThreads; i++) {
            Thread t = new Thread() {
                public void run() {
                    try {
                        startGate.await();
                        try {
                            task.run();
                        } finally {
                            endGate.countDown();
                        }
                    } catch (InterruptedException ignored) {
                    }
                }
            };
            t.start();
        }
        long start = System.nanoTime();
        startGate.countDown();
        endGate.await();
        long end = System.nanoTime();
        return end - start;
    }
}
~~~

## 5.5.2 FutureTask

FutureTask 역시 래치와 비슷한 형태로 동작한다.

시작전 대기, 시작됨, 종료됨 3가지 상태를 가진다.

> get() 메소드를 호출하면 작업이 종료될때까지 기다렸다가 연산 결과 or 예외를 알려준다.


### Listing 5.12 FutureTask를 사용해 추후 필요한 데이터를 미리 읽어들이는 모습
~~~java
public class Preloader {
    private final FutureTask<ProductInfo> future = new FutureTask<ProductInfo>(new Callable<ProductInfo>() {
        public ProductInfo call() throws DataLoadException {
            return loadProductInfo();
        }
    });
    private final Thread thread = new Thread(future);

    public void start() {
        thread.start();
    }

    public ProductInfo get() throws DataLoadException, InterruptedException {
        try {
            return future.get();
        } catch (ExecutionException e) {
            Throwable cause = e.getCause();
            if (cause instanceof DataLoadException) throw (DataLoadException) cause;
            else throw launderThrowable(cause);
        }
    }
}
~~~

### Listing 5.13 Throwable을 RuntimeException으로 변환
~~~java
/**
     * If the Throwable is an Error, throw it; if it is a  *  RuntimeException return it, otherwise throw IllegalStateException
     */
    public static RuntimeException launderThrowable(Throwable t) {
        if (t instanceof RuntimeException) return (RuntimeException) t;
        else if (t instanceof Error) throw (Error) t;
        else throw new IllegalStateException("Not unchecked", t);
    }
~~~

## 5.5.3 세마포어

Counting Semaphore는 특정 자원이나 특정 연산을 동시에 사용하거나 호출할 수 있는 스레드의 수를 제한하고자 할 때 사용한다.

> 자원 pool 이나 컬렉션의 크기에 제한을 두고자 할 때 유용하다.
* acquire() - 사용할 수 있는 퍼밋이 생기거나 타임아웃 또는 인터럽트 전까지 대기
* release() - 확보했던 퍼밋을 다시 반납

> 이진 세마포어는 뮤텍스로 활용할 수 있다.
* 뮤텍스 - 비재진입 락 (nonreentrant)

* 뮤텍스와 세마포어 차이
  * 뮤텍스 : 한 쓰레드, 프로세스에 의해 소유될 수 있는 key를 기반으로 한 상호배제기법
  * 세마포어 : 공유 자원에 접근할 수 있는 쓰레드, 프로세스의 값을 두고 상호배제를 달성하는 기법

> 두 기법 모두 데이터 무결성을 보장할 수 없으며, 데드락이 발생할 수 있다.

### Listing 5.14 세마포어를 사용해 컬렉션의 크기 제한하기
~~~java
public class BoundedHashSet<T> {
    private final Set<T> set;
    private final Semaphore sem;

    public BoundedHashSet(int bound) {
        this.set = Collections.synchronizedSet(new HashSet<T>());
        sem = new Semaphore(bound);
    }

    public boolean add(T o) throws InterruptedException {
        sem.acquire();
        boolean wasAdded = false;
        try {
            wasAdded = set.add(o);
            return wasAdded;
        } finally {
            if (!wasAdded) sem.release();
        }
    }

    public boolean remove(Object o) {
        boolean wasRemoved = set.remove(o);
        if (wasRemoved) sem.release();
        return wasRemoved;
    }
}
~~~

> 위 코드에서 Set은 내부 크기를 알 필요도 신경쓸 필요도 없다. 크기와 관련된 내용은 모두 Semaphore가 관리하기 때문이다.

## 5.5.4 배리어

> 래치는 이벤트를 기다리기 위한 동기화 클래스이고, 배리어는 다른 스레드를 기다리기 위한 동기화 클래스이다.

* 래치와의 차이점은 모든 스레드가 배리어 위치에 동시에 이르러야 관문이 열리고 계속해서 실행할 수 있다는 점이다.


### Listing 5.15 CyclicBarrier를 사용해 셀룰러 오토마타의 연산을 제어
~~~java
public class CellularAutomata {
    private final Board mainBoard;
    private final CyclicBarrier barrier;
    private final Worker[] workers;

    public CellularAutomata(Board board) {
        this.mainBoard = board;
        int count = Runtime.getRuntime().availableProcessors();
        this.barrier = new CyclicBarrier(count, new Runnable() {
            public void run() {
                mainBoard.commitNewValues();
            }
        });
        this.workers = new Worker[count];
        for (int i = 0; i < count; i++) workers[i] = new Worker(mainBoard.getSubBoard(count, i));
    }

    private class Worker implements Runnable {
        private final Board board;

        public Worker(Board board) {
            this.board = board;
        }

        public void run() {
            while (!board.hasConverged()) {
                for (int x = 0; x < board.getMaxX(); x++)
                    for (int y = 0; y < board.getMaxY(); y++) board.setNewValue(x, y, computeValue(x, y));
                try {
                    barrier.await();
                } catch (InterruptedException ex) {
                    return;
                } catch (BrokenBarrierException ex) {
                    return;
                }
            }
        }
    }

    public void start() {
        for (int i = 0; i < workers.length; i++) new Thread(workers[i]).start();
        mainBoard.waitForConvergence();
    }
}
~~~

# 5.6 효율적이고 확장성 있는 결과 캐시 구현

> 캐시를 대충 만들면 단일 스레드로 처리할 때 성능은 높아질 수 있지만 확장성있는 캐시를 구현하기는 힘들것이다.



### Listing 5.16 HashMap과 동기화 기능을 사용해 구현한 첫 번째 캐시
~~~java
public interface Computable<A, V> {
    V compute(A arg) throws InterruptedException;
}

public class ExpensiveFunction implements Computable<String, BigInteger> {
    public BigInteger compute(String arg) {
        // after deep thought...
        return new BigInteger(arg);
    }
}

public class Memorizer1<A, V> implements Computable<A, V> {
    @GuardedBy("this")
    private final Map<A, V> cache = new HashMap<A, V>();
    private final Computable<A, V> c;

    public Memorizer1(Computable<A, V> c) {
        this.c = c;
    }

    public synchronized V compute(A arg) throws InterruptedException {
        V result = cache.get(arg);
        if (result == null) {
            result = c.compute(arg);
            cache.put(arg, result);
        }
        return result;
    }
}
~~~

> 위 코드에서 HashMap은 Thread-safety하지 않기 때문에 compute() 메소드 전체를 동기화 시키는 단순한 방법을 정책을 택했다. 단 이런 방법은 확장성에 문제가 생긴다. 무조건 한 스레드만 compute()에 접근할 수 있기 때문이다.

> 따라서 컬렉션 동기화를 사용하는 것이 스레드 안전성을 확보하면서도 성능을 유지할 수 있는 방법이다.

### Listing 5.17 HashMap 대신 ConcurrentHashMap을 적용
~~~java
public class Memorizer2<A, V> implements Computable<A, V> {
    private final Map<A, V> cache = new ConcurrentHashMap<A, V>();
    private final Computable<A, V> c;

    public Memorizer2(Computable<A, V> c) {
        this.c = c;
    }

    public V compute(A arg) throws InterruptedException {
        V result = cache.get(arg);
        if (result == null) {
            result = c.compute(arg);
            cache.put(arg, result);
        }
        return result;
    }
}
~~~

> 하지만 ConcurrentHashMap() 도 문제가 있다. 바로 두개 이상의 스레드가 동시에 입력값을 넘기면 두 스레드는 같은 연산을 수행할 것이고 극단적으로 말하면 이는 효율성 측면에서 캐시를 사용하는 이유가 상쇄되는 것이다.


### Listing 5.18 FutureTask를 사용한 결과 캐시
~~~java
public class Memorizer3<A, V> implements Computable<A, V> {
    private final Map<A, Future<V>> cache = new ConcurrentHashMap<A, Future<V>>();
    private final Computable<A, V> c;

    public Memorizer3(Computable<A, V> c) {
        this.c = c;
    }

    public V compute(final A arg) throws InterruptedException {
        Future<V> f = cache.get(arg);
        if (f == null) {
            Callable<V> eval = new Callable<V>() {
                public V call() throws InterruptedException {
                    return c.compute(arg);
                }
            };
            FutureTask<V> ft = new FutureTask<V>(eval);
            f = ft;
            cache.put(arg, ft);
            ft.run(); // call to c.compute happens here
        }
        try {
            return f.get();
        } catch (ExecutionException e) {
            throw launderThrowable(e.getCause());
        }
    }
}
~~~

> 이런 일을 처리할 때 유용한 것이 바로 Future 이다. Future는 입력된 값에 대한 연산 작업이 시작됐는지를 먼저 확인하고 없으면 작업을 시작한다.

> Memorizer2에 비해 여러 스레드가 같은 값에 대한 연산을 시작할 수 있는 허점이 훨씬 작긴하지만 여전히 해당 문제가 남아있다.

### Listing 5.19 Memoizer 최종 버전
~~~java
public class Memorizer<A, V> implements Computable<A, V> {
    private final ConcurrentMap<A, Future<V>> cache = new ConcurrentHashMap<A, Future<V>>();
    private final Computable<A, V> c;

    public Memorizer(Computable<A, V> c) {
        this.c = c;
    }

    public V compute(final A arg) throws InterruptedException {
        while (true) {
            Future<V> f = cache.get(arg);
            if (f == null) {
                Callable<V> eval = new Callable<V>() {
                    public V call() throws InterruptedException {
                        return c.compute(arg);
                    }
                };
                FutureTask<V> ft = new FutureTask<V>(eval);
                f = cache.putIfAbsent(arg, ft);
                if (f == null) {
                    f = ft;
                    ft.run();
                }
            }
            try {
                return f.get();
            } catch (CancellationException e) {
                cache.remove(arg, f);
            } catch (ExecutionException e) {
                throw launderThrowable(e.getCause());
            }
        }
    }
}
~~~

> put()이 아닌 putIfAbsent() 를 사용하여 동일한 입력 값에 대한 중복 연산을 방지할 수 있다.
* putIfAbsent() 는 key가 value에 mapping되어 있지 않을 때만 mapping한다.

### Listing 5.20 Memoizer를 사용해 결과를 캐시하는 인수분해 서블릿
~~~java
@ThreadSafe
public class Factorizer implements Servlet {
    private final Computable<BigInteger, BigInteger[]> c = new Computable<BigInteger, BigInteger[]>() {
        public BigInteger[] compute(BigInteger arg) {
            return factor(arg);
        }
    };
    private final Computable<BigInteger, BigInteger[]> cache = new Memorizer<BigInteger, BigInteger[]>(c);

    public void service(ServletRequest req, ServletResponse resp) {
        try {
            BigInteger i = extractFromRequest(req);
            encodeIntoResponse(resp, cache.compute(i));
        } catch (InterruptedException e) {
            encodeError(resp, "factorization interrupted");
        }
    }
}
~~~

# 정리

## 5.1 Synchronized Collections
  * Thread-safety 를 보장할 수 있는 방법
  * 하지만 이는 성능 저하를 발생 시킬 수 있고
  * 동기화 대상을 일일히 지정 및 관리해줘야 하는 단점이 있다.

## 5.2 Concurrent Collections
  * ConcurrentHashMap, CopyOnWriteArrayList, ConcurrentSkipListSet 등의 concurrent collections을 사용해라.

## 5.3 Blocking Queues and the Producer-consumer Pattern
  * 병렬 프로그래밍 환경에서 성능을 향상 시키고 작업 영역을 분리함으로써 어플리케이션의 부하를 조절할 수 있다.

## 5.4 블로킹 메소드, 인터럽터블 메소드
  * 블로킹 메소드는 인터럽트를 발생시킬 수 있는데 이때 Exception을 처리하는 방법 2가지
  1. InterruptedExection을 전달 - 해당 Exception을 호출한 메소드에게 그대로 throw하는 방법
  2. 인터럽트를 무시하고 복구 - 해당 Exception을 캐치하여 현재 스레드의 interrupt 메소드를 호출하여 상태를 설정하고 상황 발생을 알려야한다.

>  Exception을 캐치하고도 아무 대응을 하지 않는 것은 가장 안좋은 방법이다.

## 5.5 동기화 클래스
  * Semaphore, barrier, Latch, Future 등
    1. Latch - 여러 작업을 하나로 묶어 다음 작업으로 진행할 수 있는 관문 역할로 사용, 일회성 객체
    2. Future - 래치와 비슷한 형태로 동작
    3. Semaphore - 특정 자원이나 연상을 동시에 사용하거나 호출할 수 있는 스레드의 수를 제한할 때 사용
    4. Barrier - 다른 스레드를 기다리기 위한 동기화 클래스, 모든 스레드가 배리어 위치에 동시에 이르러야 관문이 열린다.?
  * 작업 흐름을 조저할 수 있는 클래스

## 5.6 효율적이고 확장성 있는 결과 캐시 구현
  * Concurrent Collection을 사용해라.
  * FutureTask를 사용해라.
  * putIfAbsent()와 같은 검증 가능한 메소드를 사용해라.

![Concurrency5](../99.Img/Concurrency5.png)