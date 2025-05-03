FROM node:22

WORKDIR /app
RUN npm install -g create-docusaurus

COPY package.json package-lock.json ./
RUN npm install

CMD ["bash"]
