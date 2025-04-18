import re
from decimal import Decimal

from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.quantity import Quantity
from fhir.resources.reference import Reference
from ga4gh.vrs import models

from api.seqrepo import SeqRepoAPI
from resources.moleculardefinition import (
    MolecularDefinitionLocation,
    MolecularDefinitionLocationSequenceLocation,
    MolecularDefinitionLocationSequenceLocationCoordinateInterval,
    MolecularDefinitionLocationSequenceLocationCoordinateIntervalCoordinateSystem,
    MolecularDefinitionRepresentation,
    MolecularDefinitionRepresentationLiteral,
)
from translators.allele_utils import (
    detect_sequence_type,
    is_valid_allele_profile,
    is_valid_vrs_allele,
    validate_accession,
    validate_indexing,
)
from normalize.allele_normalizer import AlleleNormalizer
from profiles.allele import Allele as FhirAllele
from profiles.sequence import Sequence as FhirSequence


class VrsFhirAlleleTranslation:
    """Handles VRS <-> FHIR Allele conversion for 'contained' format."""

    def __init__(self):
        self.seqrepo_api = SeqRepoAPI()
        self.dp = self.seqrepo_api.seqrepo_dataproxy
        self.norm = AlleleNormalizer()

    ##############################################################

    def _is_valid_sequence_location(self, locations):
        """Validates the `sequenceLocation` structure within the provided locations to ensure all necessary attributes are present for accurate translations.

        Args:
            locations (list): A list of location objects containing `sequenceLocation` attributes.

        Raises:
            ValueError: If 'sequenceLocation' is missing in any location.
            ValueError: If 'coordinateInterval' is missing in any sequence location.
            ValueError: If 'coordinateSystem.system.coding' is missing in any coordinate interval.
            ValueError: If 'coding.display' is missing in 'coordinateSystem.system.coding'.
            ValueError: If 'startQuantity.value' is missing in any coordinate interval.
            ValueError: If 'endQuantity.value' is missing in any coordinate interval.

        Returns:
            sequence_location: The validated sequence location object.

        """
        for loc in locations:
            # Access sequenceLocation first
            sequence_location = loc.sequenceLocation
            if not sequence_location:
                raise ValueError("Missing 'sequenceLocation' in location.")
            # Check coordinateInterval existence
            if not sequence_location.coordinateInterval:
                raise ValueError("Missing 'coordinateInterval' in sequence location.")

            coordinate_interval = sequence_location.coordinateInterval

            # Check coordinateSystem.system.coding
            if not coordinate_interval.coordinateSystem.system.coding:
                raise ValueError(
                    "Missing 'coordinateSystem.system.coding' in coordinate interval."
                )

            if not any(
                coding.display
                for coding in coordinate_interval.coordinateSystem.system.coding
            ):
                raise ValueError(
                    "Missing 'coding.display' in 'coordinateSystem.system.coding'."
                )

            # Check startQuantity and endQuantity
            if not getattr(coordinate_interval.startQuantity, "value", None):
                raise ValueError(
                    "Missing 'startQuantity.value' in coordinate interval."
                )
            if not getattr(coordinate_interval.endQuantity, "value", None):
                raise ValueError("Missing 'endQuantity.value' in coordinate interval.")

        return sequence_location

    def _convert_decimal_to_int(self, value):
        """Validate and convert a Decimal value to an integer if possible.

        Args:
            value (Decimal): The value to be validated and converted.

        Raises:
            TypeError: If the value is not a Decimal.
            ValueError: If the Decimal value cannot be converted to an integer.

        Returns:
            int: The validated and converted integer value.

        """
        # check if the value is a decimal
        if not isinstance(value, Decimal):
            raise TypeError("Value is not a valid Decimal value.")

        if value == value.to_integral_value():
            value = int(value)
        else:
            raise TypeError(
                "Decimal Value must be able to be converted into an Integer"
            )
        return value

    def _validate_sequence(self, sequence):
        """Validate the sequence to ensure it contains valid characters as per VRS rules.

        Args:
            sequence (str): The sequence to be validated.

        Raises:
            ValueError: If the sequence contains invalid characters.

        Returns:
            str: The validated sequence.

        """
        pattern = r"^[A-Z*\-]*$"
        if not re.match(pattern, sequence):
            raise ValueError("Invalid sequence value")
        return sequence

    def _get_literal_value_for_allele_state(self, representations):
        """Retrieves the literal value associated with an `allele-state` representation, if present, from the provided list of representations.

        Args:
            representations (list): A list of representation objects that may include `allele-state` details.

        Raises:
                ValueError: If the `allele-state` representation is present but lacks a `literal.value`.

        Returns:
            str: The value of the `literal` attribute for the `allele-state` representation.

        """
        for rep in representations:
            focus = getattr(rep, "focus", None)
            if focus and any(
                coding.code == "allele-state" for coding in getattr(focus, "coding", [])
            ):
                literal = getattr(rep, "literal", None)
                if literal:
                    return literal.value
                else:
                    raise ValueError(
                        "Missing `literal.value` for the `allele-state` representation."
                    )

    def _translate_sequence_id(self, dp, sequence_id):
        """Translate a sequence ID using SeqRepo and return the RefSeq ID.

        Args:
            dp (SeqRepo DataProxy): The data proxy used to translate the sequence.
            sequence_id (str): The sequence ID to be translated.

        Raises:
            ValueError: If translation fails or if format is unexpected.

        Returns:
            str: A valid RefSeq identifier (e.g., NM_000123.3).
        """
        translated_ids = dp.translate_sequence_identifier(
            sequence_id, namespace="refseq"
        )
        if not translated_ids:
            raise ValueError(f"No RefSeq ID found for sequence ID '{sequence_id}'.")

        translated_id = translated_ids[0]
        if not translated_id.startswith("refseq:"):
            raise ValueError(f"Unexpected ID format in '{translated_id}'")

        _, refseq_id = translated_id.split(":")
        return refseq_id

    def _extract_vrs_values(self, expression, dp):
        """Extract GA4GH ID, RefSeq ID, start, end, and sequence from a VRS Allele.

        Args:
            expression: A VRS Allele object.
            dp: SeqRepo data proxy for ID translation.

        Returns:
            tuple: (refseq_id, start_pos, end_pos, alt_allele)
        """
        is_valid_vrs_allele(expression)

        refseq_id = self._translate_sequence_id(
            dp, str(expression.location.sequence_id)
        )
        start_pos = expression.location.interval.start.value
        end_pos = expression.location.interval.end.value
        alt_allele = expression.state.sequence

        return refseq_id, start_pos, end_pos, alt_allele

    def _validate_and_extract_code(self, expression):
        if not expression.contained:
            raise ValueError("Missing 'contained' field.")

        contained_item = expression.contained[0]
        if not contained_item.representation or len(contained_item.representation) != 1:
            raise ValueError(
                "Contained 'representation' must contain exactly one item."
            )

        representation_item = contained_item.representation[0]
        if not representation_item.code:
            raise ValueError("Missing 'code' field in representation.")

        code_item = representation_item.code[0]
        if not code_item.coding or not code_item.coding[0].code:
            raise ValueError("Missing 'coding.code' value.")

        return validate_accession(code_item.coding[0].code)

    def _refseq_to_fhir_id(self, refseq_accession):
        """Converts a RefSeq accession string to a standardized FHIR ID format.
        This method removes the version suffix (after the dot), strips out underscores,
        and converts the string to lowercase to ensure compatibility with FHIR resource IDs.

        Args:
            refseq_accession (str): A RefSeq accession string (e.g., 'NM_001256789.1').

        Returns:
            str: A formatted FHIR-compatible ID (e.g., 'nm001256789').
        """
        return refseq_accession.split(".", 1)[0].replace("_", "").lower()

    #############################################################

    def allele_profile_to_vrs_allele(self, expression, normalize=True):
        """Converts an FHIR Allele object into a GA4GH VRS Allele object.

        Args:
            expression (Allele): A FHIR-compliant Allele containing sequence location,
                representation, and other metadata required for conversion.
            normalize (bool, optional): If True, returns a normalized VRS Allele using the VRS normalizer.
                Defaults to True.

        Raises:
            ValueError: Raised if multiple codings are found in the coordinate system or if the
                coordinate system is unsupported.

        Returns:
            models.Allele: A GA4GH VRS Allele object.
        """
        # Validate that the input is an Allele
        is_valid_allele_profile(expression)

        # validating the locaiton
        location_data = self._is_valid_sequence_location(expression.location)

        values_needed = {
            "refseq": self._validate_and_extract_code(expression),
            "start": location_data.coordinateInterval.startQuantity.value,
            "end": location_data.coordinateInterval.endQuantity.value,
        }

        coding_list = location_data.coordinateInterval.coordinateSystem.system.coding
        if len(coding_list) != 1:
            raise ValueError("Only one coding supported in coordinateSystem.")

        values_needed["coordinate_system_display"] = coding_list[0].display

        seq = self._get_literal_value_for_allele_state(expression.representation)
        start = validate_indexing(
            values_needed["coordinate_system_display"], values_needed["start"]
        )
        start_pos = self._convert_decimal_to_int(start)
        end_pos = self._convert_decimal_to_int(values_needed["end"])
        alt_seq = self._validate_sequence(seq)

        interval = models.SequenceInterval(
            start=models.Number(value=start_pos),
            end=models.Number(value=end_pos),
        )
        location = models.SequenceLocation(
            sequence_id=f"refseq:{values_needed['refseq']}", interval=interval
        )
        state = models.LiteralSequenceExpression(sequence=alt_seq)

        allele = models.Allele(location=location, state=state)
        return self.norm.post_normalize_allele(allele) if normalize else allele

    def vrs_allele_to_allele_profile(self, expression):
        """Converts a GA4GH VRS Allele object into a FHIR Allele.

        Args:
            expression (models.Allele): A GA4GH VRS Allele containing location and state information
                used to reconstruct a FHIR Allele.

        Returns:
            Allele: A FHIR Allele object.
        """
        refseq_id, start_pos, end_pos, alt_allele = self._extract_vrs_values(
            expression, self.dp
        )

        sequence_type = detect_sequence_type(refseq_id)

        mol_type = CodeableConcept(
            coding=[
                {
                    "system": "http://hl7.org/fhir/sequence-type",
                    "code": sequence_type.lower(),
                    "display": f"{sequence_type} Sequence",
                }
            ]
        )

        coding_ref = Coding(
            system="http://www.ncbi.nlm.nih.gov/refseq",
            code=refseq_id,
        )

        code_value = CodeableConcept(coding=[coding_ref])
        representation_sequence = MolecularDefinitionRepresentation(code=[code_value])

        fhir_id = self._refseq_to_fhir_id(refseq_accession=refseq_id)

        sequence_profile = FhirSequence(
            id=f"ref-to-{fhir_id}",
            moleculeType=mol_type,
            representation=[representation_sequence],
        )

        if alt_allele == "":
            alt_allele = " "

        start_quant = Quantity(value=int(start_pos))
        end_quant = Quantity(value=int(end_pos))

        coord_system = CodeableConcept(
            coding=[
                {
                    "system": "http://loinc.org",
                    "code": "LA30100-4",
                    "display": "0-based interval counting",
                }
            ]
        )
        seq_context = Reference(
            reference=f"#{sequence_profile.id}", type="MolecularDefinition"
        )
        focus_value = CodeableConcept(
            coding=[
                Coding(
                    system="http://hl7.org/fhir/moleculardefinition-focus",
                    code="allele-state",
                )
            ]
        )

        moldef_literal = MolecularDefinitionRepresentationLiteral(value=str(alt_allele))
        moldef_repr = MolecularDefinitionRepresentation(
            focus=focus_value, literal=moldef_literal
        )

        coord_system_fhir = MolecularDefinitionLocationSequenceLocationCoordinateIntervalCoordinateSystem(
            system=coord_system
        )
        coord_interval = MolecularDefinitionLocationSequenceLocationCoordinateInterval(
            coordinateSystem=coord_system_fhir,
            startQuantity=start_quant,
            endQuantity=end_quant,
        )

        seq_location = MolecularDefinitionLocationSequenceLocation(
            sequenceContext=seq_context, coordinateInterval=coord_interval
        )

        location = MolecularDefinitionLocation(sequenceLocation=seq_location)

        return FhirAllele(
            contained=[sequence_profile],
            moleculeType=mol_type,
            location=[location],
            representation=[moldef_repr],
        )
