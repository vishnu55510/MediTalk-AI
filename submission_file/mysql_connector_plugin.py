import aiomysql
from typing import Annotated, Optional
from semantic_kernel.functions.kernel_function_decorator import kernel_function


class MySQLConnectorPlugin:
    """Semantic Kernel Plugin for interacting with a MySQL database."""

    def __init__(self, host: str, user: str, password: str, database: str, port: int = 3306):
        self.db_config = {
            "host": host,
            "user": user,
            "password": password,
            "db": database,
            "port": port,
        }

    async def _execute_query(self, query: str, params: Optional[list] = None) -> list[dict]:
        try:
            conn = await aiomysql.connect(**self.db_config)
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, params or ())
                if query.strip().lower().startswith("select"):
                    result = await cursor.fetchall()
                else:
                    await conn.commit()
                    result = [{"message": f"Query executed successfully: {cursor.rowcount} rows affected"}]
            conn.close()
            return result
        except Exception as e:
            return [{"error": str(e)}]

    @kernel_function(
        name="query_database",
        description="Run a SQL SELECT query on the MySQL database."
    )
    async def query_database(
        self,
        query: Annotated[str, "The SELECT SQL query to execute"],
        params: Annotated[str, "Comma-separated parameters for the query"] = ""
    ) -> list[dict]:
        if not query.strip().lower().startswith("select"):
            return [{"error": "Only SELECT queries are allowed in this function."}]
        param_list = [p.strip() for p in params.split(",")] if params else []
        return await self._execute_query(query, param_list)

    @kernel_function(
        name="update_database",
        description="Run an INSERT, UPDATE, or DELETE SQL query on the MySQL database."
    )
    @kernel_function(
    name="update_database",
    description="Run an INSERT, UPDATE, or DELETE SQL query on the MySQL database."
)
    async def update_database(
        self,
        query: Annotated[str, "The SQL query to execute (INSERT/UPDATE/DELETE)"],
        params: Annotated[str, "Comma-separated parameters for the query"] = ""
    ) -> list[dict]:
        if query.strip().lower().startswith("select"):
            return [{"error": "Use query_database for SELECT operations."}]
        param_list = [p.strip() for p in params.split(",")] if params else []
        return await self._execute_query(query, param_list)
    @kernel_function(
        name="list_tables",
        description="List all tables in the connected MySQL database."
    )
    async def list_tables(self) -> list[dict]:
        return await self._execute_query("SHOW TABLES")

    @kernel_function(
        name="describe_table",
        description="Describe the columns of a specific table."
    )
    async def describe_table(
        self,
        table_name: Annotated[str, "The name of the table to describe"]
    ) -> list[dict]:
        return await self._execute_query(f"DESCRIBE `{table_name}`")

    