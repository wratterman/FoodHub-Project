FROM python:3.8
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client

COPY startup_script.sh .
RUN chmod a+x startup_script.sh
CMD ["./startup_script.sh"]