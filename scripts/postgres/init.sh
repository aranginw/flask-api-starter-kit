#!/bin/bash
set -e

POSTGRES_DB=${POSTGRES_DB:?You must set the POSTGRES_DB environment variable}
APPLICATION_POSTGRES_USER=${APPLICATION_POSTGRES_USER:?You must set the APPLICATION_POSTGRES_USER environment variable}
APPLICATION_POSTGRES_PW=${APPLICATION_POSTGRES_PW:?You must set the APPLICATION_POSTGRES_PW environment variable}
APPLICATION_POSTGRES_DB=${APPLICATION_POSTGRES_DB:?You must set the APPLICATION_POSTGRES_DB environment variable}

psql -v ON_ERROR_STOP=1 --username postgres --dbname ${POSTGRES_DB} <<-EOSQL
    CREATE ROLE application_admin_role NOSUPERUSER CREATEDB NOCREATEROLE NOLOGIN NOREPLICATION INHERIT;

    CREATE USER ${APPLICATION_POSTGRES_USER} WITH ENCRYPTED PASSWORD '${APPLICATION_POSTGRES_PW}';
    GRANT application_admin_role to ${APPLICATION_POSTGRES_USER};

    CREATE DATABASE ${APPLICATION_POSTGRES_DB};
    ALTER DATABASE ${APPLICATION_POSTGRES_DB} OWNER TO application_admin_role;
EOSQL

psql -v ON_ERROR_STOP=1 --username postgres --dbname ${APPLICATION_POSTGRES_DB} <<-EOSQL
    -- Prevent default permissions
    REVOKE ALL ON SCHEMA public from PUBLIC;

    -- Admin role
    GRANT CONNECT ON DATABASE ${APPLICATION_POSTGRES_DB} TO application_admin_role;
    GRANT ALL PRIVILEGES ON DATABASE ${APPLICATION_POSTGRES_DB} TO application_admin_role;
    GRANT ALL ON SCHEMA public TO application_admin_role;

    -- Extensions
    create extension pgcrypto;
EOSQL
