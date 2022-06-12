FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Configure multi-programming language environment
RUN sed -i 's/archive.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list \
    && apt-get update \
    # Install packages for compilation and repositories
    && apt-get install -y build-essential curl \
    # Install general packages
    ## C
    && apt-get install -y gcc \
    ## Fortran
    && apt-get install -y gfortran \
    ## Julia
    && apt-get install -y julia \
    ## Python
    && apt-get install -y python3 python3-numpy python3-numba \
    ## Rust
    && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
    && echo 'source $HOME/.cargo/env' >> $HOME/.bashrc \
    # Erase downloaded archive files
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
