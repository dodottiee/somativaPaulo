# Imagem base do Nginx
FROM nginx:alpine

# Remove a configuração padrão do Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copia sua configuração customizada
COPY default.conf /etc/nginx/conf.d/

# Copia seus arquivos HTML
COPY . /usr/share/nginx/html

# Exponha a porta 80
EXPOSE 80

# Comando padrão para rodar o Nginx
CMD ["nginx", "-g", "daemon off;"]
