# Springboot-Mybatis에서 Transaction을 관리하는 방법

1. sqlSession을 이용하여 Transaction 관리를 Spring에게 맡긴다.
> @Transactional 어노테이션을 통해서 수행할 수 있다.

~~~java
@ThreadSafe
@Configuration
@MapperScan(basePackages = "com.study.damdemo.mapper")
@EnableTransactionManagement
public class DatabaseConfiguration {
    @Bean
    public SqlSessionFactory sqlSessionFactory(DataSource dataSource) throws Exception {
        final SqlSessionFactoryBean sessionFactory = new SqlSessionFactoryBean();
        sessionFactory.setDataSource(dataSource);
        PathMatchingResourcePatternResolver resolver = new PathMatchingResourcePatternResolver();
        sessionFactory.setMapperLocations(resolver.getResources("classpath:mapper/*.xml"));

        return sessionFactory.getObject();
    }

    @Bean
    public SqlSessionTemplate sqlSessionTemplate(SqlSessionFactory sqlSessionFactory) throws Exception {
        return new SqlSessionTemplate(sqlSessionFactory);
    }
}
~~~

~~~java
@Component
@Transactional
public class DamDao {
    private final SqlSession sqlSession;

    public DamDao(SqlSession sqlSession) {
        this.sqlSession = sqlSession;
    }


    public void insertDamUpldData(DamUpldData damUpldData) {
        try {
            sqlSession.insert("mapper.damUpldData.insertDamUpldData",damUpldData);
        } catch (Exception e) {
            throw e;
        }
    }
}
~~~


2. DataSourceTransactionManager 를 이용하여 수동으로 Transaction을 관리한다.
> DataSourceTransactionManager로부터 트랜잭션의 상태값을 얻은 뒤, commit or rollback을 수행한다.

~~~java
@Component
public class DamDao {
    private final SqlSession sqlSession;
    private final DataSourceTransactionManager dataSourceTransactionManager;

    public DamDao(SqlSession sqlSession, DataSourceTransactionManager dataSourceTransactionManager) {
        this.sqlSession = sqlSession;
        this.dataSourceTransactionManager = dataSourceTransactionManager;
    }

    public void insertDamUpldData(DamUpldData damUpldData) {
        TransactionStatus txStatus = dataSourceTransactionManager.getTransaction(new DefaultTransactionDefinition());

        try {
            sqlSession.insert("mapper.damUpldData.insertDamUpldData",damUpldData);
            dataSourceTransactionManager.commit(txStatus);
        } catch (Exception e) {
            dataSourceTransactionManager.rollback(txStatus);
            throw e;
        }
    }
}
~~~