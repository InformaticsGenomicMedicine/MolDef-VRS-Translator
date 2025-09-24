## MolDef-VRS-Translator Educational Notebook Series

This repository contains a collection of interactive Jupyter notebooks designed to provide a hands-on introduction to the **MolDef-VRS-Translator** codebase. The notebooks cover working implementing bidirectional **translation between GA4GH VRS (v2.0)** and **HL7 FHIR MolecularDefinition**.

### **Recommended Knowledge**

To get the most out of these notebooks, we recommend the following prerequisites:
   - Familiarity with **Jupyter Notebook** and **Python**.
   - An understanding of the **HL7 FHIR MolecularDefinition** schema, you can review it here: [FHIR MolecularDefinition Schema](https://build.fhir.org/moleculardefinition.html).
   - Knowledge of the **GA4GH VRS (v2.0)** schema, which is essential for bidirectional translation. Documentation is available here: [GA4GH VRS Schema](https://vrs.ga4gh.org/en/stable/).

## Notebook Categories

### **Translation Notebooks** (`notebooks/translations/`)

- **[VRS to FHIR: Translation to AlleleProfile](vrs_allele_translation.ipynb)**  
   - Demonstrates how to convert **GA4GH VRS (v2.0)** representations into HL7 FHIR **AlleleProfile** resources.  

- **[FHIR to VRS: Translation to VRS Allele](fhir_allele_translation.ipynb)**  
   - Shows the process of translating HL7 FHIR **AlleleProfile** resources back into **GA4GH VRS (v2.0)** representations.  

- **[Allele Factory Demo](allele_factory_demo.ipynb)**
   - Showcases the **Allele Factory Module**, which simplifies the creation of **VRS Alleles** and **FHIR Allele** resources.
   - Since generating these profiles requires a solid understanding of the schema, this module helps users by generating an Allele with just **five input attributes**.
   - The **Allele Factory Module** reduces the learning curve by automating profile generation, making it easier for users to work with VRS and FHIR Alleles without deep prior knowledge of their schemas.

- **[Full Allele Translations](vrs_fhir_full_translation_demo.ipynb)**  
   - Demonstrates the **VRSToFHIR** and **FHIRToVRS** modules, which enable translation of fully populated **VRS Allele** objects into **FHIR Allele** resources, and vice versa.  
   - Since **FHIR includes attributes beyond those defined in VRS**, the translation is asymmetric: every VRS Allele can be represented in FHIR, but only the overlapping fields can be translated from FHIR back to VRS.  
   - This notebook goes beyond the minimal examples by focusing on **full, schema-compliant translations** within that shared subset.  
