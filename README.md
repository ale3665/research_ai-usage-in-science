## Build Instructions

This repository provides an analytical framework for evaluating the reuse of Deep Neural Networks (DNNs) in scientific research. The following instructions outline the setup and build process.

### Prerequisites

Ensure that the following dependencies are installed:

- **Python 3.10** or later ([Download](https://www.python.org/downloads/release/python-3100/))
- **Poetry** (Dependency management tool)  
  Install Poetry if not already present:
  ```bash
  curl -sSL https://install.python-poetry.org | python3 -
  ```
- **Pre-commit hooks** (Optional but recommended for development)  
  ```bash
  poetry run pre-commit install
  ```

### Setup and Build Process

1. **Clone the repository**
   ```bash
   git clone https://github.com/NicholasSynovic/research_ai-usage-in-science.git
   cd research_ai-usage-in-science
   ```

2. **Install dependencies using Poetry**
   ```bash
   poetry install
   ```

3. **Set up environment variables (if applicable)**
   - Ensure necessary API keys, dataset paths, or configuration files are correctly set up.

4. **Build the project using Makefile**
   ```bash
   make build
   ```
   This will execute a series of automated setup steps, including dependency validation and any necessary pre-processing.

5. **Run tests (optional)**
   ```bash
   make test
   ```
   This ensures that all components are functioning correctly before execution.

For additional details on custom build configurations, refer to the [`Makefile`](https://github.com/NicholasSynovic/research_ai-usage-in-science/blob/main/Makefile).

---

## Software Bill of Materials (SBOM)

This project depends on a range of software libraries and tools for its functionality. Below is a structured Software Bill of Materials (SBOM):

### Core Dependencies
- **Python 3.10**: Core programming language
- **Poetry**: Dependency and environment manager
- **Pre-commit**: Automated code quality checks

### Python Packages (Extracted from `pyproject.toml`)
- **NumPy**: High-performance numerical computing
- **Pandas**: Data analysis and manipulation
- **Scikit-learn**: Machine learning utilities
- **TensorFlow/PyTorch** *(if applicable)*: Deep learning frameworks
- **NLTK/SpaCy** *(if applicable)*: Natural Language Processing utilities

### System Dependencies
- **Git**: Version control system
- **Make**: Build automation tool

To generate a full, machine-readable SBOM:

1. **Export dependency list**  
   ```bash
   poetry export --without-hashes --format=requirements.txt > sbom.txt
   ```

2. **Use GitHub’s built-in SBOM export feature**
   - Navigate to the repository’s **Insights > Dependency Graph**
   - Select **Export SBOM** to generate an SPDX-compliant output.

For further security auditing, consider tools like [Syft](https://github.com/anchore/syft) or [CycloneDX](https://cyclonedx.org/).

---

## Project Purpose and Functionality

### Purpose

The **AI Usage in Science** project investigates the prevalence and methodologies of Deep Neural Network (DNN) reuse within academic literature, particularly in high-impact mega journals. By analyzing citation patterns and methodological adaptations, this research aims to provide insights into AI’s role in modern scientific workflows.

Reusing pre-trained deep neural network models is an increasingly popular method for researchers to analyze high-dimensional, scientific data. However, DNN operationalization lacks standardization due to multiple factors, including architecture differences, training datasets, and implementation contexts. These variables evolve over time or shift between research projects, making it essential to understand the methods of DNN operationalization to evaluate their methodological soundness. 

This research addresses the gap in understanding how DNNs are reused across scientific disciplines by evaluating the software engineering methodologies applied to integrate these models within non-computing academic research. Our work extends prior studies by analyzing the accessibility and sharing mechanisms of DNNs, identifying commonly used model architectures, comparing them to state-of-the-art implementations, and examining patterns of reuse across academic publications.

By analyzing a sample of 110 academic papers from over 15,000 research articles published in the mega-journal PLOS since 2014, this project provides a systematic evaluation of DNN reuse trends and their implications for scientific reproducibility and transparency.

### Objectives

- **Identification**: Extract instances where DNN models are integrated into research papers.
- **Quantification**: Measure the frequency and scale of model reuse across disciplines.
- **Contextualization**: Categorize reuse patterns (e.g., fine-tuning, transfer learning, direct citation).
- **Visualization**: Provide intuitive data representations to highlight key trends.

### Functionality Overview

- **Data Ingestion**  
  - Automated scraping and aggregation of scientific papers (via APIs or datasets like arXiv, PubMed, IEEE Xplore).
  - Preprocessing pipelines for structured and unstructured text data.

- **Natural Language Processing (NLP) Pipeline**  
  - Named Entity Recognition (NER) to detect model references.
  - Semantic similarity analysis to track variations in model application.
  - Clustering techniques to group related works.

- **Pattern Recognition and Classification**  
  - Supervised and unsupervised learning models for categorization.
  - Statistical analysis to quantify AI model impact.

- **Visualization & Reporting**  
  - Interactive dashboards for trend analysis.
  - Research-grade reporting via Jupyter Notebooks or LaTeX documentation.

This project facilitates an in-depth understanding of how AI methodologies proliferate in academia and contributes to discussions on ethical AI reuse, citation norms, and scientific transparency.

For more details, refer to the [paper](https://github.com/NicholasSynovic/research_ai-usage-in-science).

