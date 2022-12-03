FROM ubuntu:18.04


apt-get install python3 python3-pip software-properties-common
add-apt-repository ppa:deadsnakes/ppa
apt-get install python3.7

# Make python 3.7 the default
RUN echo "alias python=python3.7" >> ~/.bashrc
RUN export PATH=${PATH}:/usr/bin/python3.7
RUN /bin/bash -c "source ~/.bashrc"

# Install pip
RUN apt install python3-pip -y
RUN python -m pip install --upgrade pip
RUN pip install requests
RUN pip install lxml

COPY . .
RUN python main.py
