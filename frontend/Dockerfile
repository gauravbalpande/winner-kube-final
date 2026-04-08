# ============================================================
# Frontend Dockerfile — Multi-Stage (Dev → Build → Production)
# Optimized: pinned nginx version, --no-cache npm, non-root nginx
# ============================================================

# Stage 1: Development (Vite dev server, hot-reload)
FROM node:18-alpine AS development
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

# Stage 2: Build (production bundle)
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
# --no-cache: fresh install; npm ci: reproducible from lock file
RUN npm ci --no-cache
COPY . .
RUN npm run build

# Stage 3: Production (nginx serving static assets)
FROM nginx:1.27-alpine AS production
# Copy build artifacts
COPY --from=build /app/dist /usr/share/nginx/html
# Custom nginx config (includes API proxy + security headers)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Run nginx as non-root (listen on 8080 internally, mapped to 80 by K8s service)
RUN chown -R nginx:nginx /usr/share/nginx/html \
    && chown -R nginx:nginx /var/cache/nginx \
    && chown -R nginx:nginx /var/log/nginx \
    && touch /var/run/nginx.pid \
    && chown -R nginx:nginx /var/run/nginx.pid

USER nginx
EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/health || exit 1

CMD ["nginx", "-g", "daemon off;"]