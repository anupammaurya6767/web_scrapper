FROM ubuntu:18.04


FROM python:3.7

RUN apt-get update

# Make python 3.7 the default
RUN echo "alias python=python3.7" >> ~/.bashrc
RUN export PATH=${PATH}:/usr/bin/python3.7
RUN /bin/bash -c "source ~/.bashrc"

# Install pip
RUN apt-get install -y python3-pip && \
    python -m pip install --upgrade pip && \
    python -m pip install -r requirements.txt

WORKDIR /usr/app/src

COPY . .

CMD ["python", "sample.py"]
