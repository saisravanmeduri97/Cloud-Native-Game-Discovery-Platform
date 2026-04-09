FROM node:20-alpine AS deps

WORKDIR /app

COPY package*.json /app/
RUN npm install

FROM node:20-alpine AS builder

WORKDIR /app

COPY --from=deps /app/node_modules /app/node_modules
COPY . /app

RUN npm run build

FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production

COPY --from=builder /app /app

EXPOSE 3000

CMD ["npm", "run", "start"]
