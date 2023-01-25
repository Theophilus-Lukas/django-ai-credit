FROM python:3.9

ENV PYTHONUNBUFFERED=1

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

RUN pip install setuptools

RUN pip install opencv-python

RUN pip install numpy scipy matplotlib scikit-image scikit-learn ipython 

RUN pip install dlib

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "8000"]