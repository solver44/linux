#!/bin/bash

REPLICATOR_PASSWORD=replicator@123

# Update and install PostgreSQL
apt update
apt install -y postgresql postgresql-contrib

systemctl enable postgresql

# Configure PostgreSQL for replication
sudo -u postgres psql -c "ALTER SYSTEM SET listen_addresses TO '*';"
sudo -u postgres psql -c "ALTER SYSTEM SET wal_level TO replica;"
sudo -u postgres psql -c "ALTER SYSTEM SET max_wal_senders TO 3;"
sudo -u postgres psql -c "ALTER SYSTEM SET wal_keep_size TO 64;"

# Allow replication connections
echo "host    replication     all             0.0.0.0/0               md5" | tee -a /etc/postgresql/15/main/pg_hba.conf

# Restart PostgreSQL service
systemctl restart postgresql

# Create a replication user
postgres psql -c "CREATE USER replicator REPLICATION LOGIN ENCRYPTED PASSWORD '$REPLICATOR_PASSWORD';"
