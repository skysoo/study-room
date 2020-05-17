# SpringBoot 정리

# 1. 개념

### 1.1 PSA

### 1.2 AOP

### 1.3 IOC


# 2. SpringJPA



# 현업 사용 Tib

### 1. Spring Project dockerfile 작성
* Dockerfile
~~~
FROM java:8
EXPOSE 8080
ARG JAR_FILE=./lib
ARG CONFIG_FILE=./config/application.properties
ADD ${JAR_FILE} lib
ADD ${CONFIG_FILE} application.properties
CMD ["java","-cp","/application.properties","-jar","lib/demo-1.0.jar"]
~~~

### 2. Spring Project 외부 파일 설정
~~~
nohup java -`Dlog4j.configurationFile=`./target/config/log4j2.xml -jar target/lib/maven-sepas-demo-0.0.1-SNAPSHOT.jar --spring.config.location=file:./target/config/application.properties 1> /dev/null 2>&1 &
~~~

