## Build the app
FROM node:21-alpine as build

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY index.html vite.config.js jsconfig.json ./
COPY src src
COPY public public


RUN npm run build

## Serve the app
FROM nginx:1.25-alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["/usr/sbin/nginx", "-g", "daemon off;"]