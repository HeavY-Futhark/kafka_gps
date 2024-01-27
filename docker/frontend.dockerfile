FROM node:14
WORKDIR /app
COPY ./frontend/package*.json .
RUN npm install
COPY ./frontend/* .
EXPOSE 8000
ENV NODE_ENV=production
CMD ["npm", "run", "start"]

