from fastapi import FastAPI
from app.routers import clients, emails
from app import models, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Email API")

app.include_router(clients.router)
app.include_router(emails.router)


# Criar clientes (POST /clients/)

# Enviar emails (POST /emails/)

# Listar enviados (GET /emails/sent/{client_id})

# Listar recebidos (GET /emails/received/{client_id})

# Marcar como lido (PATCH /emails/{email_id}/read/{recipient_id})