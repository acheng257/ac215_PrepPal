FROM postgres:17

ENV PGPORT=5432
ENV POSTGRES_DB=preppal_db
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres

EXPOSE 5432

COPY schema.sql /docker-entrypoint-initdb.d/
# COPY mock_data.sql /docker-entrypoint-initdb.d/
