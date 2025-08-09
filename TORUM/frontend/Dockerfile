# Use Node.js as the base image
FROM node:20-alpine

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy the rest of the application code
COPY . .

ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
RUN npm run build

# Expose the port the app runs on
EXPOSE 5173

# Start the React development server
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "5173"]