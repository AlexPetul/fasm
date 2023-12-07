# pull official base image
FROM node:14-alpine

# install app dependencies
COPY ./package.json .
RUN npm install --silent
RUN npm install react-scripts@4.0.0 -g --silent

# add app
COPY . /app

WORKDIR /app

# Expose port
EXPOSE 3000

# start app
CMD ["npm", "start"]
