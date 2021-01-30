# Chapter 7. 중단 및 종료

* 자바에는 스레드가 작업을 실행하고 있을 때 강제로 멈추도록 하는 방법이 없다.
* 대신 인터럽트( 특정 스레드에게 작업을 멈춰 달라고 요청하는 형태 )를 사용할 수 있다.

> 실행 중이던 일을 중단할 때 작업을 진행하던 스레드가 직접 마무리하는 것이 가장 적절한 방법


# 7.1 작업 중단

* 실행 중인 작업을 취소하고자 하는 경우
  1. 사용자가 취소하기를 원하는 경우
  2. 시간이 제한된 작업
  3. 어플리케이션 이벤트
  4. 오류
  5. 종료

> 작업을 취소하는 기본적인 형태는 취소 요청을 확인하는 플래그를 사용하는 것이다.

### Listing 7.1 volatile 변수를 사용해 취소 상태를 확인
~~~java
@ThreadSafe
public class PrimeGenerator implements Runnable {
  @GuardedBy("this")
  private final List<BigInteger> primes = new ArrayList<BigInteger>();
  private volatile boolean cancelled;

  public void run() {
    BigInteger p = BigInteger.ONE;
    while (!cancelled) {
      p = p.nextProbablePrime();
      synchronized (this) {
        primes.add(p);
      }
    }
  }

  public void cancel() {
    cancelled = true;
  }

  public synchronized List<BigInteger> get() {
    return new ArrayList<BigInteger>(primes);
  }
}
~~~

### Listing 7.2 1초간 소수를 계산하는 프로그램
~~~java
List<BigInteger> aSecondOfPrimes() throws InterruptedException {
        PrimeGenerator generator = new PrimeGenerator();
        new Thread(generator).start();
        try {
            SECONDS.sleep(1);
        } finally {
            generator.cancel();
        }
        return generator.get();
}
~~~

> 작업을 쉽게 취소하려면 어떻게, 언제, 어떤 일을 해야 하는지에 대한 취소 정책을 명확히 정의해야 한다.

### Listing 7.3 프로듀서가 대기 중인 상태로 계속 멈춰 있을 가능성이 있는 안전하지 않은 취소 방법의 예, 이런 코드는 금물!

큐에 작업을 넣는 put() 이 소비하는 take() 보다 빠를 때, 큐가 가득찬 경우 put()은 블락될 것이다. 이 때, cancle()을 호출한다면 cancelled 값이 true로 매핑은 되겠지만 프로듀서는 put() 에 멈춰있고, Put()을 풀어줄 컨슈머가 더이상 작업하지 못하므로 canclled 값을 확인할 수 없다.

~~~java
class BrokenPrimeProducer extends Thread {
  private final BlockingQueue<BigInteger> queue;
  private volatile boolean cancelled = false;

  BrokenPrimeProducer(BlockingQueue<BigInteger> queue) {
    this.queue = queue;
  }

  public void run() {
    try {
      BigInteger p = BigInteger.ONE;
      while (!cancelled)
        queue.put(p = p.nextProbablePrime());
    } catch (InterruptedException consumed) {
    }
  }

  public void cancel() {
    cancelled = true;
  }
}

void consumePrimes() throws InterruptedException {
        BlockingQueue<BigInteger> primes = ...;
        BrokenPrimeProducer producer = new BrokenPrimeProducer(primes);
        producer.start();
        try {
            while (needMorePrimes()) consume(primes.take());
        } finally {
            producer.cancel();
        }
    }
~~~

> 작업을 중단하고자 하는 부분이 아닌 다른 부분에 인터럽트를 사용한다면 오류가 발생하기 쉽다.

### Listing 7.4 Thread 클래스의 인터럽트 관련 메소드
~~~java
public class Thread {
  public void interrupt() { ... }
  public boolean isInterrupted() { ... }
  public static boolean interrupted() { ... }
  ...
}
~~~

> 특정 스레드의 interrupt 메소드를 호출한다 해도 해당 스레드가 처리하던 작업을 멈추지 않는다. 단지 해당 스레드에게 인터럽트 요청이 있었다는 메시지를 전달할 뿐이다.

### Listing 7.5 인터럽트를 사용해 작업 취소
~~~java
class PrimeProducer extends Thread {
  private final BlockingQueue<BigInteger> queue;

  PrimeProducer(BlockingQueue<BigInteger> queue) {
    this.queue = queue;
  }

  public void run() {
    try {
      BigInteger p = BigInteger.ONE;
      while (!Thread.currentThread().isInterrupted())
        queue.put(p = p.nextProbablePrime());
    } catch (InterruptedException consumed) {
      /* Allow thread to exit */ }
  }

  public void cancel() {
    interrupt();
  }
}
~~~

* 인터럽트 상태를 확인하는 부분 2가지
  1. 큐의 Put() 메서드를 호출하는 부분
  2. 인터럽트 상태를 직접 확인하는 반복문의 조건 확인 부분

> 작업 취소 기능을 구현하고자 할 때는 인터럽트가 가장 적절한 방법이다.

### Listing 7.6 InterruptedException을 상위 메소드로 전달
~~~java
BlockingQueue<Task> queue;
 ...
public Task getNextTask() throws InterruptedException {
  return queue.take();
}
~~~

## 7.1.2 인터럽트 정책

* 단일 작업마다 해당 작업을 멈출 수 있는 취소 정책이 있는 것 처럼 스레드 역시 인터럽트 처리 정책이 있어야 한다.

## 7.1.3 인터럽트에 대한 반응
  1. 발생한 예외를 호출 스택의 상위 메소드로 전달
  2. Thread.currentThread().interrupt(); 인터럽트 상황을 알리기

### Listing 7.7 인터럽트 상태를 종료 직전에 복구 시키는 중단 불가능 작업
~~~java
public Task getNextTask(BlockingQueue<Taskgt;queue) {
        boolean interrupted = false;
        try {
            while (true) {
                try {
                    return queue.take();
                } catch (InterruptedException e) {
                    interrupted = true;
                    // 그냥 넘어가고 재시도
                }
            }
        } finally {
            if (interrupted) Thread.currentThread().interrupt();
        }
}
~~~

## 7.1.4 예제: 시간 지정 실행

### Listing 7.8 임시로 빌려 사용하는 스레드에 인터럽트 거는 방법, 이런 코드는 금물!
~~~java
private static final ScheduledExecutorService cancelExec = ...;
public static void timedRun(Runnable r,long timeout,TimeUnit unit){
        final Thread taskThread=Thread.currentThread();
        cancelExec.schedule(new Runnable(){
            public void run(){
                taskThread.interrupt();
            }
            },timeout,unit);
        r.run();
}
~~~

> 작업을 실행하는 스레드와 인터럽트를 요청하는 스레드를 구분하면 인터럽트를 거는 시점에 작업 내부의 상황을 전혀 알 수 없기 때문에 결과가 정상적이지 않을 수 있다.

### Listing 7.9 작업 실행 전용 스레드에 인터럽트 거는 방법
~~~java
public static void timedRun(final Runnable r,long timeout,TimeUnit unit)throws InterruptedException {
  class RethrowableTask implements Runnable {
    private volatile Throwable t;

    public void run() {
      try {
        r.run();
      } catch (Throwable t) {
        this.t = t;
      }
    }
    void rethrow() {
      if (t != null)
      throw launderThrowable(t);
    }
  }

  RethrowableTask task = new RethrowableTask();
  final Thread taskThread = new Thread(task);
  taskThread.start();
  cancelExec.schedule(new Runnable() {
    public void run() {
      taskThread.interrupt();
      }
    }, timeout, unit);
    taskThread.join(unit.toMillis(timeout));
    task.rethrow();
}
~~~

> 이 코드는 작업 스레드가 인터럽트에 반응하지 않더라도 지정된 시간이 지나면 발생한 예외가 있는지 확인하고 있다면 상위 메소드에게 던질 것이다. 따라서 위에서 발생하는 인터럽트 후에도(인터럽트 처리가 안되어있다면) 작업이 계속 실행되는 문제는 해결할 수 있다.

> 하지만 timedRun() 메소드가 리턴됐을 때, 정상적으로 스레드가 종료된 것인지 join 메소드에서 타임아웃이 걸린 것인지를 알 수 없다는 단점을 그대로 가지고 있다.

## 7.1.5 Future를 사용해 작업 중단

### Listing 7.10 Future를 사용해 작업 중단하기
~~~java
public static void timedRun(Runnable r, long timeout, TimeUnit unit) throws InterruptedException {
        Future<?> task = taskExec.submit(r);
        try {
            task.get(timeout, unit);
        } catch (TimeoutException e) {
            // finally 블록에서 작업이 중단될 것이다.
             } catch (ExecutionException e) {
            // 작업 내부에서 예외 상황 발생. 예외를 다시 던진다.
            throw launderThrowable(e.getCause());
        } finally {
            // 이미 종료됐다 하더라도 별다른 악영향은 없다.
            task.cancel(true); // 실행중이라면 인터럽트를 건다.
            }
}
~~~

> 특정 스레드의 인터럽트 정책을 잘 알고 있지 않은 상태라면 해당 스레드에 인터럽트를 걸어서는 안된다.

> Executor에서 생성하는 스레드는 인터럽트 발생 시 작업을 중단할 수 있는 인터럽트 정책을 사용한다.
> 따라서 future의 cancle() 메소드를 사용해라.

# 7.1.6 인터럽트에 응답하지 않는 블로킹 작업 다루기

* java.io 패키지의 동기적 소켓 I/O
  * InputStream의 read와 OutputStream의 write 메소드가 인터럽트에 반응하지 않도록 되어 있다
    * But 해당 스트림이 연결된 소켓을 직접 닫으면 SocketException이 발생한다.
* java.nio 패키지의 동기적 I/O
  * InterruptibleChannel 에서 대기하고 있는 스레드에 인터럽트를 걸면 ClosedByInterruptException이 발생하면서 해당 채널이 닫힌다.
* Selector를 사용한 비동기적 I/O
  * 스레드가 Selector 클래스의 select 메소드에서 대기 중인 경우 , close 메소드를 호출하면 ClosedSelectionException을 발생시키면서 즉시 리턴된다.
* 락 확보
  * Lock 인터페이스를 구현한 락클래스의 lockInterruptibly 메소드를 사용하면 락을 확보할 때까지 대기하면서 인터럽트에도 응답하도록 구현할 수 있다.

### Listing 7.11 interrupt 메소드를 오버라이드해 표준에 정의되어 있지 않은 작업 중단 방법을 구현
~~~java
public class ReaderThread extends Thread {
  private final Socket socket;
  private final InputStream in;

  public ReaderThread(Socket socket) throws IOException {
    this.socket = socket;
    this.in = socket.getInputStream();
  }

  public void interrupt() {
    try {
      socket.close();
    } catch (IOException ignored) {
    } finally {
      super.interrupt();
    }
  }

  public void run() {
    try {
      byte[] buf = new byte[BUFSZ];
      while (true) {
        int count = in.read(buf);
        if (count < 0)
          break;
        else if (count > 0)
          processBuffer(buf, count);
      }
    } catch (IOException e) {
      /* Allow thread to exit */ }
  }
}
~~~

### Listing 7.12 newTaskFor를 사용해 비표준적인 작업 중단 방법 적용

Future 클래스를 통해 SocketUsingTask의 작업을 중단하면 소켓이 닫히는 것은 물론 실행 중인 스레드 역시 인터럽트가 걸린다.

> 응답 속도를 떨어뜨리지 않으면서 인터럽트에 대응하는 블로킹 메소드를 안전하게 호출할 수 있을 뿐만 아니라, 대기 상태에 들어갈 수 있는 소켓 I/O 메소드와 같은 기능도 호출할 수 있다.

~~~java
public interface CancellableTask<T> extends Callable<T> {
  void cancel();

  RunnableFuture<T> newTask();
}

@ThreadSafe public class CancellingExecutor extends ThreadPoolExecutor {
  ...
  protected<T> RunnableFuture<T> newTaskFor(Callable<T> callable) {
    if (callable instanceof CancellableTask)
       return ((CancellableTask<T>) callable).newTask();
    else
      return super.newTaskFor(callable);
    }
}

public abstract class SocketUsingTask<T> implements CancellableTask<T> {
  @GuardedBy("this")
  private Socket socket;

  protected synchronized void setSocket(Socket s) {
    socket = s;
  }

  public synchronized void cancel() {
    try {
      if (socket != null)
        socket.close();
    } catch (IOException ignored) {
    }
  }

  public RunnableFuture<T> newTask() {
    return new FutureTask<T>(this) {
                    public boolean cancel(boolean mayInterruptIfRunning) {
                      try {
                        SocketUsingTask.this.cancel();
                      } finally {
                        return super.cancel(mayInterruptIfRunning);
                      }
                    }
                };
  }
}
~~~


# 7.2 스레드 기반 서비스 중단

### Listing 7.13 종료 기능이 구현되지 않은 프로듀서-컨슈머 패턴의 로그 서비스
~~~java
public class LogWriter {
  private final BlockingQueue<String> queue;
  private final LoggerThread logger;

  public LogWriter(Writer writer) {
    this.queue = new LinkedBlockingQueue<String>(CAPACITY);
    this.logger = new LoggerThread(writer);
  }

  public void start() {
    logger.start();
  }

  public void log(String msg) throws InterruptedException {
    queue.put(msg);
  }

  private class LoggerThread extends Thread {
    private final PrintWriter writer;
     ...
     public void run() {
       try {
         while (true)
         writer.println(queue.take());
        } catch(InterruptedException ignored) {

         } finally {
           writer.close();
          }
        }
      }
}
~~~

### Listing 7.14 로그 서비스에 종료 기능을 덧붙이지만 안정적이지 않은 방법
~~~java
public void log(String msg) throws InterruptedException {
  if (!shutdownRequested)
    queue.put(msg);
  else
    throw new IllegalStateException("logger is shut down");
}
~~~

### Listing 7.15 LogWriter에 추가한 안정적인 종료 방법
~~~java
public class LogService {
  private final BlockingQueue<String> queue;
  private final LoggerThread loggerThread;
  private final PrintWriter writer;
  @GuardedBy("this")
  private boolean isShutdown;
  @GuardedBy("this")
  private int reservations;

  public void start() {
    loggerThread.start();
  }

  public void stop() {
    synchronized (this) {
      isShutdown = true;
    }
    loggerThread.interrupt();
  }

  public void log(String msg) throws InterruptedException {
    synchronized (this) {
       if (isShutdown)
           throw new IllegalStateException(...);
        ++reservations;
      }
      queue.put(msg);
  }

  private class LoggerThread extends Thread {
    public void run() {
      try {
        while (true) {
          try {
            synchronized (this) {
              if (isShutdown && reservations == 0)
                break;
            }
            String msg = queue.take();
            synchronized (this) {
              --reservations;
            }
            writer.println(msg);
          } catch (InterruptedException e) {
            /* retry */ }
        }
      } finally {
        writer.close();
      }
    }
  }
}
~~~

### Listing 7.16 ExecutorService를 활용한 로그 서비스
~~~java
public class LogService {
    private final ExecutorService exec = newSingleThreadExecutor();     ...

    public void start() {
    }

    public void stop() throws InterruptedException {
        try {
            exec.shutdown();
            exec.awaitTermination(TIMEOUT, UNIT);
        } finally {
            writer.close();
        }
    }

    public void log(String msg) {
        try {
            exec.execute(new WriteTask(msg));
        } catch (RejectedExecutionException ignored) {
        }
    }
}
~~~

### Listing 7.17 독약 객체를 사용해 서비스 종료
~~~java
public class IndexingService {
    private static final File POISON = new File("");
    private final IndexerThread consumer = new IndexerThread();
    private final CrawlerThread producer = new CrawlerThread();
    private final BlockingQueue<File> queue;
    private final FileFilter fileFilter;
    private final File root;

    class CrawlerThread extends Thread { /* Listing 7.18 */
    }

    class IndexerThread extends Thread { /* Listing 7.19 */
    }

    public void start() {
        producer.start();
        consumer.start();
    }

    public void stop() {
        producer.interrupt();
    }

    public void awaitTermination() throws InterruptedException {
        consumer.join();
    }
}
~~~

### Listing 7.18 IndexingService의 프로듀서 스레드
~~~java

public class CrawlerThread extends Thread {
    public void run() {
        try {
            crawl(root);
        } catch (InterruptedException e) { /*  fall through  */ } finally {
            while (true) {
                try {
                    queue.put(POISON);
                    break;
                } catch (InterruptedException e1) { /*  retry  */ }
            }
        }
    }

    private void crawl(File root) throws InterruptedException {
        ...
    }
}
~~~

### Listing 7.19 IndexingService의 컨슈머 스레드
~~~java
public class IndexerThread extends Thread {
  public void run() {
    try {
      while (true) {
        File file = queue.take();
        if (file == POISON)
          break;
        else
          indexFile(file);
      }
    } catch (InterruptedException consumed) {
    }
  }
}
~~~

### Listing 7.20 메소드 내부에서 Executor를 사용하는 모습
~~~java
boolean checkMail(Set<String> hosts, long timeout, TimeUnit unit) throws InterruptedException {
        ExecutorService exec = Executors.newCachedThreadPool();
        final AtomicBoolean hasNewMail = new AtomicBoolean(false);
        try {
            for (final String host : hosts)
                exec.execute(new Runnable() {
                    public void run() {
                        if (checkMail(host)) hasNewMail.set(true);
                    }
                });
        } finally {
            exec.shutdown();
            exec.awaitTermination(timeout, unit);
        }
        return hasNewMail.get();
    }
~~~

### Listing 7.21 종료된 이후에도 실행이 중단된 작업이 어떤 것인지 알려주는 ExecutorService
~~~java
public class TrackingExecutor extends AbstractExecutorService {
    private final ExecutorService exec;
    private final Set<Runnable> tasksCancelledAtShutdown = Collections.synchronizedSet(new HashSet<Runnable>());     ...

    public List<Runnable> getCancelledTasks() {
        if (!exec.isTerminated()) throw new IllegalStateException(...);
        return new ArrayList<Runnable>(tasksCancelledAtShutdown);
    }

    public void execute(final Runnable runnable) {
        exec.execute(new Runnable() {
            public void run() {
                try {
                    runnable.run();
                } finally {
                    if (isShutdown() && Thread.currentThread().isInterrupted()) tasksCancelledAtShutdown.add(runnable);
                }
            }
        });
    }     // delegate other ExecutorService methods to exec
 }
~~~

### Listing 7.22 TrackingExecutorService를 사용해 중단된 작업을 나중에 사용할 수 있도록 보관하는 모습
~~~java
public abstract class WebCrawler {
    private volatile TrackingExecutor exec;
    @GuardedBy("this")
    private final Set<URL> urlsToCrawl = new HashSet<URL>();     ...

    public synchronized void start() {
        exec = new TrackingExecutor(Executors.newCachedThreadPool());
        for (URL url : urlsToCrawl) submitCrawlTask(url);
        urlsToCrawl.clear();
    }

    public synchronized void stop() throws InterruptedException {
        try {
            saveUncrawled(exec.shutdownNow());
            if (exec.awaitTermination(TIMEOUT, UNIT)) saveUncrawled(exec.getCancelledTasks());
        } finally {
            exec = null;
        }
    }

    protected abstract List<URL> processPage(URL url);

    private void saveUncrawled(List<Runnable> uncrawled) {
        for (Runnable task : uncrawled) urlsToCrawl.add(((CrawlTask) task).getPage());
    }

    private void submitCrawlTask(URL u) {
        exec.execute(new CrawlTask(u));
    }

    private class CrawlTask implements Runnable {
        private final URL url;         ...

        public void run() {
            for (URL link : processPage(url)) {
                if (Thread.currentThread().isInterrupted()) return;
                submitCrawlTask(link);
            }
        }

        public URL getPage() {
            return url;
        }
    }
}
~~~

### Listing 7.23 스레드 풀에서 사용하는 작업용 스레드의 일반적인 모습
~~~java
public void run() {
        Throwable thrown = null;
        try {
            while (!isInterrupted()) runTask(getTaskFromWorkQueue());
        } catch (Throwable e) {
            thrown = e;
        } finally {
            threadExited(this, thrown);
        }
}
~~~

### Listing 7.24 UncaughtExceptionHandler 인터페이스
~~~java
public interface UncaughtExceptionHandler {
  void uncaughtException(Thread t, Throwable e);
  }
~~~

### Listing 7.25 예외 내용을 로그 파일에 출력하는 UncaughtExceptionHandler
~~~java
public class UEHLogger implements Thread.UncaughtExceptionHandler {
  public void uncaughtException(Thread t, Throwable e) {
    Logger logger = Logger.getAnonymousLogger();
    logger.log(Level.SEVERE, "Thread terminated with exception: " + t.getName(), e);
  }
}
~~~

### Listing 7.26 로그 서비스를 종료하는 종료 훅을 등록
~~~java
public void start() {
        Runtime.getRuntime().addShutdownHook(new Thread() {
            public void run() {
                try {
                    LogService.this.stop();
                } catch (InterruptedException ignored) {
                }
            }
        });
    }
~~~