from typing import List, Optional, Literal
from datetime import datetime
from pydantic import BaseModel, EmailStr
from uuid import UUID


# ------------------------
# CLIENTE
# ------------------------
class ClientBase(BaseModel):
    name: str
    email: EmailStr


class ClientCreate(ClientBase):
    pass


class ClientResponse(ClientBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True


# ------------------------
# EMAIL
# ------------------------
class EmailBase(BaseModel):
    subject: Optional[str] = None
    body: str


class EmailCreate(EmailBase):
    sender_id: UUID
    recipients: List[UUID]
    cc: Optional[List[UUID]] = []
    bcc: Optional[List[UUID]] = []


class EmailResponse(EmailBase):
    id: UUID
    sender_id: UUID
    created_at: datetime
    updated_at: datetime
    category: Optional[str] = None
    suggested_response: Optional[str] = None

    class Config:
        orm_mode = True



# ------------------------
# EMAIL RECIPIENT
# ------------------------
class EmailRecipientResponse(BaseModel):
    id: UUID
    email_id: UUID
    recipient_id: UUID
    type: Literal["TO", "CC", "BCC"]
    status: Literal["SENT", "DELIVERED", "READ"]
    read_at: Optional[datetime] = None

    class Config:
        orm_mode = True
