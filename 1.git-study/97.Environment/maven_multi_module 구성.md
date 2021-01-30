
# 1. New Project - Empty Project


# pom.xml

<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
<modelVersion>4.0.0</modelVersion>
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>2.3.3.RELEASE</version>
    <relativePath/> <!-- lookup parent from repository -->
</parent>
<groupId>com.study</groupId>
<artifactId>demo-spring</artifactId>
<version>0.0.1-SNAPSHOT</version>
<name>demo-spring</name>
<description>Demo project for Spring Boot</description>

<properties>
    <java.v>1.8</java.v>
</properties>

<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter</artifactId>
    </dependency>

    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
        <exclusions>
            <exclusion>
                <groupId>org.junit.vintage</groupId>
                <artifactId>junit-vintage-engine</artifactId>
            </exclusion>
        </exclusions>
    </dependency>
</dependencies>
<build>
    <!--        Intellij 는 default로 /src/main/java를 Sources Root 경로로 사용한다.-->
    <!--        <sourceDirectory>/src/main/java</sourceDirectory>-->
    <resources>
        <resource>
            <directory>src/main/resources</directory>
            <!--<excludes>
                <exclude>*.xml</exclude>
            </excludes>-->
        </resource>
    </resources>

    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.8.0</version>
            <configuration>
                <encoding>UTF-8</encoding>
                <compilerArgument>-nowarn</compilerArgument>
                <compilerArgument>-verbose</compilerArgument>
                <compilerArgument>-parameters</compilerArgument>
                <testCompilerArgument>-parameters</testCompilerArgument>
                <source>${java.v}</source>
                <target>${java.v}</target>
            </configuration>
        </plugin>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-dependency-plugin</artifactId>
            <executions>
                <execution>
                    <id>copy-dependencies</id>
                    <phase>package</phase>
                    <goals>
                        <goal>copy-dependencies</goal>
                    </goals>
                    <configuration>
                        <outputDirectory>
                            ${project.basedir}/target/lib
                        </outputDirectory>
                        <overWriteReleases>false</overWriteReleases>
                        <overWriteSnapshots>false</overWriteSnapshots>
                        <overWriteIfNewer>true</overWriteIfNewer>
                    </configuration>
                </execution>
            </executions>
        </plugin>
        <plugin>
            <artifactId>maven-jar-plugin</artifactId>
            <version>3.0.2</version>
            <configuration>
                <outputDirectory>${project.basedir}/target/lib</outputDirectory>
                <archive>
                    <manifest>
                        <addClasspath>true</addClasspath>
                        <mainClass>
                            com.study.demospring.DemoSpringApplication
                        </mainClass>
                    </manifest>
                </archive>
            </configuration>
        </plugin>
        <plugin>
            <artifactId>maven-resources-plugin</artifactId>
            <version>3.0.2</version>
            <executions>
                <execution>
                    <id>default-copy-resources</id>
                    <phase>process-resources</phase>
                    <goals>
                        <goal>copy-resources</goal>
                    </goals>
                    <configuration>
                        <overwrite>true</overwrite>
                        <outputDirectory>${project.basedir}/target/config</outputDirectory>
                        <resources>
                            <resource>
                                <directory>${project.basedir}/src/main/resources</directory>
                                <includes>
                                    <include>META-INF/**.*</include>
                                    <include>*.xml</include>
                                    <include>*.yml</include>
                                    <include>*.properties</include>
                                </includes>
                            </resource>
                        </resources>
                    </configuration>
                </execution>
            </executions>
        </plugin>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-deploy-plugin</artifactId>
            <version>2.8.2</version>
            <configuration>
                <updateReleaseInfo>false</updateReleaseInfo>
            </configuration>
            <executions>
                <execution>
                    <id>deploy-executable</id>
                    <goals>
                        <goal>deploy-file</goal>
                    </goals>
                    <configuration>
                        <file>
                            ${project.basedir}/target/lib/${project.artifactId}-${project.version}.jar
                        </file>
                    </configuration>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>

<!--    <build>-->
<!--        <plugins>-->
<!--            <plugin>-->
<!--                <groupId>org.springframework.boot</groupId>-->
<!--                <artifactId>spring-boot-maven-plugin</artifactId>-->
<!--            </plugin>-->
<!--        </plugins>-->
<!--    </build>-->

</project>
