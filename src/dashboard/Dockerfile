FROM node:18-alpine

WORKDIR /src/dashboard

COPY package.json package-lock.json ./
RUN npm ci


CMD ["npm", "run", "dev"]
