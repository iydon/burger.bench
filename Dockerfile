FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive \
    HOME=/root

SHELL ["/bin/bash", "-c"]

# Configure multi-programming language environment
RUN sed -i 's/archive.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list \
    && apt-get update \
    # Install packages for compilation and repositories
    && apt-get install -y build-essential curl \
    # Install general packages
    ## C
    && apt-get install -y gcc \
    ## Go
    && apt-get install -y golang-go \
    ## Fortran
    && apt-get install -y gfortran \
    ## Julia
    && apt-get install -y julia \
    ## Python
    && apt-get install -y python3 python3-numpy python3-numba \
    ## Rust
    && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
    && echo 'source $HOME/.cargo/env' >> $HOME/.bashrc \
    && source $HOME/.cargo/env \
    # Install Benchmarking tool(s)
    && cargo install hyperfine \
    # Erase downloaded archive files
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY Makefile $HOME/burger.bench/
COPY burger/ $HOME/burger.bench/burger/
COPY script/ $HOME/burger.bench/script/
