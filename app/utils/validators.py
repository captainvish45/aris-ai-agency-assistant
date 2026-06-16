import re

EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
PHONE_PATTERN = re.compile(r"^[\d\s\-\+\(\)]{7,20}$")


def validate_email(email: str) -> tuple[bool, str]:
    email = email.strip()
    if not email:
        return False, "Email address is required."
    if not EMAIL_PATTERN.match(email):
        return False, "Please enter a valid email address."
    return True, ""


def validate_phone(phone: str) -> tuple[bool, str]:
    phone = phone.strip()
    if not phone:
        return False, "Phone number is required."
    digits = re.sub(r"\D", "", phone)
    if len(digits) < 7:
        return False, "Please enter a valid phone number (at least 7 digits)."
    if not PHONE_PATTERN.match(phone):
        return False, "Phone number contains invalid characters."
    return True, ""


def validate_required(value: str, field_name: str, min_length: int = 2) -> tuple[bool, str]:
    value = value.strip()
    if not value:
        return False, f"{field_name} is required."
    if len(value) < min_length:
        return False, f"{field_name} must be at least {min_length} characters."
    return True, ""


def validate_service(service: str, valid_options: list[str]) -> tuple[bool, str]:
    service = service.strip()
    if not service:
        return False, "Please select a service."
    if service not in valid_options:
        return False, "Please select a valid service from the list."
    return True, ""
