import re

from exceptions.utils import (
    InvalidAccessionError,
    InvalidAlleleProfileError,
    InvalidCoordinateSystemError,
    InvalidSequenceTypeError,
    InvalidVRSAlleleError,
)
from profiles.allele import Allele as FhirAllele


def is_valid_vrs_allele(expression):
    """Validation step to ensure that the expression is a valid VRS Allele object.

    Args:
        expression (object): An object representing a VRS Allele.

    Raises:
        InvalidVRSAlleleError: If the expression is not a valid VRS Allele object.

    """
    conditions = [
        (expression.type == "Allele", "The expression type must be 'Allele'."),
        (
            expression.location.type == "SequenceLocation",
            "The location type must be 'SequenceLocation'.",
        ),
        (
            expression.state.type == "LiteralSequenceExpression",
            "The state type must be 'LiteralSequenceExpression'.",
        ),
    ]
    for condition, error_message in conditions:
        if not condition:
            raise InvalidVRSAlleleError(error_message)


def is_valid_allele_profile(expression: object):
    """Validates if the given expression is a valid Allele.

    Args:
        expression (object): The expression to validate.

    Raises:
        TypeError: If the expression is not an instance of Allele.

    """
    if not isinstance(expression, FhirAllele):
        raise InvalidAlleleProfileError(
            "Invalid expression type: expected an instance of Allele."
        )


def detect_sequence_type(sequence_id: str) -> str:
    """Translate the prefix of the RefSeq identifier to the type of sequence.

    Args:
        sequence_id (str): The RefSeq identifier.

    Raises:
        ValueError: If the prefix doesn't match any known sequence type.

    Returns:
        str: The type of sequence

    """
    prefix_to_type = {
        "NC_": "DNA",
        "NG_": "DNA",
        "NM_": "RNA",
        "NR_": "RNA",
        "NP_": "protein",
    }

    for prefix, seq_type in prefix_to_type.items():
        if sequence_id.startswith(prefix):
            return seq_type

    raise InvalidSequenceTypeError(f"Unknown sequence type for input: {sequence_id}")


def validate_accession(refseq_id: str) -> str:
    """Validate the given RefSeq ID to ensure it matches the expected format.

    Args:
        refseq_id (str): The RefSeq ID to be validated.

    Raises:
        ValueError: If the RefSeq ID does not match the expected format.

    Returns:
        str: The validated RefSeq ID.
    """
    refseq_pattern = re.compile(r"^(NC_|NG_|NM_|NP_)\d+\.\d+$")

    if not refseq_pattern.match(refseq_id):
        raise InvalidAccessionError(
            f"Invalid accession number: {refseq_id}. Must be a valid NCBI RefSeq ID (e.g., NM_000769.4)."
        )

    return refseq_id


def validate_indexing(coord_system, start):
    """Adjust the indexing based on the coordinate system.

    Args:
        CoordSystem (str): The coordinate system, which can be one of the following:
                            '0-based interval counting', '0-based character counting', '1-based character counting'.
        start (int): The start position to be adjusted.

    Raises:
        ValueError: If an invalid coordinate system is specified.

    Returns:
        int: The adjusted start position.

    """
    adjustments = {
        "0-based interval counting": 0,
        "0-based character counting": 1,
        "1-based character counting": -1,
    }

    if coord_system not in adjustments:
        raise InvalidCoordinateSystemError(
            "Invalid coordinate system specified. Valid options are: '0-based interval counting', '0-based character counting', '1-based character counting'."
        )

    return start + adjustments[coord_system]
