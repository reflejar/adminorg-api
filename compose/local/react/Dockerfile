# Pull de la imagen base
FROM node:14.1-alpine

# Seteado del directorio de trabajo
WORKDIR /app/frontend

# # PATH de node_modules
# ENV PATH /app/frontend/node_modules/.bin:$PATH

# # Copiado del package e instalacion
# COPY ./react/package.json ./
# COPY ./react/package-lock.json ./
# RUN npm --verbose install

# # Instalacion
COPY ./react ./

EXPOSE 3000

CMD ["npm", "start"]