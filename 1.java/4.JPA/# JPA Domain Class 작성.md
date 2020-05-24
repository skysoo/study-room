# 1. Lombok Annotaion을 이용한 Domain 클래스 작성

### 1.1 Setter를 만들지 마라.
### 1.2 @Data 한번에 @Getter, @Setter, @RequiredArgsConstructor, @ToString, @EqualsAndHashCode 이 모든 것을 다 거는 강력한 어노테이션이니만큼 함부로 쓰지 말자.
### 1.3 @NoArgsConstructor 어노테이션의 접근 레벨을 지정해주자. (public말고)
### 1.4 @EqualsAndHashCode 어노테이션 사용시 전체 필드가 아닌 반드시 값 비교가 필요한 필드만 지정을 해주자.

* example
~~~java
@Getter
@EqualsAndHashCode(of = {"id"})
//@NoArgsConstructor(force = true) // 초기값이 필요한 final 필드가 있을 경우 컴파일 에러 발생 - 해결 : force = true 옵션을 주면 된다.
@NoArgsConstructor(access = AccessLevel.PROTECTED) // 접근 권한을 Protected로 선언했으므로 외부 패키지에서 생성자에 접근할 수 없고, Builder 생성자를 통해야 한다.
@Entity
@Table(name = "`SNSR_ELK_DATA`", schema = "`EPZSEPAS`")
public class SnsrElkData implements Serializable {
    @Id
    @NotNull
    @GeneratedValue(generator = "system-uuid")
    @GenericGenerator(name = "system-uuid", strategy = "uuid")
    @Column(name = "`SNSR_ELK_SEQ`")
    private String id;
    @Column(name = "`SNSR_ID`")
    private String snsrId;
    @Column(name = "`ELK_STRE_INX_NM`")
    private String elkStreIndxNm;
    @Column(name = "`INTGR_CD`")
    private String intgrCd;
    @Column(name = "`MSRMN_DT`", length = 8)
    private String msrmnDt;
    @Column(name = "`MSRMN_TM`", length = 6)
    private String msrmnTm;
    @Column(name = "`CREATE_DT`", length = 8)
    private String createDt;
    @Column(name = "`CREATE_TM`", length = 6)
    private String createTm;

    @Builder
    public SnsrElkData(String snsrId, String elkStreIndxNm, String intgrCd, String msrmnDt, String msrmnTm, String createDt, String createTm) {
        this.snsrId = snsrId;
        this.elkStreIndxNm = elkStreIndxNm;
        this.intgrCd = intgrCd;
        this.msrmnDt = msrmnDt;
        this.msrmnTm = msrmnTm;
        this.createDt = createDt;
        this.createTm = createTm;
    }
}
~~~