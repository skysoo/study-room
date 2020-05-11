## 1. Thread

### 1.1 Thread Status
  * 객체 생성 NEW
	* 실행 대기 RUNNABLE
	* 일시 정지  WAITING - wait(), join(), sleep()
								TIMED_WAITING - wait(), join(), sleep() WAITING 상태와의 차이점은 외부적인 변화뿐 아니라 시간에 의해서도 WAITING 상태가 해제 될 수 있다
								BLOCKED - monitor를 획득하기 위해 다른 스레드가 락을 해제하기를 기다리는 상태(스레드 동기화와 관련)
	* 실행 				RUN
	* 종료				TERMINATED

1. Thread 구현 방법
   1. Thread 상속
      1. start() 메서드 호출 가능

   2. Runnable 구현한 뒤, Thread 객체 생성
      1. start() 메서드 호출 불가능, 반드시 Thread 객체에 담아서 사용

	 3. Lambda를 사용하여 runnable 구현


2. start()와 run()의 차이점?

	start() : New 상태 -> Runnable 상태 (실행 가능한 대기 큐에 들어간 것을 의미한다.)
					메타 정보를 넣고 run()한다.

	run() :  메타 정보를 넣지 않고 run()한다. 제대로된 thread 정보를 가져오지 못할 수 도 있다.

> run()은 단순히 메소드를 실행하는 것이고(싱글스레드), start()는 스택을 만들고 스택안에서 run()하는 것이다.(멀티스레드)


## 2. Concurrency 와 Parallelism

### 2.1 Concurrency


### 2.2 Parallelism
![jvm 구조]()
