
FROM postgres:13.1-alpine
LABEL maintainer "Julio Zeferino <julioszeferino@gmail.com>"
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=enem
EXPOSE 5432