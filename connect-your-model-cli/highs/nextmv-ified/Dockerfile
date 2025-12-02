FROM ubuntu:22.04

# Install build dependencies.
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory.
WORKDIR /app

# Build HiGHS.
RUN git clone https://github.com/ERGO-Code/HiGHS.git
WORKDIR /app/HiGHS
RUN cmake -S. -B build 
RUN cmake --build build --parallel

# Download nlohmann/json header.
WORKDIR /app
RUN mkdir -p nlohmann
RUN curl -L https://github.com/nlohmann/json/releases/download/v3.11.3/json.hpp \
        -o nlohmann/json.hpp

# Copy source code.
COPY main.cpp /app/

# Compile the application.
RUN g++ -std=c++11 main.cpp -o main \
        -I. \
        -I./HiGHS/highs \
        -I./HiGHS/build \
        -L./HiGHS/build/lib -lhighs
