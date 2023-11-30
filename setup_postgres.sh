#!/bin/bash

# Define variables
DB_NAME="liv_test"
DB_USER="admin"
DB_PASSWORD="admin"

# Install Homebrew if not installed
if ! command -v brew &> /dev/null; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install PostgreSQL using Homebrew
brew install postgresql

# Start PostgreSQL service
brew services start postgresql

# Wait for PostgreSQL to start
sleep 3

# Create a database
createdb $DB_NAME

# Create a user and set a password
psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" $DB_NAME

# Grant necessary permissions
psql -c "ALTER ROLE $DB_USER SET client_encoding TO 'utf8';" $DB_NAME
psql -c "ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';" $DB_NAME
psql -c "ALTER ROLE $DB_USER SET timezone TO 'UTC';" $DB_NAME
psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;" $DB_NAME

echo "PostgreSQL setup completed. Database: $DB_NAME, User: $DB_USER"