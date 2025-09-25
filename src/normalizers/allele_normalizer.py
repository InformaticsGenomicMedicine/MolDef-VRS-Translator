from ga4gh.core import ga4gh_identify
from ga4gh.vrs import normalize as vrs_normalize

from api.seqrepo import SeqRepoAPI


class AlleleNormalizer:
    """Initialize the AlleleNormalizer with a SeqRepo-backed data proxy.
    """
    def __init__(self):
        self.seqrepo_api = SeqRepoAPI()
        self.dp = self.seqrepo_api.seqrepo_dataproxy

    def post_normalize_allele(self, allele):
        """Normalize the VRS allele and assign GA4GH identifiers.

        Args:
            allele (models.Allele): The VRS allele to be normalized.

        Returns:
            models.Allele: The normalized VRS allele with GA4GH identifiers.

        """

        # Using the ga4gh normalize function to normalize the allele. (Coming form biocommons.normalize())
        allele = vrs_normalize(allele, self.dp)
        # Setting the allele id to a  GA4GH digest-based id for the object, as a CURIE
        allele.id = ga4gh_identify(allele)
        # Setting the location id to a GA4GH digest-based id for the object, as a CURIE
        allele.location.id = ga4gh_identify(allele.location)
        return allele
