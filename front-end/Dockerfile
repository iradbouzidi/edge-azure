# pull official base image
FROM arm32v7/node:buster-slim

# set working directory
WORKDIR /usr/src/app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /usr/src/app/node_modules/.bin:$PATH

# install app dependencies
COPY package.json ./
COPY package-lock.json ./
RUN npm install --silent

# add app
COPY . ./

# expose port
EXPOSE 3000

# start app
CMD ["npm", "start"]