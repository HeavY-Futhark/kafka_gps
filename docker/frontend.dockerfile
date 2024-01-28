FROM node:14
WORKDIR /app
COPY ./frontend/package*.json .
RUN npm install
COPY ./frontend/ ./
ENV NODE_ENV=production
RUN npm run build
CMD ["npm", "run", "start", "--", "--host", "0.0.0.0"]

