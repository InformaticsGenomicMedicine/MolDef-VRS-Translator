
import gzip
import time
import argparse 
import orjson
import logging
from ga4gh.vrs.models import Allele
from translators.vrs_to_fhir import VrsToFhirAlleleTranslator 


class FastTranslation():

    def __init__(self):
        self.vrs_translator = VrsToFhirAlleleTranslator()

    def clinvartranslation(self,inputfile, outputfile, invalid_allele_path, invalid_fhir_path, limit = None):
        
        invalid_allele_log = open(invalid_allele_path, "ab")
        invalid_fhir_trans_log = open(invalid_fhir_path, "ab")

        try:
            with open(outputfile, "ab") as out_f:
                with gzip.open(inputfile, "rt", encoding="utf-8") as f:
                    for line_num, line in enumerate(f, 1):
                        if limit is not None and line_num > limit:
                            break
                        try:
                            obj = orjson.loads(line)
                            members = obj.get("members", [])
                        except orjson.JSONDecodeError:
                            logging.warning("[Line %d] Skipping: JSON decode error", line_num)
                            continue

                        for member in members:
                            if not (isinstance(member, dict) and member.get("type") == "Allele"):
                                continue

                            try:
                                vo = Allele(**member)
                            except Exception as e:
                                invalid_allele = {"line": line_num, "error": str(e), "member": member}
                                invalid_allele_log.write(orjson.dumps(invalid_allele) + b"\n")
                                continue

                            try:
                                fhir_obj = self.vrs_translator.translate_allele_to_fhir(vo)

                                valid_translation = {
                                    "line": line_num,
                                    "vrs_allele": vo.model_dump(exclude_none=True), 
                                    "fhir_allele": fhir_obj.model_dump(exclude_none=True),
                                }

                                out_f.write(orjson.dumps(valid_translation) + b"\n")

                            except Exception as e:
                                invalid_translation = {
                                    "line": line_num,
                                    "error": str(e),
                                    "vrs_allele": vo.model_dump(exclude_none=True),
                                }
                                invalid_fhir_trans_log.write(orjson.dumps(invalid_translation) + b"\n")
        finally:
            invalid_allele_log.close()
            invalid_fhir_trans_log.close()

    def main(self):
        parser = argparse.ArgumentParser(
            prog="allele-to-fhir-translator",
            description="Load a dataset and translate allele expressions (tabular) or VRS 'out' objects (jsonl) to FHIR"
        )
        parser.add_argument("input_gzip", help="Path to gzipped JSONL file")
        parser.add_argument("--invalid-allele-log", default="invalid_alleles.jsonl")
        parser.add_argument("--invalid-fhir-log", default="invalid_fhir_trans.jsonl")
        parser.add_argument("--limit", type=int, help="Process only this many lines from input")
        parser.add_argument("--verbose", action="store_true", help="Enable detailed logging")

        args = parser.parse_args()

        logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
        logging.info("Starting Translation Job")
        
        t0 = time.perf_counter()

        self.clinvartranslation(
            inputfile=args.input_gzip,
            outputfile="vrs_to_fhir_translations.jsonl",
            invalid_allele_path=args.invalid_allele_log,
            invalid_fhir_path=args.invalid_fhir_log,
            limit=args.limit,
        )

        t1 = time.perf_counter()
        logging.info(f"Translation finished in {t1 - t0:.2f} seconds")

if __name__ == "__main__":
    FastTranslation().main()