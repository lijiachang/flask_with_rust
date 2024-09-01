FROM python:3.10.14

WORKDIR /app
ADD . /app

RUN rm ./config.yml
RUN mv live_config.yml ./config.yml

RUN apt-get update && apt-get install -y python3-dev gcc  # 能够编译Rust代码并使用二进制文件


# 安装Rust环境
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | bash -s -- -y --profile minimal
# 解释一下这个命令：
#-s: 这个选项告诉 Bash 从标准输入读取命令。在这个上下文中，它用于接收通过管道传递来的 Rustup 安装脚本。
#--: 这是一个特殊参数，表示后面的所有内容都是传递给脚本的参数，而不是 Bash 的选项。
#-y: 这是传递给 Rustup 安装脚本的参数，表示"yes"，自动回答所有提示为"是"。这使得安装过程成为非交互式的，适合在自动化脚本（如 Dockerfile）中使用。
#-profile: 它指定了要安装的 Rust 工具链配置文件。 minimal: 只安装 rustc、rust-std 和 cargo。 default: 安装默认组件（包括 rustfmt 和 clippy）。 complete: 安装所有可用的组件。

# 设置 Rust 环境变量
ENV PATH="/root/.cargo/bin:${PATH}"


RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt
RUN pip install -r git_repos.txt

EXPOSE 5002
CMD ["gunicorn", "-w 4", "-b", "0.0.0.0:5002", "app:app"]
# 四个worker，监听5002端口，app:app是启动的Flask应用，表示应用程序在app.py文件中，应用程序是变量名app下的Flask实例