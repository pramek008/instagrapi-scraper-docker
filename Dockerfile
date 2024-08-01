FROM python:3.9-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install ngrok
RUN curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && \
    echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | tee /etc/apt/sources.list.d/ngrok.list && \
    apt-get update && apt-get install ngrok

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all Python files
COPY app/ app/

#copy csv account
COPY accounts.csv .

RUN mkdir -p sessions
COPY sessions/ sessions/

# Copy and set entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set the command to run the entrypoint script
CMD ["/entrypoint.sh"]
