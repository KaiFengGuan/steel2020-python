# FROM 219.216.80.32:8000/python-3.7.2:requirementsAdd
# FROM 219.216.81.96:6000/basic-python-image-tensorflow
FROM 202.118.21.236:5000/basic-python-image-tensorflow
# docker build -t pythontest .
WORKDIR /usr/src/app

COPY . .
# COPY ./config.txt /usr/src/app/config.txt

# RUN pip install 
RUN pip install umap-learn -i https://mirrors.ustc.edu.cn/pypi/web/simple
# RUN pip install Tensorflow

EXPOSE 5000

CMD ["gunicorn", "-c", "gunicorn.conf", "run:app"]
