import re


def validate_email(address):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", address):
        raise ValueError("Adresse email invalide")
    if len(address) > 120:
        raise ValueError("L'adresse email est trop longue")
    return address


def validate_string_length(value, field_name, max_length):
    if len(value) > max_length:
        raise ValueError(
            f"Le champ {field_name} est trop long (maximum {max_length} caractères)"
        )
    return value


def validate_phone_number(number):
    if len(number) > 20:
        raise ValueError("Le numéro de téléphone est trop long")
    # Ajoutez une validation du format si nécessaire
    return number


def validate_positive_amount(value, field_name):
    if value < 0:
        raise ValueError(f"Le montant {field_name} ne peut pas être négatif")
    return value


def validate_positive_integer(value, field_name):
    if value < 0:
        raise ValueError(f"La valeur de {field_name} ne peut pas être négative")
    return value
