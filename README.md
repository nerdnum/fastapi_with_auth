# Fastapi with authentication

This project implements Fastapi with SqlAlchemy and postgresql. It provdes a user model, role model and allows for mapping between users and roles. It also provides simple OAuth authentication, as shown in the FastAPI documentation. It also provides extensive pytest tests for the implementation  

## Simple usage

Run the API with ```uvicorn run:server --reload```. Use the ```--reload``` only for development. 

You can provide your own config.json file in the root directory. The format is below.

```
#config.json
{
  "config_name": "development",
  "db_url": "postgresql+asyncpg://username:password@localhost/fastapi_db",
  "secret_key": "your_sercret_key",
  "algorithm": "HS256",
  "access_token_expire_minutes": 30
}
```
