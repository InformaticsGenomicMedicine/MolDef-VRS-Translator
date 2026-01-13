## MolDef Variation Translation — Educational Notebook Series

This repository provides a collection of interactive Jupyter notebooks that offer a hands-on introduction to the **MolDef-VRS-Translator** codebase. The notebooks demonstrate bidirectional translations between **GA4GH VRS (v2.0) Alleles** and **HL7 FHIR MolecularDefinition Allele Profile**, as well as conversions from SPDI and HGVS expressions into **HL7 FHIR MolecularDefinition Variation profiles**.

### **Recommended Knowledge**

To get the most out of these notebooks, we recommend the following prerequisites:
   - Familiarity with **Jupyter Notebook** and **Python**.
   - An understanding of the **HL7 FHIR MolecularDefinition** schema: [FHIR MolecularDefinition Schema](https://build.fhir.org/moleculardefinition.html).
   - Knowledge of the **GA4GH VRS (v2.0)** schema: [GA4GH VRS Schema](https://vrs.ga4gh.org/en/stable/).

## Notebook Categories

### **Translation Notebooks**

1) **[Simple Allele Creation & Translation](01_simple_allele_creation_and_translation.ipynb)**
   - Shows how the **Allele Builder**, which simplifies the creation of **VRS Allele** object and **FHIR Allele** profile.
   - Instead of requiring detailed knowledge of VRS or FHIR schemas, users provide just **five attributes** to generate valid Allele objects. 
   - The resulting Allele can then be used with the project’s translation tools to convert between **VRS** and **FHIR** representations.

- **[VRS to FHIR: Allele Translation](02_vrs_to_fhir_allele_translation.ipynb)**  
   - Demonstrates how **VRS Allele** representations with the **minimal required fields** are converted into **MolDef Allele Profile**.

- **[FHIR to VRS: Allele Translation](03_fhir_to_vrs_allele_translation.ipynb)**  
   - Shows how **MolDef Allele Profile** with the **minimal required elements** are translated into **VRS Allele** representations.  

- **[Full Allele Translations](04_full_allele_roundtrip_translation.ipynb)**  
   - Demonstrates the **VRSToFHIR** and **FHIRToVRS** modules for translating fully populated **VRS Allele** objects to **MolDef AlleleProfile**, and vice versa.
   - This notebook focuses on **full, schema compliant Alleles** rather than the minimal examples shown in earlier notebooks.

- **[SPDI / HGVS to FHIR Variation](05_spdi_hgvs_to_fhir_variation.ipynb)**  
  - Demonstrates how **SPDI** and **HGVS** expressions are translated into **HL7 FHIR Variation** profile resources.
