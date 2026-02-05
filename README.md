## Overview

`MolDef-vrs-translator` is a Python implementation for bidirectional translation between:

* **HL7 FHIR MolecularDefinition** - Allele Profile
* **GA4GH Variant Representation Specification** [(VRS)](https://vrs.ga4gh.org) - Allele (version 2.0)

This repository isolates the translation layer from our broader genomics tooling suite, providing a focused, standalone implementation for mapping between these two standards.

---
---
## Local Setup

Follow these steps to set up the project for local development.

### 1. Clone the Repository
Make sure you’re logged into GitHub, then clone the repository and navigate into it:

```bash
# Clone the repository
git clone https://github.com/yourusername/MolDef-VRS-Translator.git
cd MolDef-VRS-Translator
```

### 2. Create and Activate a Virtual Environment
We recommend using Python’s built-in `venv` module.

   ```bash
   python -m venv venv
   ```

Activate the virtual environment

- **macOS/Linux**
   ```bash
   source venv/bin/activate
   ```
- **Windows** 
   ```bash
   venv\Scripts\activate
   ```

### 3. Install the Package
- **Installation (until the package is published)**
   ```bash
   pip install . 
   ```

- **Local Development**
   ```bash
   pip install -e .[dev]
   ```

### 4. Verify Installation
Confirm the package was installed successfully
   ```bash
   pip show fhir.moldef.translator
   ```

## Jupyter Notebooks

This repository includes example Jupyter notebooks for exploring and experimenting with the project.

* **[`notebooks/README.md`](notebooks/README.md)**

<!-- ### Getting Started
This project is not yet published on PyPI and is still under active development.

If you would like to perform translations or explore the interactive translation notebooks, please see the
[FHIR-MolDef-python](https://github.com/InformaticsGenomicMedicine/FHIR-MolDef-python) project. 

That main repository includes:

* Fully functional examples
* Complete test suite
* Interactive notebooks
* Codespaces environment that lets you run the code without installing locally 

Refer to its README for step-by-step instructions and setup details.  -->

---
### Roadmap & Integration Plans
**Now**
* Packaging **[MolDef-spec-python](https://github.com/InformaticsGenomicMedicine/MolDef-spec-python)**
    * Contains the MolecularDefinition schema and the Allele/Sequence profiles
    * Will be integrated as a dependency once finalized

**Next**
* Package **MolDef-vrs-translator** as a standalone, installable Python package


## Acknowledgments
This project builds on the following packages and resources.

- **[vrs-python](https://github.com/ga4gh/vrs-python)**
- **[biocommons.seqrepo](https://github.com/biocommons/biocommons.seqrepo)**
- **[biocommons.seqrepo-rest-services](https://github.com/biocommons/seqrepo-rest-service)**
- **[HL7 FHIR](https://hl7.org/fhir/6.0.0-ballot2/moleculardefinition.html)**
- **[fhir.resource](https://github.com/nazrulworld/fhir.resources)**
- **[fhir-core](https://github.com/nazrulworld/fhir-core)**
- **[MolDef-spec-python](https://github.com/InformaticsGenomicMedicine/MolDef-spec-python)**