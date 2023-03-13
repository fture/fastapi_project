import re
from uuid import UUID
from fastapi import HTTPException
from validate_email import validate_email as valid_email


def validate_uuid(value):
    try:
        return UUID(value)
    except ValueError:
        raise HTTPException(status_code=400, detail="Not a valid UUID")


def validate_email(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise HTTPException(status_code=400, detail="Not a valid email")
    else:
        return email
