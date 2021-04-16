# Redis(Remote Dictionary Server) 특징
휘발성이며 영속성을 가진 Key-Value 형태의 in-memory 저장소

1. NoSQl 데이터 모델
   - Key-Value
   - Column : 하나의 Key에 Multi Value 가질 수 있음 (중첩된 HashMap 구조)
   - Document : Value가 Json이거나 XML Document를 갖는 모델
   - Graph : 관계에 특화된 모델

2. 휘발성이며 영속성 보장
   - in-memory 기반이다.
   - 때문에 빠른 read/write 속도를 가진다.
   - 모든 데이터가 메모리 안에 있기 때문에 캐시 관점에서 유용하다.
   - DB 부하를 줄인다.
   - snapshotting(RDB) 방식 : 순간적으로 메모리에 있는 데이터를 디스크 전체에 옮겨 담는 방식
   - AOF(Append On File) 방식 : 메모리에 있는 모든 데이터를 read/write event를 모두 log 파일에 기록하는 방식

3. Data Type
   - String
   - Set
   - Sorted Set
   - Hashes
   - List