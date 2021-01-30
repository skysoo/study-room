# Chapter 6. 작업 실행

# 6.1 스레드에서 작업 실행

1. 작업은 다른 작업의 상태, 결과, 부수 효과 등에 영향을 받지 않아야 한다.
2. 스케줄링 or Load Balancing을 하려면 유연성을 가져야하는데, 각 작업이 전체 업무 중 충분히 작은 부분을 담당해야 한다.

* 가장 간단한 작업 단위는 클라이언트의 요청 하나를 작업 하나로 보는 것


### Listing 6.1 순차적으로 처리하는 웹서버
~~~java
class SingleThreadWebServer {
  public static void main(String[] args) throws IOException {
    ServerSocket socket = new ServerSocket(80);
    while (true) {
      Socket connection = socket.accept();
      handleRequest(connection);
    }
  }
}
~~~

> 단일 스레드 작업에서는 연산을 기다려야하므로 성능 저하가 동반된다.


### Listing 6.2 요청이 들어올 때마다 스레드를 생성하는 웹서버
~~~java
class ThreadPerTaskWebServer {
  public static void main(String[] args) throws IOException {
    ServerSocket socket = new ServerSocket(80);
    while (true) {
      final Socket connection = socket.accept();
      Runnable task = new Runnable() {
        public void run() {
          handleRequest(connection);
        }
      };
      new Thread(task).start();
    }
  }
}
~~~

> 작업이 들어올 때마다 스레드를 만드므로 속도 향상 및 부하 저하 등 성능이 좋아질 수 있다.

> 하지만 대량의 스레드 생성시 아래와 같은 문제 발생
1. 스레드 라이프 사이클 문제 - 생성하고 제거하는 작업에도 자원이 소모된다.
2. 자원 낭비 - 실행중인 스레드는 메모리를 많이 소모하고 cpu 사용을 위해 경쟁
3. 안정성 문제 - OutOfMemory 발생

> 따라서 시스템이 처리할 수 있는 스레드 수를 어플리케이션에서 제한하는 방법을 사용해야 한다.

# 6.2 Executor 프레임웍

### Listing 6.3 Executor 인터페이스
~~~java
public interface Executor {
  void execute(Runnable command);
}
~~~

> Executor는 작업 등록과 작업 실행을 분리하는 표준적인 방법, 각 작업은 Runnable의 형태로 정의한다.

### Listing 6.4 스레드 풀을 사용한 웹서버
~~~java
class TaskExecutionWebServer {
  private static final int NTHREADS = 100;
  private static final Executor exec = Executors.newFixedThreadPool(NTHREADS);

  public static void main(String[] args) throws IOException {
    ServerSocket socket = new ServerSocket(80);
    while (true) {
      final Socket connection = socket.accept();
      Runnable task = new Runnable() {
        public void run() {
          handleRequest(connection);
        }
      };
      exec.execute(task);
    }
  }
}
~~~

### Listing 6.5 작업마다 스레드를 새로 생성시키는 Executor
~~~java
public class ThreadPerTaskExecutor implements Executor {
  public void execute(Runnable r) {
    new Thread(r).start();
  };
}
~~~

### Listing 6.6 작업을 등록한 스레드에서 직접 동작시키는 Executor
~~~java
public class WithinThreadExecutor implements Executor {
  public void execute(Runnable r) {
    r.run();
  };
}
~~~

* 실행 정책 (일종의 자원 관리 도구)
1. 작업을 어느 스레드에서 실행할 것인가?
2. 작업을 어떤 순서로 실행할 것인가?
3. 동시에 몇 개의 작업을 병렬로 실행할 것인가?
4. 최대 몇 개까지의 작업이 큐에서 실행을 대기할 수 있게 할 것인가?
5. 시스템에 부하가 많이 걸려서 작업을 거절해야 하는 경우, 어떤 작업을 희생양으로 삼아햐 할 것이며, 작업을 요청한 프로그램에 어떻게 알려야 할 것인가?
6. 작업을 실행하기 직전이나 실행한 직후에 어떤 동작이 있어야 하는가?

* 스레드 풀을 사용할 때 장점
1. 스레드 재사용 (자원 효율적 사용)
2. 작업 처리 반응 속도 향상
3. 메모리를 전부 소모하거나 한정된 자원을 두고 경쟁하느라 성능을 낮추는 현상도 없앤다

* 스레드 풀 종류
1. newFixedThreadPool - 최대 스레드 수 제한
2. newCachedThreadPool - 필요할 때 스레드를 생성하고, 필요없을 때 종료 시킨다. 수 제한이 없다.
3. newSingleThreadExecutor - 단일 스레드이며, 비정상 종료시 새로운 스레드를 다시 생성한다.
4. newScheduledThreadPool - 일정 시간 이후나 주기적으로 작업을 실행할 수 있으면 스레드 수가 고정적이다.

> 작업별로 스레드를 생성하는 전략보다 풀을 기반으로 하는 스레드 생성 전략이 안정성 측면에서 훨씬 좋다.



### Listing 6.7 ExecutorService 인터페이스의 동작 주기 관리
~~~java
public interface ExecutorService extends Executor {
  void shutdown();

  List<Runnable> shutdownNow();

  boolean isShutdown();

  boolean isTerminated();

  boolean awaitTermination(long timeout, TimeUnit unit) throws InterruptedException;
  // ... additional convenience methods for task submission
}
~~~

### Listing 6.8 종료 기능을 추가한 웹서버
~~~java
class LifecycleWebServer {
  private final ExecutorService exec = ...;

  public void start() throws IOException {
    ServerSocket socket = new ServerSocket(80);
    while (!exec.isShutdown()) {
      try {
        final Socket conn = socket.accept();
        exec.execute(new Runnable() {
          public void run() {
            handleRequest(conn);
          }
        });
      } catch (RejectedExecutionException e) {
        if (!exec.isShutdown())
          log("task submission rejected", e);
      }
    }
  }

  public void stop() {
    exec.shutdown();
  }

  void handleRequest(Socket connection) {
    Request req = readRequest(connection);
    if (isShutdownRequest(req))
      stop();
    else
      dispatchRequest(req);
  }
}
~~~

> 특정 주기를 사용해야 하는 Thread 라면 Timer 클래스보다 ScheduledThreadPoolExecutor를 사용해라.

### Listing 6.9 Timer를 사용할 때 발생할 수 있는 오류 상황
~~~java
public class OutOfTime {
  public static void main(String[] args) throws Exception {
    Timer timer = new Timer();
    timer.schedule(new ThrowTask(), 1);
    SECONDS.sleep(1);
    timer.schedule(new ThrowTask(), 1);
    SECONDS.sleep(5);
  }

  static class ThrowTask extends TimerTask {
    public void run() {
      throw new RuntimeException();
    }
  }
}
~~~

* DelayQueue
=> BlockingQueue + ScheduledThreadPoolExecutor 기능을 하며, 내부적으로는 여러 개의 Delayed 객체가 있으며 각각 저마다의 시간을 가진다. 그리고 시간이 만료된 객체만 take() 할 수 있고 객체 마다의 시간 순서로 정렬되어 뽑아진다.


# 6.3 병렬로 처리할 만한 작업

### Listing 6.10 페이지 내용을 순차적으로 렌더링
~~~java
public class SingleThreadRenderer {
  void renderPage(CharSequence source) {
    renderText(source);
    List<ImageData> imageData = new ArrayList<ImageData>();
    for (ImageInfo imageInfo : scanForImageInfo(source))
      imageData.add(imageInfo.downloadImage());
    for (ImageData data : imageData)
      renderImage(data);
  }
}
~~~


### Listing 6.11 Callable과 Future 인터페이스
~~~java
public interface Callable<V> {
  V call() throws Exception;
}

public interface Future<V> {
  boolean cancel(boolean mayInterruptIfRunning);

  boolean isCancelled();

  boolean isDone();

  V get() throws InterruptedException, ExecutionException, CancellationException;

  V get(long timeout, TimeUnit unit)
      throws InterruptedException, ExecutionException, CancellationException, TimeoutException;
}
~~~

### Listing 6.12 ThreadPoolExecutor.newTaskFor 메소드의 기본 구현 내용
~~~java
protected <T> RunnableFuture<T> newTaskFor(Callable<T> task) {
  return new FutureTask<T>(task);
}
~~~
### Listing 6.13 Future를 사용해 이미지 파일 다운로드 작업을 기다림
~~~java
public class FutureRenderer {
  private final ExecutorService executor = ...;

  void renderPage(CharSequence source) {
    final List<ImageInfo> imageInfos = scanForImageInfo(source);
    Callable<List<ImageData>> task = new Callable<List<ImageData>>() {
      public List<ImageData> call() {
        List<ImageData> result = new ArrayList<ImageData>();
        for (ImageInfo imageInfo : imageInfos)
          result.add(imageInfo.downloadImage());
        return result;
      }
    };
    Future<List<ImageData>> future = executor.submit(task);
    renderText(source);
    try {
      List<ImageData> imageData = future.get();
      for (ImageData data : imageData)
        renderImage(data);
    } catch (InterruptedException e) {
      // Re-assert the thread's interrupted status
      Thread.currentThread().interrupt();
      // We don't need the result, so cancel the task too
      future.cancel(true);
    } catch (ExecutionException e) {
      throw launderThrowable(e.getCause());
    }
  }
}
~~~
### Listing 6.14 ExecutorCompletionService에서 사용하는 QueueingFuture 클래스
~~~java
private class QueueingFuture<V> extends FutureTask<V> {
  QueueingFuture(Callable<V> c) {
    super(c);
  }

  QueueingFuture(Runnable t, V r) {
    super(t, r);
  }

  protected void done() {
    completionQueue.add(this);
  }
}
~~~

> ExecutorCompletionService = BlockingQueue + Executor 의 기능을 합쳐놓은 것

### Listing 6.15 CompletionService를 사용해 페이지 구성 요소를 받아오는 즉시 렌더링

~~~java
public class Renderer {
  private final ExecutorService executor;

  Renderer(ExecutorService executor) {
    this.executor = executor;
  }

  void renderPage(CharSequence source) {
    final List<ImageInfo> info = scanForImageInfo(source);
    CompletionService<ImageData> completionService = new ExecutorCompletionService<ImageData>(executor);
    for (final ImageInfo imageInfo : info)
      completionService.submit(new Callable<ImageData>() {
        public ImageData call() {
          return imageInfo.downloadImage();
        }
      });
    renderText(source);
    try {
      for (int t = 0, n = info.size(); t < n; t++) {
        Future<ImageData> f = completionService.take();
        ImageData imageData = f.get();
        renderImage(imageData);
      }
    } catch (InterruptedException e) {
      Thread.currentThread().interrupt();
    } catch (ExecutionException e) {
      throw launderThrowable(e.getCause());
    }
  }
}
~~~

> CompletionService를 잘 활용하면 전체 실행 시간을 줄이고, 응답 속도를 개선할 수 있다.

### Listing 6.16 제한된 시간 안에 광고 가져오기
~~~java
Page renderPageWithAd() throws InterruptedException {
  long endNanos = System.nanoTime() + TIME_BUDGET;
  Future<Ad> f = exec.submit(new FetchAdTask());
  // Render the page while waiting for the ad
  Page page = renderPageBody();
  Ad ad;
  try {
   // Only wait for the remaining time budget
   long timeLeft = endNanos - System.nanoTime();
   ad = f.get(timeLeft, NANOSECONDS);
  } catch (ExecutionException e) {
    ad = DEFAULT_AD;
  } catch (TimeoutException e) {
    ad = DEFAULT_AD;
    f.cancel(true);
  }
   page.setAd(ad);
   return page;
  }
~~~

> future를 get할 때, time을 줄 수 있다. 제한 시간안에 가져오지 못했을 때 작업을 취소하고 특정 액션을 취할 수 있다.

> N개의 작업마다 Future 객체를 확보하고 타임아웃을 지정한 get()으로 각 처리 결과를 가져오도록 할 수 있다. 이런 작업을 쉽게해주는 것이 invokeAll() 이다.


### Listing 6.17 제한된 시간 안에 여행 관련 입찰 정보를 가져오도록 요청하는 코드
~~~java
private class QuoteTask implements Callable<TravelQuote> {
  private final TravelCompany company;
  private final TravelInfo travelInfo;
  ...

    public TravelQuote call() throws Exception {
      return company.solicitQuote(travelInfo);
    }
  }

  public List<TravelQuote> getRankedTravelQuotes(TravelInfo travelInfo, Set<TravelCompany> companies, Comparator<TravelQuote> ranking, long time, TimeUnit unit)  throws InterruptedException {

    List<QuoteTask> tasks = new ArrayList<QuoteTask>();

    for (TravelCompany company : companies)
      tasks.add(new QuoteTask(company, travelInfo));

    List<Future<TravelQuote>> futures =  exec.invokeAll(tasks, time, unit);
    List<TravelQuote> quotes = new ArrayList<TravelQuote>(tasks.size());

    Iterator<QuoteTask> taskIter = tasks.iterator();

    for (Future<TravelQuote> f : futures) {
      QuoteTask task = taskIter.next();
      try {
        quotes.add(f.get());
       } catch (ExecutionException e) {
         quotes.add(task.getFailureQuote(e.getCause()));
        } catch (CancellationException e) {
          quotes.add(task.getTimeoutQuote(e));
        }
    }
       Collections.sort(quotes, ranking);
       return quotes;
      }
~~~


# 정리

# 6.1 스레드에서 작업 실행
1. 단일 스레드 작업은 느리다.
2. 스레드별로 작업을 생성하는 것은 장단점이 있다.
   * 장점
     1. 작업이 들어올 때마다 스레드를 만드므로 속도 향상 및 부하 저하 등 성능이 좋아질 수 있다.
     2. 하지만 대량의 스레드 생성시 아래와 같은 문제 발생
   * 단점
    1. 스레드 라이프 사이클 문제 - 생성하고 제거하는 작업에도 자원이 소모된다.
    2. 자원 낭비 - 실행중인 스레드는 메모리를 많이 소모하고 cpu 사용을 위해 경쟁
    3. 안정성 문제 - OutOfMemory 발생


# 6.2 Executor 프레임웍

> Executor는 작업 등록과 작업 실행을 분리하는 표준적인 방법, 각 작업은 Runnable의 형태로 정의한다.

* 스레드 풀을 사용할 때 장점
1. 스레드 재사용 (자원 효율적 사용)
2. 작업 처리 반응 속도 향상
3. 메모리를 전부 소모하거나 한정된 자원을 두고 경쟁하느라 성능을 낮추는 현상도 없앤다

* 스레드 풀 종류
1. newFixedThreadPool - 최대 스레드 수 제한
2. newCachedThreadPool - 필요할 때 스레드를 생성하고, 필요없을 때 종료 시킨다. 수 제한이 없다.
3. newSingleThreadExecutor - 단일 스레드이며, 비정상 종료시 새로운 스레드를 다시 생성한다.
4. newScheduledThreadPool - 일정 시간 이후나 주기적으로 작업을 실행할 수 있으면 스레드 수가 고정적이다.

> 작업별로 스레드를 생성하는 전략보다 풀을 기반으로 하는 스레드 생성 전략이 안정성 측면에서 훨씬 좋다.

 * 특정 주기를 사용해야 하는 Thread 라면 Timer 클래스보다 ScheduledThreadPoolExecutor를 사용해라.

* DelayQueue
=> BlockingQueue + ScheduledThreadPoolExecutor 기능을 하며, 내부적으로는 여러 개의 Delayed 객체가 있으며 각각 저마다의 시간을 가진다. 그리고 시간이 만료된 객체만 take() 할 수 있고 객체 마다의 시간 순서로 정렬되어 뽑아진다.


# 6.3 병렬로 처리할 만한 작업

> future를 get할 때, time을 줄 수 있다. 제한 시간안에 가져오지 못했을 때 작업을 취소하고 특정 액션을 취할 수 있다.

> N개의 작업마다 Future 객체를 확보하고 타임아웃을 지정한 get()으로 각 처리 결과를 가져오도록 할 수 있다. 이런 작업을 쉽게해주는 것이 invokeAll() 이다.