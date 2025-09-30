from sqlalchemy import Column, String, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from .database import Base


class EmailStatus(str, enum.Enum):
    SENT = "SENT"
    DELIVERED = "DELIVERED"
    READ = "READ"

class RecipientType(str, enum.Enum):
    TO = "TO"
    CC = "CC"
    BCC = "BCC"

class Client(Base):
    __tablename__ = "clients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    sent_emails = relationship("Email", back_populates="sender")

class Email(Base):
    __tablename__ = "emails"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subject = Column(String(255))
    body = Column(String, nullable=False)
    sender_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 🔹 novos campos
    category = Column(String(50), nullable=True)  # Produtivo ou Improdutivo
    suggested_response = Column(String, nullable=True)

    sender = relationship("Client", back_populates="sent_emails")
    recipients = relationship("EmailRecipient", back_populates="email")

class EmailRecipient(Base):
    __tablename__ = "email_recipients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email_id = Column(UUID(as_uuid=True), ForeignKey("emails.id"))
    recipient_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"))
    type = Column(Enum(RecipientType), default=RecipientType.TO)
    status = Column(Enum(EmailStatus), default=EmailStatus.SENT)
    read_at = Column(DateTime, nullable=True)

    email = relationship("Email", back_populates="recipients")
    recipient = relationship("Client")
