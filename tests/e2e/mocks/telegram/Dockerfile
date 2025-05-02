FROM node:18-slim

RUN apt-get update && apt-get install -y wget && apt-get clean

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["node", "server.js"]
