#!/bin/bash

echo "Starting Library Management System..."

if [ ! -d "/home/runner/.postgresql/data" ]; then
    echo "Initializing PostgreSQL database..."
    mkdir -p /home/runner/.postgresql/data
    initdb -D /home/runner/.postgresql/data
    mkdir -p /tmp/postgresql
    echo "unix_socket_directories = '/tmp/postgresql'" >> /home/runner/.postgresql/data/postgresql.conf
fi

mkdir -p /tmp/postgresql

if ! pg_ctl -D /home/runner/.postgresql/data status > /dev/null 2>&1; then
    echo "Starting PostgreSQL server..."
    pg_ctl -D /home/runner/.postgresql/data -l /home/runner/.postgresql/logfile start
    sleep 3
fi

if ! psql -h /tmp/postgresql -U runner -d postgres -lqt | cut -d \| -f 1 | grep -qw library_db; then
    echo "Initializing library database..."
    python setup_database.py
fi

echo ""
echo "Database ready! Starting Library Management System..."
echo ""

python main.py
