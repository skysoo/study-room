# synchronized 적용 유형 4가지

```
## 1. instance 메소드
## 2. static 메소드
## 3. instance 메소드 코드 블록
## 4. static 메소드 코드 블록
```

동기화는 객체에 대한 동기화로 이루어지는데, 같은 객체에 대한 모든 동기화 블록은 한 시점에 오직 한 스레드만이 블록 안으로 접근하도록(실행하도록) 한다.

블록에 접근을 시도하는 다른 스레드들은 블록 안의 스레드가 실행을 마치고 블록을 벗어날 때까지 Blocked 상태가 된다.

## 1. instance 메소드
동기화는 synchronized 메소드를 가진 인스턴스(객체)를 기준으로 이루어진다.

```java
public synchronized void add(int value){
      this.count += value;
}
```

> 인스턴스 당 한 스레드를 가진다.


## 2. static 메소드
동기화는 synchronized 메소드를 가진 클래스를 기준으로 이루어진다.

JVM 내에 클래스 객체는 클래스 당 하나만 존재할 수 있으므로 같은 클래스에 대해서는 오직 한 스레드만 동기화된 static 메소드를 실행할 수 있다.

```java
public static synchronized void add(int value){
    this.count += value;
}
```

> 클래스 당 한 스레드를 가진다.

## 3. instance 메소드 코드 블록
메소드 전체에 대한 동기화가 아니라 특정 부분에 대한 동기화로 효율을 높일 수 있다.

단, 아래 코드는 동기화된 부분 이외의 작업을 하지 않으므로 위의 코드와 동일한 기능을 한다.

코드 블록 동기화는 하나의 객체를 전달 받는데 예제에서는 this(해당 메소드를 호출한 객체)인데, 이렇게 동기화 코드 블록으로 전달된 객체를 모니터 객체라고 한다.

this 객체는 한 시점에 아래 둘 중 하나의 코드만 실행할 수 있다.

```java
public class MyClass {

    public synchronized void log1(String msg1, String msg2){
        log.writeln(msg1);
        log.writeln(msg2);
    }

    public void log2(String msg1, String msg2){
        synchronized(this){
            log.writeln(msg1);
            log.writeln(msg2);
        }
    }
}
```
> 한 스레드는 한 시점에 두 동기화된 코드 중 하나만을 실행할 수 있다. 만약 log2()의 동기화 블록의 괄호에 this가 아닌 다른 객체를 전달한다면 스레드는 한 시점에 각 메소드를 실행할 수 있다. - 동기화 기준이 달라지므로

## 4. static 메소드 코드 블록


```java
 public class MyClass {

    public static synchronized void log1(String msg1, String msg2){
        log.writeln(msg1);
        log.writeln(msg2);
    }

    public static void log2(String msg1, String msg2){
        synchronized(MyClass.class){
            log.writeln(msg1);
            log.writeln(msg2);  
        }
    }
}
```

> 한 시점에 오직 한 스레드만 둘 중 하나의 코드를 실행할 수 있다. 


## 5. 예제
아래 예제1은 두개의 스레드가 생성되었지만 인스턴스인 counter 를 기준으로 동기화 될 것이다. 따라서 각 스레드는 add() 메소드 수행에 제약을 받는다. 한 스레드가 작업시 다른 스레드는 대기한다.

예제2는 두개의 스레드가 생성되었고 인스턴스가 다르기 때문에 각 스레드는 add() 수행에 제약 받지 않는다.

#### 5-1. 예제1
```java
public class Counter{
     
    long count = 0;
    
    public synchronized void add(long value){
       this.count += value;
    }
}

public class CounterThread extends Thread{

    protected Counter counter = null;

    public CounterThread(Counter counter){
        this.counter = counter;
    }

    public void run() {
        for(int i=0; i<10; i++){
            counter.add(i);
            }
    }
}

public class Example {

    public static void main(String[] args){
        Counter counter = new Counter();
        Thread  threadA = new CounterThread(counter);
        Thread  threadB = new CounterThread(counter);

        threadA.start();
        threadB.start(); 
    }
}
```

#### 5-2. 예제2
```java
public class Example {

    public static void main(String[] args){
        Counter counterA = new Counter();
        Counter counterB = new Counter();
        Thread  threadA = new CounterThread(counterA);
        Thread  threadB = new CounterThread(counterB);

        threadA.start();
        threadB.start(); 
    }
}
```