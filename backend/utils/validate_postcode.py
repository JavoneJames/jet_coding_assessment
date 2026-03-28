from re import match

from fastapi import HTTPException

# check if the postcode is valid based on UK format
def validate_postcode(postcode: str):
    if not postcode or not isinstance(postcode, str):
        raise HTTPException(status_code=400,detail=f"Invalid postcode format: {postcode}")
    pattern = (
            r"^("
            r"GIR 0AA|"  # Special postcode
            r"(?:[A-PR-UWYZ][0-9][0-9A-HJKSTUW]?|"  # A9, A9A
            r"[A-PR-UWYZ][A-HK-Y][0-9][0-9ABEHMNPRV-Y]?))"  # AA9, AA9A
            r"\s?[0-9][ABD-HJLNP-UW-Z]{2}$"  # Inward code
        )
    if not match(pattern=pattern, string=postcode):
            raise HTTPException(status_code=400,detail=f"Invalid postcode format: {postcode}")


