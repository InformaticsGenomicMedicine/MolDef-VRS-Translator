from ga4gh.vrs.models import LiteralSequenceExpression
from ga4gh.vrs.normalize import denormalize_reference_length_expression

from api.seqrepo import SeqRepoAPI


class SequenceExpressionTranslator:
    def __init__(self):
        seqrepo_api = SeqRepoAPI()
        self.dp = seqrepo_api.seqrepo_dataproxy

    def translate_rle_to_lse(self, ao):

        sequence = f"ga4gh:{ao.location.get_refget_accession()}"

        aliases = self.dp.translate_sequence_identifier(sequence, 'refseq')
        refseq_id = aliases[0].split(':')[1]

        ref_seq = self.dp.get_sequence(identifier=refseq_id,
                                start=ao.location.start,
                                end=ao.location.end)

        if ao.state.type == "ReferenceLengthExpression":
            alt_seq = denormalize_reference_length_expression(
                ref_seq=ref_seq,
                repeat_subunit_length=ao.state.repeatSubunitLength,
                alt_length=ao.state.length
            )
            ao.state = LiteralSequenceExpression(sequence=alt_seq)

        return ao
