#!/bin/sh

set -e

host_port="$1"
shift

# Разделяем host:port на отдельные переменные
host=$(echo $host_port | cut -d: -f1)
port=$(echo $host_port | cut -d: -f2)

echo "Waiting for PostgreSQL at $host:$port..."

# Используем переменные из окружения
until PGPASSWORD=$DB_PASSWORD psql -h "$host" -p "$port" -U "$DB_USER" -d "$DB_NAME" -c '\q' > /dev/null 2>&1; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec "$@"