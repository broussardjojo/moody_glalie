FROM python:3.8
RUN mkdir /app
ADD . /app
WORKDIR app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"
EXPOSE 5001
CMD ["python", "resurety_homework/app_for_container.py"]