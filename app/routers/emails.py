from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from datetime import datetime

router = APIRouter(prefix="/emails", tags=["Emails"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.EmailResponse)
def send_email(email_data: schemas.EmailCreate, db: Session = Depends(get_db)):
    db_email = models.Email(
        subject=email_data.subject,
        body=email_data.body,
        sender_id=email_data.sender_id,
    )
    db.add(db_email)
    db.commit()
    db.refresh(db_email)

    # salvar destinatários
    for r in email_data.recipients:
        db_recipient = models.EmailRecipient(
            email_id=db_email.id, recipient_id=r, type=models.RecipientType.TO
        )
        db.add(db_recipient)

    for r in email_data.cc:
        db_recipient = models.EmailRecipient(
            email_id=db_email.id, recipient_id=r, type=models.RecipientType.CC
        )
        db.add(db_recipient)

    for r in email_data.bcc:
        db_recipient = models.EmailRecipient(
            email_id=db_email.id, recipient_id=r, type=models.RecipientType.BCC
        )
        db.add(db_recipient)

    db.commit()
    return db_email


@router.get("/sent/{client_id}", response_model=list[schemas.EmailResponse])
def list_sent_emails(client_id: str, db: Session = Depends(get_db)):
    return db.query(models.Email).filter(models.Email.sender_id == client_id).all()


@router.get("/received/{client_id}", response_model=list[schemas.EmailRecipientResponse])
def list_received_emails(client_id: str, db: Session = Depends(get_db)):
    return db.query(models.EmailRecipient).filter(models.EmailRecipient.recipient_id == client_id).all()


@router.patch("/{email_id}/read/{recipient_id}", response_model=schemas.EmailRecipientResponse)
def mark_as_read(email_id: str, recipient_id: str, db: Session = Depends(get_db)):
    recipient = (
        db.query(models.EmailRecipient)
        .filter(models.EmailRecipient.email_id == email_id, models.EmailRecipient.recipient_id == recipient_id)
        .first()
    )
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")

    recipient.status = models.EmailStatus.READ
    recipient.read_at = datetime.utcnow()
    db.commit()
    db.refresh(recipient)
    return recipient
