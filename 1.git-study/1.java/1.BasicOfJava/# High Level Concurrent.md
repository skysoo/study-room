# High Level Concurrent

# 1. Java5

* ExecutorService
  * newFixedThreadPool - ExecutorService의 구현체 (팩토리 메소드)
    * 내부적으로는 new ThreadPoolExecutor()를 사용한다.

~~~java
ExecutorService exeuctorService = Executors.newFixedThreadPool(n);

Future<T> task = executorService.submit(()->{
  T t = null;
  /*
  * logic 작성
  */
  return t;
});

T result = task.get();

exeuctorService.shutdown();
~~~

# 2. Java7
* ForkJoinPool
    * Recursive~ 를 구현해야 한다.
      1. RecursiveTask - return 값이 존재함
      2. RecursiveAction - return 값이 없음

~~~java
public class SimpleForkJoinTask {
    public static void main(String[] args) {
        int nThreads = Runtime.getRuntime().availableProcessors();
        System.out.println("가용한 스레드 수 : "+nThreads);

        int[] numbers = new int[1000];

        for (int i=0;i<numbers.length;i++){
            numbers[i] = i;
        }

        ForkJoinPool forkJoinPool = new ForkJoinPool(nThreads);
        Long result = forkJoinPool.invoke(new Sum(0, numbers.length, numbers));
        System.out.println(result);
    }

    static class Sum extends RecursiveTask<Long>{
        int low;
        int high;
        int[] array;

        public Sum(int low, int high, int[] array) {
            this.low = low;
            this.high = high;
            this.array = array;
        }

        @Override
        protected Long compute() {
            if (high-low<=10){
                long sum = 0;
                for(int i=low;i<high;++i){
                    sum += array[i];
                }

                return sum;
            } else {
                int mid = low + (high - low) / 2;
                Sum left = new Sum(low,mid,array);
                Sum right = new Sum(mid,high,array);
                left.fork();
                long rightResult = right.compute();
                long leftResult = left.join();

                return leftResult + rightResult;
            }
        }
    }
}

~~~


# 3. Java8

* WorkStealingPool
  * ExecutorService의 WorkStealingPool은 ForkJoinPool의 Recursive~ 를 직접 구현하지 않고도 ForkJoinPool을 사용할 수 있게 해준다.
~~~java
ExecutorService exeuctorService = new WorkStealingPool(n);

Future<T> task = executorService.submit(()->{
  T t = null;
  /*
  * logic 작성
  */
  return t;
});

T result = task.get();

exeuctorService.shutdown();
~~~

* CompletableFuture
  * Future로는 구현할 수 없는 복작한 로직의 비동기 앱을 만들수 있다.
    1. 두개 이상의 순서가 필요한 비동기 작업을 파이프 라인으로 만들기
    2. 두개 이상의 비동기 작업 결과를 합치기
    3. Thread 내부 에러 코드 반환
    4. 간결한 코드로 가독성 향상

~~~java
public class CompletableFutureTask {
    private static List<Integer> numList = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
    private static List<Integer> urlList = Arrays.asList(10, 20, 30, 40, 50);

    public static void main(String[] args) throws ExecutionException, InterruptedException {
        int nThreads = Runtime.getRuntime().availableProcessors();
        System.out.println("가용한 스레드 수 : " + nThreads);

        ExecutorService executorService = Executors.newFixedThreadPool(2);
        CompletableFuture<Map<Integer, List<String>>> completableFuture = new CompletableFuture<>();

        Map<Integer, List<String>> resultMap = Maps.newConcurrentMap();
        for (int num : numList) {
            completableFuture = CompletableFuture.supplyAsync(() -> {
                List<String> urls = Lists.newArrayList();
                for (int url : urlList) {
                    String urlStr = getUrl(url);
                    urls.add(urlStr);
                }
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                resultMap.put(num, urls);

                return resultMap;
            }, executorService).exceptionally(throwable -> {
                log.error("실패에 대한 로그", throwable);
                throw new RuntimeException();
            });
        }
        Map<Integer, List<String>> integerListMap = completableFuture.get();
        System.out.println("map size : " + integerListMap.size());
        integerListMap.forEach((n, lists) -> {
            System.out.println("key : " + n + " value : " + Arrays.toString(lists.toArray()));
        });
        executorService.shutdown();
    }

    public static String getUrl(int num) {
        return "http://192.168.10." + num;
    }
}
~~~