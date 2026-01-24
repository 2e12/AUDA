FROM node:25-slim AS builder

COPY web /web/

ARG AUDA_BACKEND_URL

WORKDIR /web

RUN yarn install

RUN yarn nuxt generate

RUN ls -hal

FROM nginx:alpine

COPY --from=builder /web/.output/public/ /usr/share/nginx/html
