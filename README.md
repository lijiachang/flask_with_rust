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