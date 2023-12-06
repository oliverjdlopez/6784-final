FROM python:3.8-slim-bullseye

WORKDIR /demo

COPY . /demo

RUN pip install -r requirements.txt

# Downloading and preparing the dataset
RUN apt update
RUN apt install -y wget
RUN wget https://zenodo.org/record/7589131/files/21-05.tar
RUN tar xfv 21-05.tar
RUN rm 21-05.tar
RUN wget https://zenodo.org/record/7589131/files/21-06.tar
RUN tar xfv 21-06.tar
RUN rm 21-06.tar
RUN wget https://zenodo.org/record/7589320/files/21-07.tar
RUN tar xfv 21-07.tar
RUN rm 21-07.tar
RUN wget https://zenodo.org/record/7589320/files/21-08.tar
RUN tar xfv 21-08.tar
RUN rm 21-08.tar
RUN mkdir dataset
RUN mv year_month=21-05 dataset
RUN mv year_month=21-06 dataset
RUN mv year_month=21-07 dataset
RUN mv year_month=21-08 dataset

CMD ["jupyter-notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]