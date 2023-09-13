FROM node:14-alpine
COPY . /main
WORKDIR /main
RUN npm install --production
CMD ["npm", "start"]
EXPOSE 3000