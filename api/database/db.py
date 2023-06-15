from sqlalchemy import create_engine
import settings


# Create engine
if settings.DATABASE_URL is not None:
    engine = create_engine(settings.DATABASE_URL, echo=True)

else:
    db_url = f"postgres://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}" + \
                       f"@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"

    engine = create_engine(db_url, echo=True)
