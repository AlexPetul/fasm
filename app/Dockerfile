# pull official base image
FROM node:14-alpine

# set working directory
WORKDIR /app

# install app dependencies
COPY ./app/package.json .
RUN npm install --silent
RUN npm install react-scripts@4.0.0 -g --silent

# add app
COPY ./app .

# Expose port
EXPOSE 3000

# start app
CMD ["npm", "start"]
