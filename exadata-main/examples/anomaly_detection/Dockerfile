FROM python:3.8-slim-bullseye

WORKDIR /demo

COPY requirements.txt /demo
COPY demo.ipynb /demo
COPY 388.parquet /demo

RUN pip install -r requirements.txt

CMD ["jupyter-notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]
