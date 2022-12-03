FROM ubuntu:18.04


FROM python:3.7

RUN apt-get update

# Make python 3.7 the default
RUN echo "alias python=python3.7" >> ~/.bashrc
RUN export PATH=${PATH}:/usr/bin/python3.7
RUN /bin/bash -c "source ~/.bashrc"

# Install pip
RUN apt-get install -y python3-pip
RUN python -m pip install --upgrade pip
RUN pip install requests
RUN pip install lxml

WORKDIR /usr/app/src

COPY . .

CMD ["python", "main.py"]
