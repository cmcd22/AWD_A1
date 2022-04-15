FROM python:3.7-alpine
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . /src
WORKDIR /src

#Uncomment just the next 2  lines to run your application in Docker container
#EXPOSE 8080
#CMD python server3.py 8080


#Uncomment just the next line when you want to deploy your container on Heroku
CMD python server3.py $PORT
