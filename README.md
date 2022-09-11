https://docs.dask.org/en/stable/

 && alembic upgrade head && python run.py 


# criar as imagens
docker-compose build
# subir os containers
docker-compose up -d
# rodar as migrations
docker run --rm crawler_app sh
exec -it crawler_app alembic upgrade
# rodar o crawler

# derrubar os containers