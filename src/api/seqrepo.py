from ga4gh.vrs.dataproxy import create_dataproxy

class SeqRepoClient:
    """Simple interface for creating and managing a SeqRepo data proxy."""

    DEFAULT_LOCAL_URL = "seqrepo+file:///usr/local/share/seqrepo/2024-12-20/"
    # HOST_URL = "seqrepo+https://services.genomicmedlab.org/seqrepo"

    def __init__(self, uri: str | None = None):
        """Initialize a SeqRepo data proxy from local or remote source."""
        self.dataproxy = self._create_proxy_with_fallback(uri or self.DEFAULT_LOCAL_URL)

    def _create_proxy_with_fallback(self, uri: str):
        try:
            return create_dataproxy(uri=uri)
        except Exception:
            try:
                return create_dataproxy(uri=self.DEFAULT_LOCAL_URL)
            except Exception as e:
                raise RuntimeError(f"Failed to create SeqRepo data proxy: {e}") from e
