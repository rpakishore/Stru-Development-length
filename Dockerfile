#Set base image in Python 3.7
FROM python:3.7
MAINTAINER Arun rpakishore@gmail.com

#Set Working directory
WORKDIR /app

RUN pip3 install -r requirements.txt

#Expose Port 8501 for app to be run on
EXPOSE 8501

COPY . .

ENTRYPOINT ["streamlit", "run"]
CMD ["About.py"]