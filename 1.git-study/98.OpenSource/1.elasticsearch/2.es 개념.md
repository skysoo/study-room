# Elasticsearch

# 1. Transport Client

* Java Low Level REST Client 로 Client를 소켓으로 직접 만들어 사용했다.

~~~java
TransportClient client = new PreBuiltTransportClient(Settings.EMPTY)
        .addTransportAddress(new InetSocketTransportAddress(InetAddress.getByName("host1"), 9300))
        .addTransportAddress(new InetSocketTransportAddress(InetAddress.getByName("host2"), 9300));

// on shutdown
client.close();
~~~

> 하지만 TransportClient는 Elasticsearch 7.0에서 deprecataing, 8.0에서 완전히 지원하지 않는 것으로 확정


# 2. RestHighLevelClient

* Java High Level REST Client 를 사용하도록 강제함

* 기본적으론 Low Level REST Client를 기반한 것이며, 가장 큰 차이점은 비동기 처리를 지원한다는 것이다.

~~~java
RestHighLevelClient client = new RestHighLevelClient(
        RestClient.builder(
                new HttpHost("localhost", 9200, "http"),
                new HttpHost("localhost", 9201, "http")));
~~~


일 데이터가 2TB가 된다는 것은 작게는 KB에서 크게는 MB까지 되는 로그 파일이 하루에 억 단위로 쌓이는 양입니다.

분당 수만건의 데이터가 적재되는데 이를 실시간으로 처리해야 합니다.

엄청난 트래픽인데요. 해당 서비스를 구현하기 위해서 데이터를 받는 부분, 전처리 하는 부분, 적재하는 부분, 조회하는 부분으로 크게 프로세스를 나눴습니다.

데이터 양이 너무 많아 속도나 메모리 관련 이슈가 발생하였고 처리하는 부분은 C(메모리를 직접 조절하여 릭을 방지)로 구현되어있습니다.

적재하는 부분은 자바로 작성되었고 멀티 스레딩을 적용하여 처리 속도를 개선하였습니다.

하지만 Elasticsearch 7.x부터 소켓통신의 LowLevel

