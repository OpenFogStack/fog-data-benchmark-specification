FROM python:3.9-slim

RUN pip install tensorflow==2.12.0 tensorflow-io==0.32.0 scikit-learn==1.2.2

ENTRYPOINT [ "python3" ]