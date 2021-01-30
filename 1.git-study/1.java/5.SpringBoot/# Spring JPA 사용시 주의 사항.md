# Spring JPA 사용시 주의 사항

# 1. JPA N+1 문제

연관되는 하위 엔티티들에 대한 대량의 조회 쿼리를 막기 위해서는 지연 로딩을 사용해라.

- 지연 로딩

```java
// 지연 로딩
@ManyToOne(fetch = FetchType.LAZY)
@JoinColumn(name = "team_id")
private Team team;
```

- 지연로딩으로 설정된 엔티티 객체는 처음에 프록시로 가져온다.
- 그리고 프록시 내 다른 값이 필요한 경우(프록시 초기화가 진행된다)

> 그리고 한번에 여러 엔티티들의 데이터를 가져와야한다면 Fetch Join을 사용해라!!

# 2. JPA Session Error

```java
org.hibernate.LazyInitializationException: failed to lazily initialize a collection of role: com.study.batch.dto.relation.MemberDTO.orderDTOSet, could not initialize proxy - no Session
```

JPA Session 에러는 다양한 원인이 있을 수 있지만 나같은 경우는 lombok의 @ToString 어노테이션 때문이었다.

Lazy 엔티티를 ToString으로 값을 불러 들이려고 하는데서 Lazy Exception 에러가 발생한 것이다.

MEMBER DTO에는 아래와 같이 orderDTOSet이 FetchType.LAZY로 설정 되어 있었다.

```java
 @OneToMany(mappedBy = "memberDTO", fetch = FetchType.LAZY)
    private Set<OrderDTO> orderDTOSet = new HashSet<>();
```

그 와중에 Memeber DTO 전체 객체에 대한 @ToString이 적용되니 둘의 컨텍스트 영속성 상태가 다르기 때문에 Lazy Exception이 발생한 것이다.

# 3. 기본 연관 관계 문제

다대일 관계의 테이블에 값을 매핑하고 save를 했지만 FK가 매핑되지 않는 문제가 발생한다면?

연관관계 매핑의 기초적인 공부부터 다시 해야 한다.

## 3-1. 문제 상황

```JAVA
public class MemberDTO implements Serializable {
    ...
    @OneToMany(mappedBy = "memberDTO", fetch = FetchType.LAZY)
    private Set<OrderDTO> orderDTOSet = new HashSet<>();

    // 연관 관계 편의 메서드
    public void add(OrderDTO orderDTO){
        this.orderDTOSet.add(orderDTO);
    }
    ...
}

public class OrderDTO implements Serializable {
    ...
    @ManyToOne(fetch = FetchType.LAZY, cascade = CascadeType.ALL)
    @JoinColumn(name = "`MEMBER_ID`")
    private MemberDTO memberDTO;
    ...
}

@Test
public void jpaInsertTest(){
    MemberDTO member = MemberDTO.builder()
                    .name("BOOK TEST")
                    .city("BUSAN")
                    .street("SEOGU")
                    .zipCode("12345")
                    .roleType(RoleType.VIP)
                    .orderDTOSet(new HashSet<>())
                    .build();
    memberService.save(member); // Member를 하나 만들어주고

    OrderDTO order = OrderDTO.builder()
                    .orderDate(LocalDateTime.now())
                    .build();

    member.add(order); // Member에 Order(주문)을 하나 추가한다.

    orderService.save(order); // 주문을 저장
}
```

## 3-2. 해결 방법-1 연관 관계의 주인에 바로 값을 셋팅

```java
@Test
public void jpaInsertTest(){
    MemberDTO member = MemberDTO.builder()
                    .name("BOOK TEST")
                    .city("BUSAN")
                    .street("SEOGU")
                    .zipCode("12345")
                    .roleType(RoleType.VIP)
                    .build();
    memberService.save(member);

    OrderDTO order = OrderDTO.builder()
                    .memberDTO(member) // 연관 관계의 주인에 값을 셋팅하면됨
                    .orderDate(LocalDateTime.now())
                    .build();
    orderService.save(order);
}
```

## 3-3. 해결 방법-2 잘못된 연관 관계 편의 메서드

```java
# MemberDTO의 add() 메서드 수정
public void add(OrderDTO orderDTO){
    this.orderDTOSet.add(orderDTO); // mappedBy는 가짜 매핑이다.(자바코드에서 조회용으로 사용됨)
    orderDTO.setMemberDTO(this); // 주인쪽 객체에 값을 담아줘야 한다.
}
```

## 3-4. 결론

> 연관 관계 주인쪽에서 항상 값을 셋팅하자
