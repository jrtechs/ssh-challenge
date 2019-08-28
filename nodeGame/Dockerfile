#choose the base image for the build
FROM node:10
RUN mkdir -p /home/node/app && chown -R node:node /home/node/app
WORKDIR /home/node/app
COPY package*.json ./
COPY index.js ./
RUN chmod 755 package.json
RUN chmod 755 index.js
USER node
RUN npm install
RUN ls -l
#RUN ["chmod", "755", "your-script.sh"]
EXPOSE 7777
CMD [ "npm", "start" ]
