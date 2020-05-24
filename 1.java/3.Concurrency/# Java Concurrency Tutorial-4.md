<<<<<<< HEAD
[Chapter 4. Composing Objects](#chapter-4-composing-objects)
- [Chapter 4. Composing Objects](#chapter-4-composing-objects)
- [4.1. Designing a Thread-safe Class, Thread-safe 클래스 디자인하기](#41-designing-a-thread-safe-class-thread-safe-%ed%81%b4%eb%9e%98%ec%8a%a4-%eb%94%94%ec%9e%90%ec%9d%b8%ed%95%98%ea%b8%b0)
  - [4.1.1. Gathering Synchronization Requirements](#411-gathering-synchronization-requirements)
  - [4.1.2. State dependent Operations](#412-state-dependent-operations)
  - [4.1.3. State Ownership](#413-state-ownership)
- [4.2 Instance Confinement, 인스턴스 제한](#42-instance-confinement-%ec%9d%b8%ec%8a%a4%ed%84%b4%ec%8a%a4-%ec%a0%9c%ed%95%9c)
  - [4.2.1. The Java Monitor Pattern](#421-the-java-monitor-pattern)
  - [4.2.2. Example: Tracking Fleet Vehicles](#422-example-tracking-fleet-vehicles)
- [4.3. Delegating Thread Safety](#43-delegating-thread-safety)
  - [4.3.1. Example: Vehicle Tracker Using Delegation , 위임(Delegation)을 사용](#431-example-vehicle-tracker-using-delegation--%ec%9c%84%ec%9e%84delegation%ec%9d%84-%ec%82%ac%ec%9a%a9)
        - [DelegatingVehicleTracker-class](#delegatingvehicletracker-class)
  - [4.3.2. Independent State Variables](#432-independent-state-variables)
        - [VisualComponent-class](#visualcomponent-class)
  - [4.3.3. When Delegation Fails](#433-when-delegation-fails)
  - [4.3.4. Publishing Underlying State Variables](#434-publishing-underlying-state-variables)
  - [4.3.5. Example: Vehicle Tracker that Publishes Its State](#435-example-vehicle-tracker-that-publishes-its-state)
- [4.4 Adding Functionality to Existing Thread-safe Classes, Thread-safe 클래스에 기능 추가](#44-adding-functionality-to-existing-thread-safe-classes-thread-safe-%ed%81%b4%eb%9e%98%ec%8a%a4%ec%97%90-%ea%b8%b0%eb%8a%a5-%ec%b6%94%ea%b0%80)
  - [4.4.1. Client-side Locking](#441-client-side-locking)
  - [4.4.2. Composition](#442-composition)
- [4.5 Documenting Synchronization Policies](#45-documenting-synchronization-policies)

# Chapter 4. Composing Objects

# 4.1. Designing a Thread-safe Class, Thread-safe 클래스 디자인하기

public static 필드에 모든 상태를 저장하는 Thread-safe 프로그램을 작성할 수 있지만 Thread 상태를 안전하게 유지하는 것은 더욱 어렵다.

캡슐화를 통해 전체 프로그램을 검사하지 않고도 클래스가 스레드로부터 안전하다고 판단 할 수 있다.


> Thread-safe 클래스를 설계하려면 다음의 3가지 기본 요소가 포함되어야 한다.
  + 객체안의 변수를 확인해라.
  + 상태값을 가지는 변수의 생성을 제한해라.
  + 객체에 동시적으로 접근하는 것에 대한 정책을 수립해라.

~~~java
@ThreadSafe
public final class Counter {
    @GuardedBy("this")  private long value = 0;

    public synchronized  long getValue() {
        return value;
    }

    public  synchronized  long increment() {
         if (value == Long.MAX_VALUE)
             throw new IllegalStateException("counter overflow");
         return ++value;
    }
}
~~~

value 변수에 대해 synchronized가 정의되었으므로 Thread-safety 하다.


## 4.1.1. Gathering Synchronization Requirements

Thread-safety한 클래스라는 것은 클래스내 변수가 동시 접근 상태에서의 안전을 보장한다는 것이다.

객체와 변수는 상태 공간이라는 것을 가진다. 이 상태 공간이 작을수록 추론하기가 쉽다.

가능한 경우 final로 선언하면 상태를 더 간단하게 추론할 수 있다.

많은 클래스에는 특정 상태를 유효한 것으로 식별하는 유형이 있다.

위의 예제 Counter 클래스에서 변수 value의 길이는 long타입으로 그 길이는 Long.MIN_VALUE에서 Long.MAX_VALUE까지로 유효한 값으로 식별한다.

또한 특정 상태 전이를 유효하지 않은 것으로 식별하는 사후 조건이 있을 수 있다.

Counter 클래스에서 value의 현재 값이 17인 경우 유효한 다음 상태는 18뿐이다.

> 객체의 immutable 및 post conditions을 이해하지 못하면 Thread-safety를 보장할 수 없다.
> 상태 변수에 대한 (유효한 값 또는 상태 전이) 제약 조건은 원자성 및 캡슐화 요구 사항을 만든다.


## 4.1.2. State dependent Operations

일부 객체에는 상태 기반 전제 조건이 있는 메소드들이 있다. 예를 들어 비어있는 큐의 항목을 제거할 수는 없다. 요소를 제거하려면 큐가 "비어 있지 않은" 상태여야 한다.

동시 프로그램에서는 다른 스레드의 동작으로 인해 상태 기반 전제 조건들이 변경될 수 있다. 따라서 작업을 처리할 수 있는 상태가 될 때까지 효율적으로 대기하기 위한 고유 잠금(intrinsic locking)과 같은 내장 메커니즘을 사용해야 한다. 이러한 작업은 BlockingQueue, Semaphore 및 기타 Block 라이브러리 클래스로 쉽게 구현할 수 있다.

## 4.1.3. State Ownership



# 4.2 Instance Confinement, 인스턴스 제한

객체 내에 데이터를 캡슐화하면 객체의 메서드에 대한 데이터 접근이 제한되므로 적절한 lock을 유지한 상태에서 데이터에 항상 접근할 수 있다.

> Instance Confinement 객체는 의도한 범위를 벗어나면 안되는 것을 의미한다.

~~~java
@ThreadSafe
public class PersonSet {
    @GuardedBy("this")
    private final Set<Person> mySet = new HashSet<Person>();

    public synchronized void addPerson(Person p) {
       mySet.add(p);
    }
    public synchronized boolean containsPerson(Person p) {
      return mySet.contains(p);
    }
}
~~~

위 코드는 Instance Confinement 및 lock이 함께 작동하여 클래스 스레드를 안전하게 만드는 방법을 보여준다.

HashSet 자체는 스레드로부터 안전하지 않지만 mySet은 private 타입이며 PersonSet 객체를 탈출할 수 없다. mySet에 접근할 수 있는 유일한 경로는 addPerson 및 containsPerson이며, 이들 각각은 PersonSet에 대한 synchronized를 가지므로 모든 상태는 instrinsic lock으로 보호되어 PersonSet 객체를 Thread-safe 하게 만든다.

> Confinement 클래스는 전체 프로그램을 검사하지 않고도 Thread-safe에 대해 분석할 수 있기 때문에 보다 쉽게 Thread-safety한 프로그램을 작성할 수 있게 만든다.


## 4.2.1. The Java Monitor Pattern

Instance Confinement 원칙을 따라서 java 코드를 짜면 Java 모니터 패턴으로 연결이 된다.

Java 모니터 패턴이란 모든 변경 가능한 상태를 캡슐화하고 객체 자체의 고유 잠금으로 보호하는 것을 뜻한다.

~~~java
public class PrivateLock {
    private final Object myLock = new Object();

    @GuardedBy("myLock") Widget widget;
    void someMethod() {
        synchronized(myLock) {
        // Access or modify the state of widget
        }
    }
}
~~~


## 4.2.2. Example: Tracking Fleet Vehicles

~~~java
Map<String, Point> locations = vehicles.getLocations();

for (String key : locations.keySet())
   renderVehicle(key, locations.get(key));

void vehicleMoved(VehicleMovedEvent evt) {
    Point loc = evt.getNewLocation();
    vehicles.setLocation(evt.getVehicleId(), loc.x, loc.y);
}
~~~

MonitorVehicleTracker 클래스는 차량 위치를 표시하기 위해 MutablePoint 클래스를 사용하여 차량 추적기를 구현한 것이다.

MutablePoint 클래스가 스레드로부터 안전하지 않더라도 MonitorVehicleTracker 클래스는 안전하다.

~~~java
@ThreadSafe
public class MonitorVehicleTracker {
    @GuardedBy("this")
    private final Map<String, MutablePoint> locations;

    public MonitorVehicleTracker(Map<String, MutablePoint> locations) {
        this.locations = deepCopy(locations);
    }
    public synchronized Map<String, MutablePoint> getLocations() {
        return deepCopy(locations);
    }
    public synchronized MutablePoint getLocation(String id) {
           MutablePoint loc = locations.get(id);
        return loc == null ? null : new MutablePoint(loc);
    }
    public synchronized void setLocation(String id, int x, int y) {
        MutablePoint loc = locations.get(id);

        if (loc == null)
            throw new IllegalArgumentException("No such ID: " + id);

        loc.x = x;
        loc.y = y;
    }
    private static Map<String, MutablePoint> deepCopy(Map<String, MutablePoint> m) {
        Map<String, MutablePoint> result = new HashMap<String, MutablePoint>();

        for (String id : m.keySet())
            result.put(id, new MutablePoint(m.get(id)));

        return Collections.unmodifiableMap(result);
    }
}
public class MutablePoint { /* Listing 4.5 */ }
~~~

deepCopy 객체에 Map<String,MutablePoint> 인 locations를 넘기는데 굳이 result로 옮겨 담는 이유는?
=> 중복 데이터 저장을 막기위해서? 동시 스레드 접근할 때 thread-safe 하기 위해서

~~~java
@NotThreadSafe
public class MutablePoint {
    public int x, y;
    public MutablePoint() { x = 0; y = 0; }
    public MutablePoint(MutablePoint p) {
        this.x = p.x;
        this.y = p.y;
    }
}
~~~

# 4.3. Delegating Thread Safety

## 4.3.1. Example: Vehicle Tracker Using Delegation , 위임(Delegation)을 사용

MonitorVehicleTracker 클래스와 달리 위치 정보를 Thread-safety한 클래스에 위임하는 차량 추적기를 구현해보자.

HashMap 대신 ConcurrentHashMap을 사용하고, MutablePoint 대신 ImmutablePoint 클래스를 사용하자.

~~~java
@Immutable
public class Point {
    public final int x, y;
    public Point(int x, int y) {
        this.x = x;
        this.y = y;
    }
}
~~~

> Point는 immutable 이므로 thread로 부터 안전하다.

더이상 위치를 반환할 때 위치를 복사할 필요가 없다. 아래 DelegatingVehicleTracker 클래스는 명시적인 동기화를 사용하지 않는다.

상태에 대한 모든 접근은 ConcurrentHashMap에 의해 관리되며 맵의 모든 키와 값은 변경할 수 없다.

##### DelegatingVehicleTracker-class
~~~java
@ThreadSafe
public class DelegatingVehicleTracker {
    private final ConcurrentMap<String, Point> locations;
    private final Map<String, Point> unmodifiableMap;

    public DelegatingVehicleTracker(Map<String, Point> points) {
        locations = new ConcurrentHashMap<String, Point>(points);
        unmodifiableMap = Collections.unmodifiableMap(locations);
    }
    public Map<String, Point> getLocations() {
        return unmodifiableMap;
    }
    public Point getLocation(String id) {
        return locations.get(id);
    }
    public void setLocation(String id, int x, int y) {
        if (locations.replace(id, new Point(x, y)) == null)
            throw new IllegalArgumentException("invalid vehicle name: " + id);
    }
}
~~~

~~~java
public Map<String, Point> getLocations() {
    return Collections.unmodifiableMap(new HashMap<String, Point>(locations));
}
~~~

## 4.3.2. Independent State Variables

복합 클래스가 여러 상태 변수와 관련하여 불변을 강요하지 않는다.

keyListener와 mouseListener는 서로 연관 관계가 없다. 이 둘의 독립적이므로 VisualComponent는 Thread-safe 의무를 Thread-safety한 list에 위임할 수 있다.

CopyOnWriteArrayList()는 Thread-safety하다.

단 write를 할 때마다 배열을 통째로 copy 하므로, write가 잦은 경우 성능이 저하될 수 있다. write가 적고 read가 빈번한 경우에 좋다.

Thread-safety한 리스트
* CopyOnWriteArrayList()
* Collections.synchronizedList(Lists.newArrayList())


##### VisualComponent-class
~~~java
public class VisualComponent {
    private final List<KeyListener> keyListeners = new CopyOnWriteArrayList<KeyListener>();
    private final List<MouseListener> mouseListeners = new CopyOnWriteArrayList<MouseListener>();

    public void addKeyListener(KeyListener listener) {
        keyListeners.add(listener);
    }
    public void addMouseListener(MouseListener listener) {
        mouseListeners.add(listener);
    }
    public void removeKeyListener(KeyListener listener) {
        keyListeners.remove(listener);
    }
    public void removeMouseListener(MouseListener listener) {
        mouseListeners.remove(listener);
    }
}
~~~


## 4.3.3. When Delegation Fails

아래 예제 NumberRange에서는 두 개의 AtomicInteger를 사용하여 상태를 관리하지만 첫번째 숫자가 두번째 숫자보다 작거나 같은 경우는 고려되지 않았다.

NumberRange의 lower와 upper는 원자적이지만 두 스레드가 동시에 setLower나 setUpper에 진입할 수 있으면 유효하지 않는 결과값을 가지게 될 수 있기 때문에 Thread-safety하지 않다.

NumberRange의 상태 구성 요소인 lower, upper가 Thread-safety하지만 NumberRange 클래스가 Thread-safety하지 않은 이유이다.

lock을 사용하여 Thread-safety하게 만들 수 있다.

~~~java
public class NumberRange {
    // INVARIANT: lower <= upper
    private final AtomicInteger lower = new AtomicInteger(0);
    private final AtomicInteger upper = new AtomicInteger(0);

    public void setLower(int i) {
        // Warning -- unsafe check-then-act
        if (i > upper.get())
            throw new IllegalArgumentException("can't set lower to " + i + " > upper");
        lower.set(i);
    }
    public void setUpper(int i) {
        // Warning -- unsafe check-then-act
        if (i < lower.get())
            throw new IllegalArgumentException("can't set upper to " + i + " < lower");
        upper.set(i);
    }
    public boolean isInRange(int i) {
        return (i >= lower.get() && i <= upper.get());
    }
}
~~~


## 4.3.4. Publishing Underlying State Variables

> 상태 변수가 Thread-safety하고 값을 제한하는 변수(private)를 가지며 작업에 대한 금지된 상태 전이가 없는 경우 안전하게 게시할 수 있다.

예를 들어 [VisualComponent-class](#visualcomponent-class) 에서 mouseListener 또는 keyListener를 게시하는 것은 안전하다.


## 4.3.5. Example: Vehicle Tracker that Publishes Its State

아래 SafePoint 클래스는 두 개의 배열 요소를 반환하여 x, y 값을 한번에 검색하는 getter()를 제공한다.

따라서 위치 정보를 변경 가능 하지만 Thread-safety 하다.

~~~java
@ThreadSafe
public class SafePoint {
    @GuardedBy("this") private int x, y;
    private SafePoint(int[] a) {
         this(a[0], a[1]);
    }
    public SafePoint(SafePoint p) {
         this(p.get());
    }
    public SafePoint(int x, int y) {
        this.x = x;
        this.y = y;
    }
    public synchronized int[] get() {
        return new int[] { x, y };
    }
    public synchronized void set(int x, int y) {
        this.x = x;
        this.y = y;
    }
}
~~~

아래 로직은 [DelegatingVehicleTracker-class](#delegatingvehicletracker-class)  클래스와 달리 맵의 내용(x, y 위치 정보)이 변경 가능하지만 Thread-safety를 보장하는 변경 가능한 클래스 이다.

~~~java
@ThreadSafe
public class PublishingVehicleTracker {
    private final Map<String, SafePoint> locations;
    private final Map<String, SafePoint> unmodifiableMap;

    public PublishingVehicleTracker(Map<String, SafePoint> locations) {
        this.locations = new ConcurrentHashMap<String, SafePoint>(locations);
        this.unmodifiableMap = Collections.unmodifiableMap(this.locations);
    }
    public Map<String, SafePoint> getLocations() {
        return unmodifiableMap;
    }
    public SafePoint getLocation(String id) {
        return locations.get(id);
    }
    public void setLocation(String id, int x, int y) {
        if (!locations.containsKey(id))
            throw new IllegalArgumentException("invalid vehicle name: " + id);
        locations.get(id).set(x, y);
    }
}
~~~


# 4.4 Adding Functionality to Existing Thread-safe Classes, Thread-safe 클래스에 기능 추가

~~~java
@ThreadSafe
public class BetterVector<E> extends Vector<E> {
    public synchronized boolean putIfAbsent(E x) {
        boolean absent = !contains(x);
        if (absent)
            add(x);
        return absent;
    }
}
~~~


## 4.4.1. Client-side Locking

왜 아래 코드는 Thread-safety하지 않을까? putIfAbsent 메소드를 synchronized로 묶었는데도 불구하고 말이다.

문제는 잘못된 Lock에서 synchronized를 하고 있다는 것이다.

동기화의 대상은 list이지 메소드가 아니다. 아래 코드에서는 putIfAbsent가 실행되는 동안 다른 스레드가 list의 값을 수정하지 않을리라는 보장이 없다.

하지만 BetterVector 클래스의 경우 Vector는 동기화 처리가 되어있는 클래스이기 때문에 위와 같은 작업을 할 필요가 없다.

~~~java
@NotThreadSafe
public class ListHelper<E> {
    public List<E> list = Collections.synchronizedList(new ArrayList<E>());
        ...
    public synchronized boolean putIfAbsent(E x) {
        boolean absent = !list.contains(x);
        if (absent)
          list.add(x);
        return absent;
    }
}
~~~

> 따라서 아래 코드처럼 putIfAbsent가 아닌 list를 synchronized 하는 것이 올바른 동기화 방법이다.

~~~java
@ThreadSafe
public class ListHelper<E> {
    public List<E> list = Collections.synchronizedList(new ArrayList<E>());
     ...
    public boolean putIfAbsent(E x) {
        synchronized (list) {
            boolean absent = !list.contains(x);
            if (absent)
                list.add(x);
            return absent;
        }
    }
}
~~~


## 4.4.2. Composition

또다른 동기화 방법으로는 생성자에 list를 넘겨서 사용하는 방법이다.

아래 ImprovedList 클래스처럼 사용한다면 기본 List가 Thread-safety한지는 상관이 없다.

~~~java
@ThreadSafe
public class ImprovedList<T> implements List<T> {
    private final List<T> list;
    public ImprovedList(List<T> list) {
        this.list = list;
    }
    public synchronized boolean putIfAbsent(T x) {
        boolean contains = list.contains(x);
        if (contains)
            list.add(x);
        return !contains;
    }
    public synchronized void clear() {
        list.clear();
    }
    // ... similarly delegate other List methods
}
~~~


# 4.5 Documenting Synchronization Policies

문서화는 Thread-safety를 위한 가장 좋은 방법이다. (가장 활용도가 낮지만) 사용자는 문서를 보고 클래스가 스레드로부터 안전한지를 확인할 수 있고 전략을 구상하기 더욱 편해진다.

동기화 정책을 만들려면 몇가지 결정이 필요하다.

어떤 변수를 스레드로부터 lock으로 보호할지, Volatile 타입으로 선언할지, immutable 하게 만들지, 어떤 작업이 원자적이어야 하는지 등에 대해 엄격하게 정리가 되어 있어야 향후 유지보수에도 많은 도움이 된다.

=======
[Chapter 4. Composing Objects](#chapter-4-composing-objects)
- [Chapter 4. Composing Objects](#chapter-4-composing-objects)
- [4.1. Designing a Thread-safe Class, Thread-safe 클래스 디자인하기](#41-designing-a-thread-safe-class-thread-safe-%ed%81%b4%eb%9e%98%ec%8a%a4-%eb%94%94%ec%9e%90%ec%9d%b8%ed%95%98%ea%b8%b0)
  - [4.1.1. Gathering Synchronization Requirements](#411-gathering-synchronization-requirements)
  - [4.1.2. State dependent Operations](#412-state-dependent-operations)
  - [4.1.3. State Ownership](#413-state-ownership)
- [4.2 Instance Confinement, 인스턴스 제한](#42-instance-confinement-%ec%9d%b8%ec%8a%a4%ed%84%b4%ec%8a%a4-%ec%a0%9c%ed%95%9c)
  - [4.2.1. The Java Monitor Pattern](#421-the-java-monitor-pattern)
  - [4.2.2. Example: Tracking Fleet Vehicles](#422-example-tracking-fleet-vehicles)
- [4.3. Delegating Thread Safety](#43-delegating-thread-safety)
  - [4.3.1. Example: Vehicle Tracker Using Delegation , 위임(Delegation)을 사용](#431-example-vehicle-tracker-using-delegation--%ec%9c%84%ec%9e%84delegation%ec%9d%84-%ec%82%ac%ec%9a%a9)
        - [DelegatingVehicleTracker-class](#delegatingvehicletracker-class)
  - [4.3.2. Independent State Variables](#432-independent-state-variables)
        - [VisualComponent-class](#visualcomponent-class)
  - [4.3.3. When Delegation Fails](#433-when-delegation-fails)
  - [4.3.4. Publishing Underlying State Variables](#434-publishing-underlying-state-variables)
  - [4.3.5. Example: Vehicle Tracker that Publishes Its State](#435-example-vehicle-tracker-that-publishes-its-state)
- [4.4 Adding Functionality to Existing Thread-safe Classes, Thread-safe 클래스에 기능 추가](#44-adding-functionality-to-existing-thread-safe-classes-thread-safe-%ed%81%b4%eb%9e%98%ec%8a%a4%ec%97%90-%ea%b8%b0%eb%8a%a5-%ec%b6%94%ea%b0%80)
  - [4.4.1. Client-side Locking](#441-client-side-locking)
  - [4.4.2. Composition](#442-composition)
- [4.5 Documenting Synchronization Policies](#45-documenting-synchronization-policies)

# Chapter 4. Composing Objects

# 4.1. Designing a Thread-safe Class, Thread-safe 클래스 디자인하기

public static 필드에 모든 상태를 저장하는 Thread-safe 프로그램을 작성할 수 있지만 Thread 상태를 안전하게 유지하는 것은 더욱 어렵다.

캡슐화를 통해 전체 프로그램을 검사하지 않고도 클래스가 스레드로부터 안전하다고 판단 할 수 있다.


> Thread-safe 클래스를 설계하려면 다음의 3가지 기본 요소가 포함되어야 한다.
  + 객체안의 변수를 확인해라.
  + 상태값을 가지는 변수의 생성을 제한해라.
  + 객체에 동시적으로 접근하는 것에 대한 정책을 수립해라.

~~~java
@ThreadSafe
public final class Counter {
    @GuardedBy("this")  private long value = 0;

    public synchronized  long getValue() {
        return value;
    }

    public  synchronized  long increment() {
         if (value == Long.MAX_VALUE)
             throw new IllegalStateException("counter overflow");
         return ++value;
    }
}
~~~

value 변수에 대해 synchronized가 정의되었으므로 Thread-safety 하다.


## 4.1.1. Gathering Synchronization Requirements

Thread-safety한 클래스라는 것은 클래스내 변수가 동시 접근 상태에서의 안전을 보장한다는 것이다.

객체와 변수는 상태 공간이라는 것을 가진다. 이 상태 공간이 작을수록 추론하기가 쉽다.

가능한 경우 final로 선언하면 상태를 더 간단하게 추론할 수 있다.

많은 클래스에는 특정 상태를 유효한 것으로 식별하는 유형이 있다.

위의 예제 Counter 클래스에서 변수 value의 길이는 long타입으로 그 길이는 Long.MIN_VALUE에서 Long.MAX_VALUE까지로 유효한 값으로 식별한다.

또한 특정 상태 전이를 유효하지 않은 것으로 식별하는 사후 조건이 있을 수 있다.

Counter 클래스에서 value의 현재 값이 17인 경우 유효한 다음 상태는 18뿐이다.

> 객체의 immutable 및 post conditions을 이해하지 못하면 Thread-safety를 보장할 수 없다.
> 상태 변수에 대한 (유효한 값 또는 상태 전이) 제약 조건은 원자성 및 캡슐화 요구 사항을 만든다.


## 4.1.2. State dependent Operations

일부 객체에는 상태 기반 전제 조건이 있는 메소드들이 있다. 예를 들어 비어있는 큐의 항목을 제거할 수는 없다. 요소를 제거하려면 큐가 "비어 있지 않은" 상태여야 한다.

동시 프로그램에서는 다른 스레드의 동작으로 인해 상태 기반 전제 조건들이 변경될 수 있다. 따라서 작업을 처리할 수 있는 상태가 될 때까지 효율적으로 대기하기 위한 고유 잠금(intrinsic locking)과 같은 내장 메커니즘을 사용해야 한다. 이러한 작업은 BlockingQueue, Semaphore 및 기타 Block 라이브러리 클래스로 쉽게 구현할 수 있다.

## 4.1.3. State Ownership



# 4.2 Instance Confinement, 인스턴스 제한

객체 내에 데이터를 캡슐화하면 객체의 메서드에 대한 데이터 접근이 제한되므로 적절한 lock을 유지한 상태에서 데이터에 항상 접근할 수 있다.

> Instance Confinement 객체는 의도한 범위를 벗어나면 안되는 것을 의미한다.

~~~java
@ThreadSafe
public class PersonSet {
    @GuardedBy("this")
    private final Set<Person> mySet = new HashSet<Person>();

    public synchronized void addPerson(Person p) {
       mySet.add(p);
    }
    public synchronized boolean containsPerson(Person p) {
      return mySet.contains(p);
    }
}
~~~

위 코드는 Instance Confinement 및 lock이 함께 작동하여 클래스 스레드를 안전하게 만드는 방법을 보여준다.

HashSet 자체는 스레드로부터 안전하지 않지만 mySet은 private 타입이며 PersonSet 객체를 탈출할 수 없다. mySet에 접근할 수 있는 유일한 경로는 addPerson 및 containsPerson이며, 이들 각각은 PersonSet에 대한 synchronized를 가지므로 모든 상태는 instrinsic lock으로 보호되어 PersonSet 객체를 Thread-safe 하게 만든다.

> Confinement 클래스는 전체 프로그램을 검사하지 않고도 Thread-safe에 대해 분석할 수 있기 때문에 보다 쉽게 Thread-safety한 프로그램을 작성할 수 있게 만든다.


## 4.2.1. The Java Monitor Pattern

Instance Confinement 원칙을 따라서 java 코드를 짜면 Java 모니터 패턴으로 연결이 된다.

Java 모니터 패턴이란 모든 변경 가능한 상태를 캡슐화하고 객체 자체의 고유 잠금으로 보호하는 것을 뜻한다.

~~~java
public class PrivateLock {
    private final Object myLock = new Object();

    @GuardedBy("myLock") Widget widget;
    void someMethod() {
        synchronized(myLock) {
        // Access or modify the state of widget
        }
    }
}
~~~


## 4.2.2. Example: Tracking Fleet Vehicles

~~~java
Map<String, Point> locations = vehicles.getLocations();

for (String key : locations.keySet())
   renderVehicle(key, locations.get(key));

void vehicleMoved(VehicleMovedEvent evt) {
    Point loc = evt.getNewLocation();
    vehicles.setLocation(evt.getVehicleId(), loc.x, loc.y);
}
~~~

MonitorVehicleTracker 클래스는 차량 위치를 표시하기 위해 MutablePoint 클래스를 사용하여 차량 추적기를 구현한 것이다.

MutablePoint 클래스가 스레드로부터 안전하지 않더라도 MonitorVehicleTracker 클래스는 안전하다.

~~~java
@ThreadSafe
public class MonitorVehicleTracker {
    @GuardedBy("this")
    private final Map<String, MutablePoint> locations;

    public MonitorVehicleTracker(Map<String, MutablePoint> locations) {
        this.locations = deepCopy(locations);
    }
    public synchronized Map<String, MutablePoint> getLocations() {
        return deepCopy(locations);
    }
    public synchronized MutablePoint getLocation(String id) {
           MutablePoint loc = locations.get(id);
        return loc == null ? null : new MutablePoint(loc);
    }
    public synchronized void setLocation(String id, int x, int y) {
        MutablePoint loc = locations.get(id);

        if (loc == null)
            throw new IllegalArgumentException("No such ID: " + id);

        loc.x = x;
        loc.y = y;
    }
    private static Map<String, MutablePoint> deepCopy(Map<String, MutablePoint> m) {
        Map<String, MutablePoint> result = new HashMap<String, MutablePoint>();

        for (String id : m.keySet())
            result.put(id, new MutablePoint(m.get(id)));

        return Collections.unmodifiableMap(result);
    }
}
public class MutablePoint { /* Listing 4.5 */ }
~~~

deepCopy 객체에 Map<String,MutablePoint> 인 locations를 넘기는데 굳이 result로 옮겨 담는 이유는?
=> 중복 데이터 저장을 막기위해서? 동시 스레드 접근할 때 thread-safe 하기 위해서

~~~java
@NotThreadSafe
public class MutablePoint {
    public int x, y;
    public MutablePoint() { x = 0; y = 0; }
    public MutablePoint(MutablePoint p) {
        this.x = p.x;
        this.y = p.y;
    }
}
~~~

# 4.3. Delegating Thread Safety

## 4.3.1. Example: Vehicle Tracker Using Delegation , 위임(Delegation)을 사용

MonitorVehicleTracker 클래스와 달리 위치 정보를 Thread-safety한 클래스에 위임하는 차량 추적기를 구현해보자.

HashMap 대신 ConcurrentHashMap을 사용하고, MutablePoint 대신 ImmutablePoint 클래스를 사용하자.

~~~java
@Immutable
public class Point {
    public final int x, y;
    public Point(int x, int y) {
        this.x = x;
        this.y = y;
    }
}
~~~

> Point는 immutable 이므로 thread로 부터 안전하다.

더이상 위치를 반환할 때 위치를 복사할 필요가 없다. 아래 DelegatingVehicleTracker 클래스는 명시적인 동기화를 사용하지 않는다.

상태에 대한 모든 접근은 ConcurrentHashMap에 의해 관리되며 맵의 모든 키와 값은 변경할 수 없다.

##### DelegatingVehicleTracker-class
~~~java
@ThreadSafe
public class DelegatingVehicleTracker {
    private final ConcurrentMap<String, Point> locations;
    private final Map<String, Point> unmodifiableMap;

    public DelegatingVehicleTracker(Map<String, Point> points) {
        locations = new ConcurrentHashMap<String, Point>(points);
        unmodifiableMap = Collections.unmodifiableMap(locations);
    }
    public Map<String, Point> getLocations() {
        return unmodifiableMap;
    }
    public Point getLocation(String id) {
        return locations.get(id);
    }
    public void setLocation(String id, int x, int y) {
        if (locations.replace(id, new Point(x, y)) == null)
            throw new IllegalArgumentException("invalid vehicle name: " + id);
    }
}
~~~

~~~java
public Map<String, Point> getLocations() {
    return Collections.unmodifiableMap(new HashMap<String, Point>(locations));
}
~~~

## 4.3.2. Independent State Variables

복합 클래스가 여러 상태 변수와 관련하여 불변을 강요하지 않는다.

keyListener와 mouseListener는 서로 연관 관계가 없다. 이 둘의 독립적이므로 VisualComponent는 Thread-safe 의무를 Thread-safety한 list에 위임할 수 있다.

CopyOnWriteArrayList()는 Thread-safety하다.

단 write를 할 때마다 배열을 통째로 copy 하므로, write가 잦은 경우 성능이 저하될 수 있다. write가 적고 read가 빈번한 경우에 좋다.

Thread-safety한 리스트
* CopyOnWriteArrayList()
* Collections.synchronizedList(Lists.newArrayList())


##### VisualComponent-class
~~~java
public class VisualComponent {
    private final List<KeyListener> keyListeners = new CopyOnWriteArrayList<KeyListener>();
    private final List<MouseListener> mouseListeners = new CopyOnWriteArrayList<MouseListener>();

    public void addKeyListener(KeyListener listener) {
        keyListeners.add(listener);
    }
    public void addMouseListener(MouseListener listener) {
        mouseListeners.add(listener);
    }
    public void removeKeyListener(KeyListener listener) {
        keyListeners.remove(listener);
    }
    public void removeMouseListener(MouseListener listener) {
        mouseListeners.remove(listener);
    }
}
~~~


## 4.3.3. When Delegation Fails

아래 예제 NumberRange에서는 두 개의 AtomicInteger를 사용하여 상태를 관리하지만 첫번째 숫자가 두번째 숫자보다 작거나 같은 경우는 고려되지 않았다.

NumberRange의 lower와 upper는 원자적이지만 두 스레드가 동시에 setLower나 setUpper에 진입할 수 있으면 유효하지 않는 결과값을 가지게 될 수 있기 때문에 Thread-safety하지 않다.

NumberRange의 상태 구성 요소인 lower, upper가 Thread-safety하지만 NumberRange 클래스가 Thread-safety하지 않은 이유이다.

lock을 사용하여 Thread-safety하게 만들 수 있다.

~~~java
public class NumberRange {
    // INVARIANT: lower <= upper
    private final AtomicInteger lower = new AtomicInteger(0);
    private final AtomicInteger upper = new AtomicInteger(0);

    public void setLower(int i) {
        // Warning -- unsafe check-then-act
        if (i > upper.get())
            throw new IllegalArgumentException("can't set lower to " + i + " > upper");
        lower.set(i);
    }
    public void setUpper(int i) {
        // Warning -- unsafe check-then-act
        if (i < lower.get())
            throw new IllegalArgumentException("can't set upper to " + i + " < lower");
        upper.set(i);
    }
    public boolean isInRange(int i) {
        return (i >= lower.get() && i <= upper.get());
    }
}
~~~


## 4.3.4. Publishing Underlying State Variables

> 상태 변수가 Thread-safety하고 값을 제한하는 변수(private)를 가지며 작업에 대한 금지된 상태 전이가 없는 경우 안전하게 게시할 수 있다.

예를 들어 [VisualComponent-class](#visualcomponent-class) 에서 mouseListener 또는 keyListener를 게시하는 것은 안전하다.


## 4.3.5. Example: Vehicle Tracker that Publishes Its State

아래 SafePoint 클래스는 두 개의 배열 요소를 반환하여 x, y 값을 한번에 검색하는 getter()를 제공한다.

따라서 위치 정보를 변경 가능 하지만 Thread-safety 하다.

~~~java
@ThreadSafe
public class SafePoint {
    @GuardedBy("this") private int x, y;
    private SafePoint(int[] a) {
         this(a[0], a[1]);
    }
    public SafePoint(SafePoint p) {
         this(p.get());
    }
    public SafePoint(int x, int y) {
        this.x = x;
        this.y = y;
    }
    public synchronized int[] get() {
        return new int[] { x, y };
    }
    public synchronized void set(int x, int y) {
        this.x = x;
        this.y = y;
    }
}
~~~

아래 로직은 [DelegatingVehicleTracker-class](#delegatingvehicletracker-class)  클래스와 달리 맵의 내용(x, y 위치 정보)이 변경 가능하지만 Thread-safety를 보장하는 변경 가능한 클래스 이다.

~~~java
@ThreadSafe
public class PublishingVehicleTracker {
    private final Map<String, SafePoint> locations;
    private final Map<String, SafePoint> unmodifiableMap;

    public PublishingVehicleTracker(Map<String, SafePoint> locations) {
        this.locations = new ConcurrentHashMap<String, SafePoint>(locations);
        this.unmodifiableMap = Collections.unmodifiableMap(this.locations);
    }
    public Map<String, SafePoint> getLocations() {
        return unmodifiableMap;
    }
    public SafePoint getLocation(String id) {
        return locations.get(id);
    }
    public void setLocation(String id, int x, int y) {
        if (!locations.containsKey(id))
            throw new IllegalArgumentException("invalid vehicle name: " + id);
        locations.get(id).set(x, y);
    }
}
~~~


# 4.4 Adding Functionality to Existing Thread-safe Classes, Thread-safe 클래스에 기능 추가

~~~java
@ThreadSafe
public class BetterVector<E> extends Vector<E> {
    public synchronized boolean putIfAbsent(E x) {
        boolean absent = !contains(x);
        if (absent)
            add(x);
        return absent;
    }
}
~~~


## 4.4.1. Client-side Locking

왜 아래 코드는 Thread-safety하지 않을까? putIfAbsent 메소드를 synchronized로 묶었는데도 불구하고 말이다.

문제는 잘못된 Lock에서 synchronized를 하고 있다는 것이다.

동기화의 대상은 list이지 메소드가 아니다. 아래 코드에서는 putIfAbsent가 실행되는 동안 다른 스레드가 list의 값을 수정하지 않을리라는 보장이 없다.

하지만 BetterVector 클래스의 경우 Vector는 동기화 처리가 되어있는 클래스이기 때문에 위와 같은 작업을 할 필요가 없다.

~~~java
@NotThreadSafe
public class ListHelper<E> {
    public List<E> list = Collections.synchronizedList(new ArrayList<E>());
        ...
    public synchronized boolean putIfAbsent(E x) {
        boolean absent = !list.contains(x);
        if (absent)
          list.add(x);
        return absent;
    }
}
~~~

> 따라서 아래 코드처럼 putIfAbsent가 아닌 list를 synchronized 하는 것이 올바른 동기화 방법이다.

~~~java
@ThreadSafe
public class ListHelper<E> {
    public List<E> list = Collections.synchronizedList(new ArrayList<E>());
     ...
    public boolean putIfAbsent(E x) {
        synchronized (list) {
            boolean absent = !list.contains(x);
            if (absent)
                list.add(x);
            return absent;
        }
    }
}
~~~


## 4.4.2. Composition

또다른 동기화 방법으로는 생성자에 list를 넘겨서 사용하는 방법이다.

아래 ImprovedList 클래스처럼 사용한다면 기본 List가 Thread-safety한지는 상관이 없다.

~~~java
@ThreadSafe
public class ImprovedList<T> implements List<T> {
    private final List<T> list;
    public ImprovedList(List<T> list) {
        this.list = list;
    }
    public synchronized boolean putIfAbsent(T x) {
        boolean contains = list.contains(x);
        if (contains)
            list.add(x);
        return !contains;
    }
    public synchronized void clear() {
        list.clear();
    }
    // ... similarly delegate other List methods
}
~~~


# 4.5 Documenting Synchronization Policies

문서화는 Thread-safety를 위한 가장 좋은 방법이다. (가장 활용도가 낮지만) 사용자는 문서를 보고 클래스가 스레드로부터 안전한지를 확인할 수 있고 전략을 구상하기 더욱 편해진다.

동기화 정책을 만들려면 몇가지 결정이 필요하다.

어떤 변수를 스레드로부터 lock으로 보호할지, Volatile 타입으로 선언할지, immutable 하게 만들지, 어떤 작업이 원자적이어야 하는지 등에 대해 엄격하게 정리가 되어 있어야 향후 유지보수에도 많은 도움이 된다.

>>>>>>> 199dcd17923b9ab64d081d598e2eca5a8f415615
> 최소한 클래스가 Thread-safety한지 정도는 문서화해라. 클래스가 Thread-safety한지 추측하면서 개발하지 마라.