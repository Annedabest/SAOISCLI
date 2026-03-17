# SAOIS Website - Static Site Dockerfile
FROM nginx:alpine

# Copy website files to nginx html directory
COPY website/*.html /usr/share/nginx/html/

# Copy custom nginx config
COPY website/nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
