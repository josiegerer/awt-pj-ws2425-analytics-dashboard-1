-- init-scripts/init.sql
CREATE USER lrsql_user WITH CREATEDB PASSWORD 'lrsql_password';
CREATE DATABASE lrsql_db OWNER lrsql_user;
\c lrsql_db
CREATE SCHEMA IF NOT EXISTS lrsql;
ALTER ROLE lrsql_user SET search_path TO lrsql,public;
