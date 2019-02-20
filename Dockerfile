FROM postgres:10.7
WORKDIR /var/lib/postgres
EXPOSE 5432


FROM python:3.7.2
COPY . /home/app
WORKDIR /home/app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "run.py"]
