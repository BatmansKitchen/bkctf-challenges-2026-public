FROM node:18-slim

RUN apt-get update && apt-get install -y \
    wget \
    curl \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY package*.json ./
RUN npm install --production

ENV PUPPETEER_CACHE_DIR=/home/node/.cache/puppeteer
ENV NODE_ENV=production

RUN mkdir -p /home/node/.cache/puppeteer \
    && npx puppeteer browsers install chrome

COPY app/ ./

COPY flag.txt /flag.txt

RUN mkdir -p /app/snapshots \
    && chmod 777 /app/snapshots \
    && chown -R node:node /app /home/node \
    && chmod 644 /flag.txt

EXPOSE 3000

USER node
CMD ["node", "server.js"]
