FROM arm32v7/node:alpine as builder

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --prod

# Only copy over the node pieces we need from the above image
FROM arm32v7/node:alpine

WORKDIR /app

COPY --from=builder /app .
COPY . .

EXPOSE 8000
CMD ["node", "index.js"]