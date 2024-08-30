# flask_with_rust
Injecting Rust into a Python Flask App. 将Rust注入到Python Flask应用程序

## 构建Python Flask应用程序
使用Nginx、数据库、Celery（实现消息总线）来构建一个Flask Web应用程序  
此消息总线将允许应用程序在返回Web http请求时在后台处理繁重的任务。  
Web应用程序和消息总线将会包装到Docker中，并部署到docker-compose

