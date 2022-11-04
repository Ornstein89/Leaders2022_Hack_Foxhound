from typing import Any, Dict, Optional

from pydantic import AmqpDsn, BaseSettings, MongoDsn, validator


class Settings(BaseSettings):
    project_name: str = "Foxhound"

    mongodb_server: str
    mongodb_db: str = "db"
    broker_server: str = "localhost"
    broker_port: str = "5672"
    broker_user: str = "guest"
    broker_pass: str = "guest"
    database_uri: Optional[MongoDsn] = None
    broker_uri: Optional[AmqpDsn] = None

    @validator("database_uri", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return MongoDsn.build(
            scheme="mongodb",
            host=values.get("mongodb_server"),
            path=f"/{values.get('mongodb_db') or ''}",
        )

    @validator("broker_uri", pre=True)
    def assemble_broker_connection(
        cls, v: Optional[str], values: Dict[str, Any]
    ) -> Any:
        if isinstance(v, str):
            return v
        return AmqpDsn.build(
            scheme="amqp",
            host=values.get("broker_server"),
            user=values.get("broker_user"),
            password=values.get("broker_pass"),
            port=values.get("broker_port"),
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
