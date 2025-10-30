from ga4gh.core import ga4gh_identify
from ga4gh.vrs import normalize as vrs_normalize


class VariantNormalizer:
    """Handles variant normalization using GA4GH VRS."""

    def __init__(self, dataproxy):
        self.dataproxy = dataproxy

    def normalize(self, allele):
        # Using the ga4gh normalize function to normalize the allele. (Coming form biocommons.normalize())
        allele = vrs_normalize(allele, self.dataproxy)
        # Setting the allele id to a GA4GH digest-based id for the object, as a CURIE
        allele.id = ga4gh_identify(allele)
        # Setting the location id to a GA4GH digest-based id for the object, as a CURIE
        allele.location.id = ga4gh_identify(allele.location)

        return allele
