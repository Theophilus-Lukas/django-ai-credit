FROM python

RUN apt-get update

# INSTALL PREREQUSITES
RUN pip install -U pip

RUN apt-get install -y --force-yes libboost-all-dev

RUN apt-get update -y

RUN apt-get install build-essential cmake pkg-config -y --force-yes

RUN apt-get install tesseract-ocr -y --force-yes

RUN apt-get install tesseract-ocr-ind -y --force-yes

# INSTALL PYTHON TOOLS
WORKDIR /app

COPY requirements.txt ./

RUN pip3 install wheel

RUN pip3 install cmake

RUN pip3 install -U pip wheel cmake

RUN pip3 install setuptools

RUN pip3 install opencv-python

RUN pip3 install numpy scipy matplotlib scikit-image scikit-learn ipython 

RUN pip3 install dlib

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python3", "manage.py", "runserver"]