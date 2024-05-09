from sqlalchemy import TextClause, text


def create_on_update_trigger_func(table_name: str) -> tuple[str, TextClause]:
    """
    PostgreSQL on update trigger function
    :return: TextClause
    """
    func_name = f"{table_name}__{create_on_update_trigger_func.__name__}"

    return func_name, text(
        f"""
        CREATE OR REPLACE FUNCTION {func_name}()
        RETURNS trigger AS ${func_name}$
            BEGIN
                NEW.status_updated_at = TIMEZONE('utc', now());
                RETURN NEW;
            END;
        ${func_name}$ LANGUAGE plpgsql;
        """,
    )


def create_on_update_trigger(
    table_name: str,
    schema: str = "public",
    *,
    func_name: str,
) -> TextClause:
    """
    PostgreSQL trigger on update
    :return: TextClause
    """
    return text(
        f""" 
        CREATE OR REPLACE TRIGGER {table_name}_on_update
        BEFORE UPDATE OF status ON {schema}.{table_name}
        FOR EACH ROW
        EXECUTE FUNCTION {func_name}();
        """,
    )
