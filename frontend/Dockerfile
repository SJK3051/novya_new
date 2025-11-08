# ---------- Build Stage ----------
FROM node:18 AS build

WORKDIR /app

# Copy dependency files first for better caching
COPY package*.json ./

# Install dependencies ignoring peer version conflicts
RUN npm install --legacy-peer-deps

# Copy the remaining files
COPY . .

# Build the production-ready React app
RUN npm run build

# ---------- Serve Stage ----------
FROM nginx:alpine

# Copy the build output from the previous stage
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80 for the web server
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]

