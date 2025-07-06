-- Database initialization script for E-CLARIA AI
-- This script works with the postgres user configured in docker-compose

-- Create extensions in the default database
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create a test database for testing purposes
CREATE DATABASE eclaria_test;

-- Grant all privileges on the test database to postgres user
GRANT ALL PRIVILEGES ON DATABASE eclaria_test TO postgres;

-- Connect to the test database and create extensions there too
\c eclaria_test;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Switch back to the main database
\c eclaria;

-- Set default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO postgres;
