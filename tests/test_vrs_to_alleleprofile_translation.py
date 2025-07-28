from decimal import Decimal

import pytest
from ga4gh.vrs.models import Allele

from translators.vrs_fhir_translator import VrsFhirAlleleTranslation


@pytest.fixture
def example():
    return {
        "id": "ga4gh:VA.3edM6TTGAmx8DnPV-uzA6IYlAfatAP2s",
        "type": "Allele",
        "digest": "3edM6TTGAmx8DnPV-uzA6IYlAfatAP2s",
        "location": {
            "id": "ga4gh:SL.OUMCiUkn_AGlFuFCFTdfppig932_HV2k",
            "type": "SequenceLocation",
            "digest": "OUMCiUkn_AGlFuFCFTdfppig932_HV2k",
            "sequenceReference": {
                "type": "SequenceReference",
                "refgetAccession": "SQ.Ya6Rs7DHhDeg7YaOSg1EoNi3U_nQ9SvO",
            },
            "start": 113901365,
            "end": 113901365,
        },
        "state": {"type": "LiteralSequenceExpression", "sequence": "ATA"},
    }


@pytest.fixture
def allele_translator():
    return VrsFhirAlleleTranslation()

@pytest.fixture
def vrs_allele(example):
    return Allele(**example)

@pytest.fixture
def alleleprofile_expected_outputs():
    return {
        "resourceType": "MolecularDefinition",
        "contained": [
            {
                "resourceType": "MolecularDefinition",
                "id": "ref-to-nc000001",
                "moleculeType": {
                    "coding": [
                        {
                            "system": "http://hl7.org/fhir/sequence-type",
                            "code": "dna",
                            "display": "DNA Sequence",
                        }
                    ]
                },
                "representation": [
                    {
                        "code": [
                            {
                                "coding": [
                                    {
                                        "system": "http://www.ncbi.nlm.nih.gov/refseq",
                                        "code": "NC_000001.11",
                                    }
                                ]
                            }
                        ]
                    }
                ],
            }
        ],
        "moleculeType": {
            "coding": [
                {
                    "system": "http://hl7.org/fhir/sequence-type",
                    "code": "dna",
                    "display": "DNA Sequence",
                }
            ]
        },
        "location": [
            {
                "sequenceLocation": {
                    "sequenceContext": {
                        "reference": "#ref-to-nc000001",
                        "type": "MolecularDefinition",
                    },
                    "coordinateInterval": {
                        "coordinateSystem": {
                            "system": {
                                "coding": [
                                    {
                                        "system": "http://loinc.org",
                                        "code": "LA30100-4",
                                        "display": "0-based interval counting",
                                    }
                                ]
                            }
                        },
                        "startQuantity": {"value": Decimal(113901365)},
                        "endQuantity": {"value": Decimal(113901365)},
                    },
                }
            }
        ],
        "representation": [
            {
                "focus": {
                    "coding": [
                        {
                            "system": "http://hl7.org/fhir/moleculardefinition-focus",
                            "code": "allele-state",
                        }
                    ]
                },
                "literal": {"value": "ATA"},
            }
        ],
    }


def test_translate_vrs_to_alleleprofile(
    allele_translator, vrs_allele, alleleprofile_expected_outputs
):
    output_dict = allele_translator.vrs_allele_to_allele_profile(
        vrs_allele
    ).model_dump()
    assert output_dict == alleleprofile_expected_outputs
