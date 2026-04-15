import os
import boto3
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base


# Aurora RDS config
RDS_HOST = os.getenv("RDS_HOST", "database-1.cluster-c3omqe20so68.us-east-2.rds.amazonaws.com")
RDS_PORT = int(os.getenv("RDS_PORT", "5432"))
RDS_USER = os.getenv("RDS_USER", "postgres")
RDS_DB = os.getenv("RDS_DB", "postgres")
RDS_REGION = os.getenv("RDS_REGION", "us-east-2")
USE_IAM_AUTH = os.getenv("USE_IAM_AUTH", "false").lower() == "true"
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")


def get_iam_token():
    client = boto3.client("rds", region_name=RDS_REGION)
    token = client.generate_db_auth_token(
        DBHostname=RDS_HOST,
        Port=RDS_PORT,
        DBUsername=RDS_USER,
    )
    return token


if "sqlite" in DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
elif USE_IAM_AUTH:
    # IAM auth: do NOT embed token in URL (tokens contain @ which breaks URL parsing)
    # Instead, inject token via event listener on every new connection
    iam_url = f"postgresql://{RDS_USER}@{RDS_HOST}:{RDS_PORT}/{RDS_DB}"
    engine = create_engine(
        iam_url,
        connect_args={"sslmode": "require"}
    )

    @event.listens_for(engine, "do_connect")
    def provide_token(dialect, conn_rec, cargs, cparams):
        cparams["password"] = get_iam_token()
else:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"sslmode": "require"}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()