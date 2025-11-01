#!/bin/bash

if [ ! -d "/home/runner/.postgresql/data" ]; then
    echo "Initializing PostgreSQL database..."
    mkdir -p /home/runner/.postgresql/data
    initdb -D /home/runner/.postgresql/data
    mkdir -p /tmp/postgresql
    echo "unix_socket_directories = '/tmp/postgresql'" >> /home/runner/.postgresql/data/postgresql.conf
fi

if ! pg_ctl -D /home/runner/.postgresql/data status > /dev/null 2>&1; then
    echo "Starting PostgreSQL server..."
    mkdir -p /tmp/postgresql
    pg_ctl -D /home/runner/.postgresql/data -l /home/runner/.postgresql/logfile start
    sleep 2
else
    echo "PostgreSQL is already running"
fi

if [ "$1" = "setup" ]; then
    echo "Setting up library database..."
    python setup_database.py
fi
