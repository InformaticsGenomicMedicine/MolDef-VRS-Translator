# Allele Utils

class InvalidVRSAlleleError(Exception):
    """Raised when the expression is not a valid VRS Allele."""
    pass

class InvalidAlleleProfileError(Exception):
    """Raised when the expression is not a valid FHIR Allele."""
    pass

class InvalidSequenceTypeError(Exception):
    """Raised when the RefSeq identifier has an unrecognized prefix."""
    pass

class InvalidAccessionError(Exception):
    """Raised when the provided RefSeq ID does not match the expected format."""
    pass

class InvalidCoordinateSystemError(Exception):
    """Raised when an invalid coordinate system is specified."""
    pass
