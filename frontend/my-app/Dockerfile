FROM node:14
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 8080
ENV NODE_ENV=production
CMD ["npm", "start", "--", "--host", "0.0.0.0"]

