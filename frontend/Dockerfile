FROM node:20

WORKDIR /app

COPY package*.json ./
RUN npm install

# Bundle app source inside Docker image
COPY . .

# Build your Next.js application
RUN npm run build

# Set the command to start the node server
CMD ["npm", "start"]

