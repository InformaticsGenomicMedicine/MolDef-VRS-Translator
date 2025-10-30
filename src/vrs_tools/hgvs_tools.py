import hgvs
import hgvs.parser

from ga4gh.vrs.utils.hgvs_tools import HgvsTools as _Base

class HgvsToolsLite(_Base):
    """
    A lightweight subclass of HgvsTools that does not connect to the UTA database.
    Provides parsing and syntax validation only.
    """
    def __init__(self, data_proxy=None):
        self.parser = hgvs.parser.Parser()
        self.data_proxy = data_proxy

        # make UTA-related attrs exist but disabled
        # Need to write a Query to see if i get a connection form UTA
        self.uta_conn = None
        self.normalizer = None
        self.variant_mapper = None

    def normalize(self, hgvs):
        raise NotImplementedError("normalize() requires the UTA database (not available in HgvsToolsLite)")

    def n_to_c(self, hgvs):
        raise NotImplementedError("n_to_c() requires the UTA database (not available in HgvsToolsLite)")

    def c_to_n(self, hgvs):
        raise NotImplementedError("c_to_n() requires the UTA database (not available in HgvsToolsLite)")


