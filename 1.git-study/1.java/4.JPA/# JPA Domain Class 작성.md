# 1. Lombok Annotaion을 이용한 Domain 클래스 작성

### 1.1 Setter를 만들지 마라.

### 1.2 @Data 한번에 @Getter, @Setter, @RequiredArgsConstructor, @ToString, @EqualsAndHashCode 이 모든 것을 다 거는 강력한 어노테이션이니만큼 함부로 쓰지 말자.

### 1.3 클래스 및 모든 필드를 final로 선언하자.

### 1.4 @NoArgsConstructor (force=true) - 모든 필드가 final 이기 때문에 초기값이 필요하다.

### 1.5 @EqualsAndHashCode 어노테이션 사용시 전체 필드가 아닌 반드시 값 비교가 필요한 필드만 지정을 해주자.

### 1.6 Immutable 클래스로 작성되었기 때문에 Builder 패턴을 이용하여 값을 세팅하자.

### 1.7 @ManyToOne, @OneToOne 은 반드시 FetchType.LAZY로 걸어라 - 아니면 쿼리 날리때마다 모든 값을 다 가져옴

### 1.8 값 타입 컬렉션은 그냥 @ElementCollection, @CollectionTable 은 사용하지마라 - 모든 데이터를 지웠다가 다시 Insert함

### 1.9 Domain 클래스에서 @OneToMany는 Builder에 추가할 필요 없다.

### 1.10 DTO 작성시 데이터 타입은 Wrapper 클래스를 사용하자. (null 필요할 수도 있기 때문에)

- example 빌더 직접 구현

```java
/**
 * @author skysoo
 * @version 1.0.0
 * @since 2020-05-20 오후 2:09
 **/
@Getter
@EqualsAndHashCode(of = {"id"}, callSuper = false)
@NoArgsConstructor(force = true) // 초기값이 필요한 final 필드가 있을 경우 컴파일 에러 발생 - 해결 : force = true 옵션을 주면 된다.
//@NoArgsConstructor(access = AccessLevel.PROTECTED) // 접근 권한을 Protected로 선언했으므로 외부 패키지에서 생성자에 접근할 수 없고, Builder 생성자를 통해야 한다.
@Entity
@Table(name = "`SNSR_ECK_DATA`", schema = "`EPZSEPAS`")
public final class SnsrEckData extends BaseEntity implements Serializable {
    @Id
    @NotNull
    @GeneratedValue(generator = "system-uuid")
    @GenericGenerator(name = "system-uuid", strategy = "uuid")
    @Column(name = "`SNSR_ECK_SEQ`")
    private String id;
    @Column(name = "`ECK_STRE_INX_NM`")
    private final String eckStreIndxNm;
    @Column(name = "`INTGR_CD`")
    private final String intgrCd;
    @Embedded
    private final Msrmn msrmn;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "`SNSR_ID`")
    private final SnsrInfo snsrInfo;

    public SnsrEckData(SnsrEckDataBuilder builder) {
        super(builder.createDt, builder.createTm);
        this.eckStreIndxNm = builder.eckStreIndxNm;
        this.intgrCd = builder.intgrCd;
        this.msrmn = builder.msrmn;
        this.snsrInfo = builder.snsrInfo;
        builder.snsrInfo.getSnsrEckDataSet().add(this); // 양방향 매핑 값 설정
    }

    public static class SnsrEckDataBuilder extends BaseEntity{
        private final String eckStreIndxNm;
        private final String intgrCd;
        private final Msrmn msrmn;
        private final SnsrInfo snsrInfo;
        private final String createDt;
        private final String createTm;

        public SnsrEckDataBuilder(String eckStreIndxNm, String intgrCd, String msrmnDt, String msrmnTm, String createDt, String createTm, SnsrInfo snsrInfo) {
            this.eckStreIndxNm = eckStreIndxNm;
            this.intgrCd = intgrCd;
            this.msrmn = new Msrmn.MsrmnBuilder(msrmnDt,msrmnTm).builder();
            this.snsrInfo = snsrInfo;
            this.createDt = createDt;
            this.createTm = createTm;
        }

        public SnsrEckData builder(){
            return new SnsrEckData(this);
        }
    }

//    @Builder
//    public SnsrElkData(SnsrInfo snsrInfo, String eckStreIndxNm, String intgrCd, String msrmnDt, String msrmnTm, String createDt, String createTm) {
//        this.snsrInfo = snsrInfo;
//        this.eckStreIndxNm = eckStreIndxNm;
//        this.intgrCd = intgrCd;
//        this.period = new Period.PeriodBuilder(msrmnDt,msrmnTm).builder();
//        super.setCreateDt(createDt);
//        super.setCreateTm(createTm);
//    }

}
```

## DeliveryDTO

```java
@Entity
@Getter
@EqualsAndHashCode
@NoArgsConstructor(force = true)
@SequenceGenerator(
        name = "DELIVERY_SEQ_GENERATOR",
        schema = "`PSS`",
        sequenceName = "`DELIVERY_SEQ`",
        initialValue = 1, allocationSize = 5)
@Table(name = "`DELIVERY`", schema = "`PSS`")
public class DeliveryDTO implements Serializable {
    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "DELIVERY_SEQ_GENERATOR")
    @Column(name = "`DELIVERY_ID`")
    private final long id;
    @Column(name = "`CITY`")
    private final String city;
    @Column(name = "`STREET`")
    private final String street;
    @Column(name = "`ZIP_CODE`")
    private final String zipCode;
    @Enumerated(EnumType.STRING)
    @Column(name = "`DELIVERY_STATUS`")
    private StatusType statusType;

    @Builder
    public DeliveryDTO(long id, String city, String street, String zipCode, StatusType statusType, OrderDTO orderDTO) {
        this.id = id;
        this.city = city;
        this.street = street;
        this.zipCode = zipCode;
        this.statusType = statusType;
    }
}
```

## OrderItemDTO

```java
@Entity
@Getter
@EqualsAndHashCode
@NoArgsConstructor(force = true)
@SequenceGenerator(
        name = "ORDER_ITEM_SEQ_GENERATOR",
        schema = "`PSS`",
        sequenceName = "`ORDER_ITEM_SEQ`",
        initialValue = 1, allocationSize = 5)
@Table(name = "`ORDER_ITEM`", schema = "`PSS`")
public class OrderItemDTO implements Serializable {
    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "ORDER_ITEM_SEQ_GENERATOR")
    @Column(name = "`ORDER_ITEM_ID`")
    private final long id;
    @Column(name = "`ORDER_PRICE`")
    private final int orderPrice;
    @Column(name = "`COUNT`")
    private final int count;

    @ManyToOne(fetch = FetchType.LAZY, cascade = CascadeType.ALL)
    @JoinColumn(name = "`ORDER_ID`")
    private OrderDTO orderDTO;

    @ManyToOne(fetch = FetchType.LAZY, cascade = CascadeType.ALL)
    @JoinColumn(name = "`ITEM_ID`")
    private ItemDTO itemDTO;

    // 연관 관계 편의 메서드
    public void setOrderDTO(OrderDTO orderDTO){
        this.orderDTO = orderDTO;
        orderDTO.getOrderItemDTOList().add(this);
    }

    // 연관 관계 편의 메서드
    public void setItemDTO(ItemDTO itemDTO){
        this.itemDTO = itemDTO;
        itemDTO.getOrderItemDTOList().add(this);
    }

    @Builder
    public OrderItemDTO(long id, int orderPrice, int count, OrderDTO orderDTO, ItemDTO itemDTO) {
        this.id = id;
        this.orderPrice = orderPrice;
        this.count = count;
        this.orderDTO = orderDTO;
        this.itemDTO = itemDTO;
    }
}
```

## OrderDTO

```java
@Entity
@Getter
@EqualsAndHashCode
@NoArgsConstructor(force = true)
@SequenceGenerator(
        name = "ORDER_SEQ_GENERATOR",
        schema = "`PSS`",
        sequenceName = "`ORDER_SEQ`",
        initialValue = 1, allocationSize = 5)
@Table(name = "`ORDERS`", schema = "`PSS`")
public class OrderDTO implements Serializable {
    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "ORDER_SEQ_GENERATOR")
    @Column(name = "`ORDER_ID`")
    private final long id;
//    @Temporal(TemporalType.TIMESTAMP) // 타입이 Date 일 경우
    @Column(name = "`ORDER_DATE`")
    private final LocalDateTime orderDate;

    @ManyToOne(fetch = FetchType.LAZY, cascade = CascadeType.ALL)
    @JoinColumn(name = "`MEMBER_ID`")
    private MemberDTO memberDTO;

    @OneToMany(mappedBy = "orderDTO", fetch = FetchType.LAZY)
    private List<OrderItemDTO> orderItemDTOList = new ArrayList<>();

    @OneToOne(fetch = FetchType.LAZY, cascade = CascadeType.ALL)
    @JoinColumn(name = "`DELIVERY_ID`")
    private DeliveryDTO deliveryDTO;

    // 연관 관계 편의 메서드
    public void setMemberDTO(MemberDTO memberDTO){
        this.memberDTO = memberDTO;
        memberDTO.getOrderDTOList().add(this);
    }

    @Builder
    public OrderDTO(long id, LocalDateTime orderDate, MemberDTO memberDTO, List<OrderItemDTO> orderItemDTOList, DeliveryDTO deliveryDTO) {
        this.id = id;
        this.orderDate = orderDate;
        this.memberDTO = memberDTO;
        this.orderItemDTOList = orderItemDTOList;
        this.deliveryDTO = deliveryDTO;
    }
}
```

## MemberDTO

```java
@Entity
@Getter
@EqualsAndHashCode
@NoArgsConstructor(force = true)
@SequenceGenerator(
        name = "`MEMBER_SEQ_GENERATOR`",
        schema = "`PSS`",
        sequenceName = "`MEMBER_SEQ`",
        initialValue = 1, allocationSize = 5)
@Table(name = "`MEMBER`", schema = "`PSS`")
public class MemberDTO implements Serializable {
    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "`MEMBER_SEQ_GENERATOR`")
    @Column(name = "`MEMBER_ID`")
    private final long id;
    @Column(name = "`NAME`")
    private final String name;
    @Column(name = "`CITY`")
    private final String city;
    @Column(name = "`STREET`")
    private final String street;
    @Column(name = "`ZIP_CODE`")
    private final String zipCode;
    @Enumerated(EnumType.STRING)
    @Column(name = "`ROLE`")
    private final RoleType roleType;

    @OneToMany(mappedBy = "memberDTO", fetch = FetchType.LAZY)
    private List<OrderDTO> orderDTOList = new ArrayList<>();

    @Builder
    public MemberDTO(long id, String name, String city, String street, String zipCode, RoleType roleType, List<OrderDTO> orderDTOList) {
        this.id = id;
        this.name = name;
        this.city = city;
        this.street = street;
        this.zipCode = zipCode;
        this.roleType = roleType;
        this.orderDTOList = orderDTOList;
    }
}
```

## ItemDTO

```java
@Entity
@Getter
@EqualsAndHashCode
@NoArgsConstructor(force = true)
@SequenceGenerator(
        name = "ITEM_SEQ_GENERATOR",
        schema = "`PSS`",
        sequenceName = "`ITEM_SEQ`",
        initialValue = 1, allocationSize = 5)
@Table(name = "`ITEM`", schema = "`PSS`")
public class ItemDTO implements Serializable {
    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "ITEM_SEQ_GENERATOR")
    @Column(name = "`ITEM_ID`")
    private final long id;
    @Column(name = "`NAME`")
    private final String name;
    @Column(name = "`PRICE`")
    private final int price;
    @Column(name = "`STOCK_QUANTITY`")
    private final int stockQuantity;

    @OneToMany(mappedBy = "itemDTO", fetch = FetchType.LAZY)
    private List<OrderItemDTO> orderItemDTOList = new ArrayList<>();

    @Builder
    public ItemDTO(long id, String name, int price, int stockQuantity, List<OrderItemDTO> orderItemDTOList) {
        this.id = id;
        this.name = name;
        this.price = price;
        this.stockQuantity = stockQuantity;
        this.orderItemDTOList = orderItemDTOList;
    }
}

```
