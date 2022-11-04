
set -e
set -u

function create_schema(){
    psql -v ON_ERROR_STOP=1 -d $POSTGRES_DB --username "$POSTGRES_USER" <<-EOSQL
        CREATE SCHEMA IF NOT EXISTS $POSTGRES_SCHEMA;
EOSQL
}

if [ -n "$POSTGRES_SCHEMA" ]; then
    echo "creating schema $POSTGRES_SCHEMA."
    create_schema
fi

echo "initdb script completed."
