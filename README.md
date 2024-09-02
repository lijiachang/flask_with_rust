# Speed Your Python with Rust: flask_with_rust
Injecting Rust into a Python Flask App.   
将Rust注入到Python Flask应用程序

项目使用Flask、Rust、Postgres、Celery、Nginx、Docker、Docker-compose构建一个Web应用程序，计算斐波那契数列。  

第一阶段
* 使用Flask作为Web框架，Flask使用当前最新的3.0版本
* 使用数据库存储计算结果，避免重复计算
* 使用Celery异步处理计算任务
* 使用Docker和Docker-compose部署应用程序
* 使用Alembic进行数据库迁移
* 使用Nginx作为Web服务器
* 使用Gunicorn作为WSGI服务器  


第二阶段
* 使用Rust编写计算斐波那契数列的函数，提高计算速度
* 使用Rust Diesel管理与数据库的模型和连接 (项目地址: https://github.com/lijiachang/rust-db-diesel)


## 构建Python Flask应用程序
使用Nginx、数据库、Celery（实现消息总线）来构建一个Flask Web应用程序  
此消息总线将允许应用程序在返回Web http请求时在后台处理繁重的任务。  
Web应用程序和消息总线将会包装到Docker中，并部署到docker-compose

构建flask镜像

    docker build . -t flask-fib

```text
(.venv) ➜  src git:(main) ✗ docker image ls            
REPOSITORY                                     TAG          IMAGE ID       CREATED          SIZE
flask-fib                                      latest       85a32b6a11f4   10 seconds ago   1.12GB
```

使用docker-compose构建Flask和Nginx

    docker-compose up

```text
(.venv) ➜  deployment git:(main) ✗ docker-compose up          
WARN[0000] /Users/lijiachang/code/rust/flask_with_rust/deployment/docker-compose.yml: `version` is obsolete 
[+] Running 4/4
 ✔ nginx Pulled                                                                                                                                                                                                                                     9.6s 
   ✔ e907afd6e256 Pull complete                                                                                                                                                                                                                     3.8s 
   ✔ 2b5bbb821f8e Pull complete                                                                                                                                                                                                                     3.6s 
   ✔ eb1c7aecab15 Pull complete                                                                                                                                                                                                                     1.5s 
[+] Running 1/3
 ✔ Network deployment_default  Created                                                                                                                                                                                                              0.0s 
 ⠴ Container fib-calculator    Created                                                                                                                                                                                                              0.5s 
 ⠋ Container nginx             Created                                                                                                                                                                                                              0.0s 
Attaching to fib-calculator, nginx
fib-calculator  | [2024-08-31 07:03:31 +0000] [1] [INFO] Starting gunicorn 23.0.0
fib-calculator  | [2024-08-31 07:03:31 +0000] [1] [INFO] Listening at: http://0.0.0.0:5002 (1)
fib-calculator  | [2024-08-31 07:03:31 +0000] [1] [INFO] Using worker: sync
fib-calculator  | [2024-08-31 07:03:31 +0000] [7] [INFO] Booting worker with pid: 7
fib-calculator  | [2024-08-31 07:03:31 +0000] [8] [INFO] Booting worker with pid: 8
fib-calculator  | [2024-08-31 07:03:31 +0000] [9] [INFO] Booting worker with pid: 9
fib-calculator  | [2024-08-31 07:03:31 +0000] [10] [INFO] Booting worker with pid: 10
```
访问http://0.0.0.0:5002/calculate/5  
得到结果: your entered number is: 5, and the fibonacci number is: 5


启动Flask、Nginx、postgres、celery

    docker-compose up

```text
(.venv) ➜  deployment git:(main) ✗ docker-compose up
WARN[0000] /Users/lijiachang/code/rust/flask_with_rust/deployment/docker-compose.yml: `version` is obsolete 
[+] Running 15/1
 ✔ postgres Pulled                                                                                                                                                                                                                                 14.5s 
[+] Running 2/3
 ✔ Container fib-calculator    Running                                                                                                                                                                                                              0.0s 
 ⠦ Container fib-dev-postgres  Created                                                                                                                                                                                                              0.6s 
 ✔ Container nginx             Created                                                                                                                                                                                                              0.0s 
Attaching to fib-calculator, fib-dev-postgres, nginx
fib-dev-postgres  | The files belonging to this database system will be owned by user "postgres".
fib-dev-postgres  | This user must also own the server process.
fib-dev-postgres  | 
fib-dev-postgres  | The database cluster will be initialized with locale "en_US.utf8".
fib-dev-postgres  | The default database encoding has accordingly been set to "UTF8".
fib-dev-postgres  | The default text search configuration will be set to "english".
fib-dev-postgres  | 
fib-dev-postgres  | Data page checksums are disabled.
fib-dev-postgres  | 
fib-dev-postgres  | fixing permissions on existing directory /var/lib/postgresql/data ... ok
fib-dev-postgres  | creating subdirectories ... ok
fib-dev-postgres  | selecting default max_connections ... 100
fib-dev-postgres  | selecting default shared_buffers ... 128MB
fib-dev-postgres  | selecting dynamic shared memory implementation ... posix
fib-dev-postgres  | creating configuration files ... ok
fib-dev-postgres  | running bootstrap script ... ok
fib-dev-postgres  | performing post-bootstrap initialization ... ok
fib-dev-postgres  | syncing data to disk ... ok
fib-dev-postgres  | 
fib-dev-postgres  | Success. You can now start the database server using:
fib-dev-postgres  | 
fib-dev-postgres  |     pg_ctl -D /var/lib/postgresql/data -l logfile start
fib-dev-postgres  | 
fib-dev-postgres  | 
fib-dev-postgres  | WARNING: enabling "trust" authentication for local connections
fib-dev-postgres  | You can change this by editing pg_hba.conf or using the option -A, or
fib-dev-postgres  | --auth-local and --auth-host, the next time you run initdb.
fib-dev-postgres  | waiting for server to start....2024-08-31 13:00:30.958 UTC [42] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
fib-dev-postgres  | 2024-08-31 13:00:30.963 UTC [43] LOG:  database system was shut down at 2024-08-31 13:00:30 UTC
fib-dev-postgres  | 2024-08-31 13:00:30.965 UTC [42] LOG:  database system is ready to accept connections
fib-dev-postgres  |  done
fib-dev-postgres  | server started
fib-dev-postgres  | CREATE DATABASE
fib-dev-postgres  | 
fib-dev-postgres  | 
fib-dev-postgres  | /usr/local/bin/docker-entrypoint.sh: ignoring /docker-entrypoint-initdb.d/*
fib-dev-postgres  | 
fib-dev-postgres  | waiting for server to shut down...2024-08-31 13:00:31.322 UTC [42] LOG:  received fast shutdown request
fib-dev-postgres  | .2024-08-31 13:00:31.323 UTC [42] LOG:  aborting any active transactions
fib-dev-postgres  | 2024-08-31 13:00:31.325 UTC [42] LOG:  background worker "logical replication launcher" (PID 49) exited with exit code 1
fib-dev-postgres  | 2024-08-31 13:00:31.325 UTC [44] LOG:  shutting down
fib-dev-postgres  | 2024-08-31 13:00:31.332 UTC [42] LOG:  database system is shut down
fib-dev-postgres  |  done
fib-dev-postgres  | server stopped
fib-dev-postgres  | 
fib-dev-postgres  | PostgreSQL init process complete; ready for start up.
fib-dev-postgres  | 
fib-dev-postgres  | 2024-08-31 13:00:31.442 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
fib-dev-postgres  | 2024-08-31 13:00:31.442 UTC [1] LOG:  listening on IPv6 address "::", port 5432
fib-dev-postgres  | 2024-08-31 13:00:31.445 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
fib-dev-postgres  | 2024-08-31 13:00:31.454 UTC [60] LOG:  database system was shut down at 2024-08-31 13:00:31 UTC
fib-dev-postgres  | 2024-08-31 13:00:31.457 UTC [1] LOG:  database system is ready to accept connections
```

生成迁移文件  
```text
(.venv) ➜  src git:(main) ✗ alembic revision --autogenerate -m create-fib-entry
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'fib_entries'
  Generating /Users/lijiachang/code/rust/flask_with_rust/src/alembic/versions/247189195619_create_fib_entry.py ...  done
```
如果需要迁移数据库，执行alembic upgrade head  
如果需要回滚数据库，执行alembic downgrade -1
```text
(.venv) ➜  src git:(main) ✗ alembic upgrade head
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 247189195619, create-fib-entry
```
可以看到数据库迁移系统可以正常工作  

把上面的修改同步到docker中  
```text
docker build . -t flask-fib
docker-compose up 
docker exec -it fib-calculator alembic upgrade head  # 在docker-compose运行的同时，执行迁移
```

连续访问两次计算请求,可以看到第二次是从数据库中获取的  
http://127.0.0.1:5002/calculate_v2/12  
your entered number is: 12, which has a fibonacci number of: 144  
http://127.0.0.1:5002/calculate_v2/12  
your entered number is: 12, which has an existing fibonacci number of: 144  


## 使用Celery异步处理计算任务
```text
(.venv) ➜  deployment git:(main) ✗ docker-compose up                  
[+] Running 4/5
 ✔ Container main-dev-redis    Running                                                                                                                                                                                                              0.0s 
 ✔ Container fib-dev-postgres  Running                                                                                                                                                                                                              0.0s 
 ✔ Container fib-calculator    Running                                                                                                                                                                                                              0.0s 
 ✔ Container nginx             Created                                                                                                                                                                                                              0.0s 
 ⠹ Container fib-worker        Recreated                                                                                                                                                                                                            0.3s 
Attaching to fib-calculator, fib-dev-postgres, fib-worker, main-dev-redis, nginx
fib-worker        | /usr/local/lib/python3.10/site-packages/celery/platforms.py:829: SecurityWarning: You're running the worker with superuser privileges: this is
fib-worker        | absolutely not recommended!
fib-worker        | 
fib-worker        | Please specify a different user using the --uid option.
fib-worker        | 
fib-worker        | User information: uid=0 euid=0 gid=0 egid=0
fib-worker        | 
fib-worker        |   warnings.warn(SecurityWarning(ROOT_DISCOURAGED.format(
fib-worker        |  
fib-worker        |  -------------- celery@e0c3e7871c4e v5.4.0 (opalescent)
fib-worker        | --- ***** ----- 
fib-worker        | -- ******* ---- Linux-6.6.22-linuxkit-aarch64-with-glibc2.36 2024-09-01 08:09:41
fib-worker        | - *** --- * --- 
fib-worker        | - ** ---------- [config]
fib-worker        | - ** ---------- .> app:         __main__:0xffffb7791870
fib-worker        | - ** ---------- .> transport:   redis://main_cache:6379/0
fib-worker        | - ** ---------- .> results:     redis://main_cache:6379/0
fib-worker        | - *** --- * --- .> concurrency: 4 (prefork)
fib-worker        | -- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
fib-worker        | --- ***** ----- 
fib-worker        |  -------------- [queues]
fib-worker        |                 .> celery           exchange=celery(direct) key=celery
fib-worker        |                 
fib-worker        | 
fib-worker        | [tasks]
fib-worker        |   . task_queue.fib_calc_task.calculate_fib
fib-worker        | 
fib-worker        | [2024-09-01 08:09:41,961: WARNING/MainProcess] /usr/local/lib/python3.10/site-packages/celery/worker/consumer/consumer.py:508: CPendingDeprecationWarning: The broker_connection_retry configuration setting will no longer determine
fib-worker        | whether broker connection retries are made during startup in Celery 6.0 and above.
fib-worker        | If you wish to retain the existing behavior for retrying connections on startup,
fib-worker        | you should set broker_connection_retry_on_startup to True.
fib-worker        |   warnings.warn(
fib-worker        | 
fib-worker        | [2024-09-01 08:09:41,970: INFO/MainProcess] Connected to redis://main_cache:6379/0
fib-worker        | [2024-09-01 08:09:41,970: WARNING/MainProcess] /usr/local/lib/python3.10/site-packages/celery/worker/consumer/consumer.py:508: CPendingDeprecationWarning: The broker_connection_retry configuration setting will no longer determine
fib-worker        | whether broker connection retries are made during startup in Celery 6.0 and above.
fib-worker        | If you wish to retain the existing behavior for retrying connections on startup,
fib-worker        | you should set broker_connection_retry_on_startup to True.
fib-worker        |   warnings.warn(
fib-worker        | 
fib-worker        | [2024-09-01 08:09:41,973: INFO/MainProcess] mingle: searching for neighbors
fib-worker        | [2024-09-01 08:09:42,983: INFO/MainProcess] mingle: all alone
fib-worker        | [2024-09-01 08:09:43,006: INFO/MainProcess] celery@e0c3e7871c4e ready.
fib-calculator    | 2024-09-01 08:10:18,733 INFO sqlalchemy.engine.Engine select pg_catalog.version()
fib-calculator    | 2024-09-01 08:10:18,733 INFO sqlalchemy.engine.Engine [raw sql] {}
fib-calculator    | 2024-09-01 08:10:18,736 INFO sqlalchemy.engine.Engine select current_schema()
fib-calculator    | 2024-09-01 08:10:18,736 INFO sqlalchemy.engine.Engine [raw sql] {}
fib-calculator    | 2024-09-01 08:10:18,738 INFO sqlalchemy.engine.Engine show standard_conforming_strings
fib-calculator    | 2024-09-01 08:10:18,738 INFO sqlalchemy.engine.Engine [raw sql] {}
fib-calculator    | 2024-09-01 08:10:18,738 INFO sqlalchemy.engine.Engine BEGIN (implicit)
fib-calculator    | 2024-09-01 08:10:18,741 INFO sqlalchemy.engine.Engine SELECT fib_entries.id AS fib_entries_id, fib_entries.input_number AS fib_entries_input_number, fib_entries.calculated_number AS fib_entries_calculated_number 
fib-calculator    | FROM fib_entries 
fib-calculator    | WHERE fib_entries.input_number = %(input_number_1)s
fib-calculator    | 2024-09-01 08:10:18,741 INFO sqlalchemy.engine.Engine [generated in 0.00014s] {'input_number_1': 15}
fib-calculator    | 2024-09-01 08:10:18,743 INFO sqlalchemy.engine.Engine ROLLBACK
fib-calculator    | 2024-09-01 08:10:27,504 INFO sqlalchemy.engine.Engine BEGIN (implicit)
fib-calculator    | 2024-09-01 08:10:27,506 INFO sqlalchemy.engine.Engine SELECT fib_entries.id AS fib_entries_id, fib_entries.input_number AS fib_entries_input_number, fib_entries.calculated_number AS fib_entries_calculated_number 
fib-calculator    | FROM fib_entries 
fib-calculator    | WHERE fib_entries.input_number = %(input_number_1)s
fib-calculator    | 2024-09-01 08:10:27,506 INFO sqlalchemy.engine.Engine [cached since 8.765s ago] {'input_number_1': 15}
fib-calculator    | 2024-09-01 08:10:27,510 INFO sqlalchemy.engine.Engine ROLLBACK
fib-calculator    | 2024-09-01 08:10:57,843 INFO sqlalchemy.engine.Engine BEGIN (implicit)
fib-calculator    | 2024-09-01 08:10:57,845 INFO sqlalchemy.engine.Engine SELECT fib_entries.id AS fib_entries_id, fib_entries.input_number AS fib_entries_input_number, fib_entries.calculated_number AS fib_entries_calculated_number 
fib-calculator    | FROM fib_entries 
fib-calculator    | WHERE fib_entries.input_number = %(input_number_1)s
fib-calculator    | 2024-09-01 08:10:57,845 INFO sqlalchemy.engine.Engine [cached since 39.1s ago] {'input_number_1': 32}
fib-calculator    | 2024-09-01 08:10:57,950 INFO sqlalchemy.engine.Engine ROLLBACK
fib-worker        | [2024-09-01 08:10:57,963: INFO/MainProcess] Task task_queue.fib_calc_task.calculate_fib[03682898-55fe-4c6f-819e-b11067677b3c] received
fib-worker        | 2024-09-01 08:10:59,307 INFO sqlalchemy.engine.Engine select pg_catalog.version()
fib-worker        | 2024-09-01 08:10:59,308 INFO sqlalchemy.engine.Engine [raw sql] {}
fib-worker        | [2024-09-01 08:10:59,307: INFO/ForkPoolWorker-4] select pg_catalog.version()
fib-worker        | [2024-09-01 08:10:59,308: INFO/ForkPoolWorker-4] [raw sql] {}
fib-worker        | 2024-09-01 08:10:59,312 INFO sqlalchemy.engine.Engine select current_schema()
fib-worker        | 2024-09-01 08:10:59,312 INFO sqlalchemy.engine.Engine [raw sql] {}
fib-worker        | [2024-09-01 08:10:59,312: INFO/ForkPoolWorker-4] select current_schema()
fib-worker        | [2024-09-01 08:10:59,312: INFO/ForkPoolWorker-4] [raw sql] {}
fib-worker        | [2024-09-01 08:10:59,314: INFO/ForkPoolWorker-4] show standard_conforming_strings
fib-worker        | [2024-09-01 08:10:59,314: INFO/ForkPoolWorker-4] [raw sql] {}
fib-worker        | 2024-09-01 08:10:59,314 INFO sqlalchemy.engine.Engine show standard_conforming_strings
fib-worker        | 2024-09-01 08:10:59,314 INFO sqlalchemy.engine.Engine [raw sql] {}
fib-worker        | 2024-09-01 08:10:59,317 INFO sqlalchemy.engine.Engine BEGIN (implicit)
fib-worker        | [2024-09-01 08:10:59,317: INFO/ForkPoolWorker-4] BEGIN (implicit)
fib-worker        | 2024-09-01 08:10:59,334 INFO sqlalchemy.engine.Engine INSERT INTO fib_entries (input_number, calculated_number) VALUES (%(input_number)s, %(calculated_number)s) RETURNING fib_entries.id
fib-worker        | [2024-09-01 08:10:59,334: INFO/ForkPoolWorker-4] INSERT INTO fib_entries (input_number, calculated_number) VALUES (%(input_number)s, %(calculated_number)s) RETURNING fib_entries.id
fib-worker        | 2024-09-01 08:10:59,335 INFO sqlalchemy.engine.Engine [generated in 0.00046s] {'input_number': 32, 'calculated_number': 2178309}
fib-worker        | [2024-09-01 08:10:59,335: INFO/ForkPoolWorker-4] [generated in 0.00046s] {'input_number': 32, 'calculated_number': 2178309}
fib-worker        | [2024-09-01 08:10:59,340: INFO/ForkPoolWorker-4] COMMIT
fib-worker        | 2024-09-01 08:10:59,340 INFO sqlalchemy.engine.Engine COMMIT
fib-worker        | [2024-09-01 08:10:59,350: INFO/ForkPoolWorker-4] Task task_queue.fib_calc_task.calculate_fib[03682898-55fe-4c6f-819e-b11067677b3c] succeeded in 1.3337355839999958s: None
fib-calculator    | 2024-09-01 08:12:36,892 INFO sqlalchemy.engine.Engine select pg_catalog.version()
fib-calculator    | 2024-09-01 08:12:36,892 INFO sqlalchemy.engine.Engine [raw sql] {}
fib-calculator    | 2024-09-01 08:12:36,896 INFO sqlalchemy.engine.Engine select current_schema()
fib-calculator    | 2024-09-01 08:12:36,896 INFO sqlalchemy.engine.Engine [raw sql] {}
fib-calculator    | 2024-09-01 08:12:36,897 INFO sqlalchemy.engine.Engine show standard_conforming_strings
fib-calculator    | 2024-09-01 08:12:36,897 INFO sqlalchemy.engine.Engine [raw sql] {}
fib-calculator    | 2024-09-01 08:12:36,898 INFO sqlalchemy.engine.Engine BEGIN (implicit)
fib-calculator    | 2024-09-01 08:12:36,907 INFO sqlalchemy.engine.Engine SELECT fib_entries.id AS fib_entries_id, fib_entries.input_number AS fib_entries_input_number, fib_entries.calculated_number AS fib_entries_calculated_number 
fib-calculator    | FROM fib_entries 
fib-calculator    | WHERE fib_entries.input_number = %(input_number_1)s
fib-calculator    | 2024-09-01 08:12:36,907 INFO sqlalchemy.engine.Engine [generated in 0.00031s] {'input_number_1': 32}
fib-calculator    | 2024-09-01 08:12:36,912 INFO sqlalchemy.engine.Engine ROLLBACK

```

连续访问两次 大数字的计算请求, 使用Celery异步处理  
http://0.0.0.0:5002/calculate_v3/32  
your entered number is: 32, which is too large to calculate immediately, and has been sent to the queue  
http://0.0.0.0:5002/calculate_v3/32  
your entered number is: 32, which has an existing fibonacci number of: 2178309  


使用Rust构建新的v4视图后  
现在可以选择python或Rust计算  
http://0.0.0.0:5002/calculate_v4/python/17  
your entered number is: 17, which has a fibonacci number of: 1597, took 0.0003750324249267578 seconds  
http://0.0.0.0:5002/calculate_v4/rust/18  
your entered number is: 18, which has a fibonacci number of: 2584, took 0.0003132820129394531 seconds  
可以看到尽管Rust请求的数字更大，但是速度比Python更快