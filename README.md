# flask_with_rust
Injecting Rust into a Python Flask App. 将Rust注入到Python Flask应用程序

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
