FROM python:3.9

RUN apt-get update

# INSTALL PREREQUSITES
RUN pip install -U pip

RUN apt-get update -y

RUN apt-get install build-essential cmake pkg-config -y --force-yes

RUN apt-get install -y libx11-dev

RUN apt-get install -y libatlas-base-dev

RUN apt-get install -y libgtk-3-dev

RUN apt-get install -y --force-yes libboost-python-dev

RUN apt-get install tesseract-ocr -y --force-yes

RUN apt-get install tesseract-ocr-ind -y --force-yes

RUN apt install g++
# INSTALL PYTHON TOOLS
WORKDIR /app

COPY requirements.txt ./

RUN pip install wheel

RUN pip install cmake

#RUN pip3 install -U pip wheel cmake

RUN pip install setuptools

RUN pip install opencv-python

RUN pip install numpy scipy matplotlib scikit-image scikit-learn ipython 

RUN pip install dlib
#RUN pip install https://github.com/jloh02/dlib/releases/download/v19.22/dlib-19.22.99-cp310-cp310-win_amd64.whl

#RUN pip install https://pypi.python.org/packages/da/06/bd3e241c4eb0a662914b3b4875fc52dd176a9db0d4a2c915ac2ad8800e9e/dlib-19.7.0-cp36-cp36m-win_amd64.whl#md5=b7330a5b2d46420343fbed5df69e6a3f

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python3", "manage.py", "runserver"]