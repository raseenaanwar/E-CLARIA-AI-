-- -- Database initialization script for E-CLARIA AI
-- -- This script creates the necessary database and user for the application

-- -- Create database if it doesn't exist
-- CREATE DATABASE IF NOT EXISTS eclaria_db;
-- CREATE DATABASE IF NOT EXISTS eclaria_test_db;

-- -- Create user if it doesn't exist
-- DO $$
-- BEGIN
--     IF NOT EXISTS (SELECT FROM pg_catalog.pg_user WHERE usename = 'eclaria_user') THEN
--         CREATE USER eclaria_user WITH PASSWORD 'eclaria_password';
--     END IF;
-- END
-- $$;

-- -- Grant privileges
-- GRANT ALL PRIVILEGES ON DATABASE eclaria_db TO eclaria_user;
-- GRANT ALL PRIVILEGES ON DATABASE eclaria_test_db TO eclaria_user;

-- -- Connect to the main database
-- \c eclaria_db;

-- -- Grant schema privileges
-- GRANT ALL ON SCHEMA public TO eclaria_user;
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO eclaria_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO eclaria_user;

-- -- Create extensions if needed
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- -- Connect to the test database
-- \c eclaria_test_db;

-- -- Grant schema privileges for test database
-- GRANT ALL ON SCHEMA public TO eclaria_user;
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO eclaria_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO eclaria_user;

-- -- Create extensions for test database
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- -- Set default privileges for future tables
-- ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO eclaria_user;
-- ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO eclaria_user;
-- Create user if not exists
DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles WHERE rolname = 'eclaria_user'
   ) THEN
      CREATE ROLE eclaria_user LOGIN PASSWORD 'eclaria_password';
   END IF;
END
$do$;

-- Note: Databases 'eclaria_db' and 'eclaria_test_db' will be created automatically by Docker
-- based on POSTGRES_DB environment variable. No need to create them here.

-- Create extensions in the default database (run inside the DB later if needed)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
