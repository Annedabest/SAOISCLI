# SAOIS Website - Static Site Dockerfile
FROM nginx:alpine

# Copy website files to nginx html directory
COPY website/*.html /usr/share/nginx/html/

# Copy custom nginx config
COPY website/nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD wget -q --spider http://127.0.0.1/ || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
