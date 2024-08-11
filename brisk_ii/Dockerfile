# STAGE 1: build rust project with python bindings
FROM python:3.12.5-bookworm AS rust_build

RUN apt-get -y update
RUN apt -y install rust-all

COPY requirements-build.txt requirements-build.txt
RUN pip3 install -r requirements-build.txt

COPY /src /src
COPY Cargo.toml Cargo.toml
COPY pyproject.toml pyproject.toml 
RUN maturin build

# STAGE 2: build main image
FROM python:3.12.5-bookworm AS main
COPY --from=rust_build /target/wheels/game_core-0.1.0-cp312-cp312-manylinux_2_34_x86_64.whl game_core-0.1.0-cp312-cp312-manylinux_2_34_x86_64.whl

RUN pip3 install game_core-0.1.0-cp312-cp312-manylinux_2_34_x86_64.whl
COPY /python/brisk /python/brisk

CMD ["python3", "-m", "python.brisk.main"]