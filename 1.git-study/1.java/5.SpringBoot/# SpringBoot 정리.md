# Spring 정리

# 1. 개념

### 1.1 PSA

### 1.2 AOP

### 1.3 IOC


# 2. DI 의존성 주입 방법

## 2.1 Field 주입
~~~java
@Autowired
private SampleObject sampleObject;
~~~

매우 간단하지만 아래와 같은 단점으로 권장되지 않는 방법이다.
1. 불변성 위반
    - 필드 주입 객체는 final로 선언할 수 없다.
    
2. 순환 의존성 알수 없음
    - 순환 의존 현상이 발생하더라도 Exception을 안뱉으므로 알 수 없다.
    서로 끊임없이 참조하다 결국 StackOverFlowError로 죽는다.

3. DI 컨테이너의 결합성과 테스트 용이성 위배
    - 필요한 의존성을 전달하면 독립적으로 인스턴스화 가능해야 한다.
    - 하지만 필드 주입을 사용하면 필요한 의존성을 가진 클래스를 인스턴스화 할 수 없다.

4. 단일 책임의 원칙
    - 하나의 클래스에서 주입되는 클래스가 많아질수록 해당 클래스가 책임지는 상황이 많이 발생하게 되는데 이는 리팩토링이 되어야할 상황이다.
    - 이 때 필드 주입 방식은 비교적 간단한 코드로 의존성을 주입하므로 다른 방식에 비해서 무분별하게 의존성을 주입하기 쉽다.

## 2.2 Setter 주입
~~~java
private SampleObject sampleObject;

@Autowired
public void setSampleObject(SampleObject sampleObject){
    this.sampleObject = sampleObject;
}
~~~

## 2.3 Construtor 주입 (권장되는 방법)
~~~java
~~~


# 2. SpringJPA



# Docker에서 Spring 프로젝트 사용 Tib

### 1. Spring Project dockerfile 작성
* Dockerfile
~~~Dockerfile
FROM java:8
EXPOSE 8080
ARG JAR_FILE=./lib
ARG CONFIG_FILE=./config/application.properties
ADD ${JAR_FILE} lib
ADD ${CONFIG_FILE} application.properties
CMD ["java","-cp","/application.properties","-jar","lib/demo-1.0.jar"]

#base image
FROM openjdk:8
ADD config /home/vagrant/sepas/config
ADD lib /home/vagrant/sepas/lib
ENV TZ=Asia/Seoul
CMD ["java","-jar","/home/vagrant/sepas/lib/sepas-demo-0.0.1-SNAPSHOT.jar","--spring.config.location=/home/vagrant/sepas/config/application.yml"]
~~~

### 2. Spring Project 외부 파일 설정
~~~py
$ nohup java -`Dlog4j.configurationFile=`./target/config/log4j2.xml -jar target/lib/maven-sepas-demo-0.0.1-SNAPSHOT.jar --spring.config.location=file:./target/config/application.properties 1> /dev/null 2>&1 &
~~~

