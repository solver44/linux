#!/bin/bash

MASTER_IP=192.168.0.117
REPLICATOR_PASSWORD=replicator@123

# Install PostgreSQL
apt update
apt install -y postgresql postgresql-contrib

# Stop PostgreSQL service
systemctl stop postgresql

# Clear the data directory
postgres rm -rf /var/lib/postgresql/15/main/*

# Create a base backup from the master server
postgres pg_basebackup -h $MASTER_IP -D /var/lib/postgresql/15/main -U replicator -P -R

# Create recovery.conf file
echo "standby_mode = 'on'" | tee -a /var/lib/postgresql/15/main/recovery.conf
echo "primary_conninfo = 'host=$MASTER_IP port=5432 user=replicator password=$REPLICATOR_PASSWORD'" | tee -a /var/lib/postgresql/15/main/recovery.conf
echo "trigger_file = '/tmp/postgresql.trigger.5432'" | tee -a /var/lib/postgresql/15/main/recovery.conf

# Set permissions for the recovery.conf file
chown postgres:postgres /var/lib/postgresql/15/main/recovery.conf
chmod 600 /var/lib/postgresql/15/main/recovery.conf

# Start PostgreSQL service
systemctl start postgresql