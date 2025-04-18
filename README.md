## Overview

`MolDef-Vrs-translator` provides Python-based logic for **bidirectional translation** between HL7 FHIR Allele profiles (as defined in the MolecularDefinition resource) and GA4GH [Variant Representation Specification (VRS)](https://vrs.ga4gh.org) Alleles (version 1.3).

This repository highlights the **translation component** of our broader genomics tooling suite. It contains standalone code for mapping between these two standards, with the goal of supporting interoperability between clinical and research genomic data systems.

---

### Looking to Use This Code?

This repository contains a standalone copy of the translation logic used in the [FHIR-MolDef-python](https://github.com/InformaticsGenomicMedicine/FHIR-MolDef-python) project.

It has been separated into its own repository to reflect the modular structure of our tooling suite and to highlight the translation functionality between FHIR Alleles and GA4GH VRS Alleles.

If you are looking to use or explore this code in practice, including fully functional examples, test coverage, and interactive notebooks, please visit the main implementation repository:

[FHIR-MolDef-python](https://github.com/InformaticsGenomicMedicine/FHIR-MolDef-python)

There you will find:

- Integrated translation logic alongside model definitions  
- Example notebooks demonstrating usage  
- A complete test suite for validation

---

## Acknowledgments
This project relies on the following packages and resources. We extend our gratitude to their respective developers and contributors for making these tools freely available:

- **[vrs-python](https://github.com/ga4gh/vrs-python)**
- **[biocommons.seqrepo](https://github.com/biocommons/biocommons.seqrepo)**
- **[biocommons.seqrepo-rest-services](https://github.com/biocommons/seqrepo-rest-service)**
- **[HL7 FHIR](https://hl7.org/fhir/6.0.0-ballot2/moleculardefinition.html)**
- **[fhir.resource](https://github.com/nazrulworld/fhir.resources)**
- **[fhir-core](https://github.com/nazrulworld/fhir-core)**