FROM python:3.10.14

WORKDIR /app
ADD . /app

RUN rm ./config.yml
RUN mv live_config.yml ./config.yml

RUN apt-get update && apt-get install -y python3-dev gcc  # 能够编译Rust代码并使用二进制文件


# 安装Rust环境
#RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | bash -s -- -y -profile minimal -no-modify-path
# 解释一下这个命令：
#-s: 这个选项告诉 Bash 从标准输入读取命令。在这个上下文中，它用于接收通过管道传递来的 Rustup 安装脚本。
#--: 这是一个特殊参数，表示后面的所有内容都是传递给脚本的参数，而不是 Bash 的选项。
#-y: 这是传递给 Rustup 安装脚本的参数，表示"yes"，自动回答所有提示为"是"。这使得安装过程成为非交互式的，适合在自动化脚本（如 Dockerfile）中使用。
#-profile: 它指定了要安装的 Rust 工具链配置文件。 minimal: 只安装 rustc、rust-std 和 cargo。 default: 安装默认组件（包括 rustfmt 和 clippy）。 complete: 安装所有可用的组件。
#-no-modify-path: 它告诉 Rustup 不要修改 PATH 环境变量。这是因为在 Docker 容器中，我们不需要修改 PATH，因为我们可以直接使用绝对路径来调用 Rust 工具链。

# 尝试安装 Rust 并捕获输出
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | bash -s -- -y --default-toolchain stable --profile minimal -v > rustup_log.txt 2>&1 || (cat rustup_log.txt && exit 1)

# 检查安装日志
RUN cat rustup_log.txt

# 设置 Rust 环境变量
ENV PATH="/root/.cargo/bin:${PATH}"
ENV RUSTUP_HOME=/root/.rustup
ENV CARGO_HOME=/root/.cargo
# 调试：检查 Rust 安装
RUN ls -la /root/.cargo
RUN ls -la /root/.rustup
RUN echo $PATH

# 验证 Rust 安装
RUN . $HOME/.cargo/env && rustc --version && cargo --version


RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt
RUN pip install -r git_repos.txt

EXPOSE 5002
CMD ["gunicorn", "-w 4", "-b", "0.0.0.0:5002", "app:app"]
# 四个worker，监听5002端口，app:app是启动的Flask应用，表示应用程序在app.py文件中，应用程序是变量名app下的Flask实例