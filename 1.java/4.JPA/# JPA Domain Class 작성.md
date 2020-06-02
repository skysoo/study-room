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

* example
~~~java
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
~~~