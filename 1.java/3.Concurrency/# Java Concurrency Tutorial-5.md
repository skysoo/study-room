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

synchronized collections은 모든 컬렉션에 대한 접근을 직렬화하여 Thread-safety를 달정한다.

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

## 5.3. Blocking Queues and the Producer-consumer Pattern

