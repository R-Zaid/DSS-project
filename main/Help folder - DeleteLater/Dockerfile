#Dockerfile, Image , Container 
#Python versie van mijn laptop 
#

#toevoegen van de python file in container
#ADD vehicles.py . 

#nu de libraries die in vehicles.py zitten hierin gooien
#RUN pip install requests pandas matplotlib

#Specify entry command
#CMD [ "python", "./vehicles.py" ]


# docker image maken, in terminal run ik: docker build -t python-veh . 
#   hierna ook met "." runnen in terminal


# Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# alleen 1 file aan het testen nu
COPY vehicles.py .

# lib's installeren
RUN pip install --no-cache-dir flask requests pandas plotly matplotlib gunicorn


#Make port 80 available to the world outside this container (Optional, only for web apps) # GeeksforGeeks
EXPOSE 8080

# start Flask-app via gunicorn (
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
