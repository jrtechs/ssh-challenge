#choose the base image for the build
FROM node:10
RUN mkdir -p /home/node/app && chown -R node:node /home/node/app
WORKDIR /home/node/app

#copies in the node files
COPY package*.json ./
COPY *.js ./
COPY *.html ./

# permission stuff
RUN chmod 755 package.json
RUN chmod 755 index.js

# Runs the node app
USER node
RUN npm install
EXPOSE 7777
CMD [ "npm", "start" ]
