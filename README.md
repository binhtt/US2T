# US2T: Explainable Test Case Generation from User Stories

Official implementation and experimental artifacts for the paper:

> **US2T: Explainable Test Case Generation from User Stories**

US2T is an explainable framework for automated test generation from agile user stories. The framework combines semantic modeling and Large Language Models (LLMs) to automatically generate test cases, establish requirement-to-test traceability links, and provide human-readable explanations of requirement coverage.

---

## Features

- Automatic extraction of semantic models from user stories
- LLM-based test case generation
- Requirement-to-test traceability
- Explainable test generation
- Fallback mechanisms for invalid LLM outputs
- Benchmark consisting of 109 user stories and 325 acceptance criteria
- Experimental artifacts and reproducibility package

---

## Benchmark

The benchmark contains five software projects from different application domains.

| Project | User Stories | Acceptance Criteria |
|---------|--------------:|--------------------:|
| E-commerce | 26 | 78 |
| Online Banking | 21 | 64 |
| Course Management | 24 | 69 |
| Healthcare | 18 | 53 |
| Mobile Payment | 20 | 61 |
| **Total** | **109** | **325** |

The benchmark is available in the `benchmark/` directory.

---

## Repository Structure

```text
US2T/
│
├── src/                       # Source code
│   └── main.py
│
├── benchmark/                 # User stories and acceptance criteria
│   ├── ecommerce/
│   ├── online_banking/
│   ├── course_management/
│   ├── healthcare/
│   └── mobile_payment/
│
├── experiments/              # Scripts for reproducing experiments
│
├── results/                  # Generated test suites and RTMs
│   ├── ecommerce/
│   ├── online_banking/
│   ├── course_management/
│   ├── healthcare/
│   └── mobile_payment/
│
│
├── requirements.txt
├── README.md
└── LICENSE
```

---

## Installation

### Clone repository

```bash
git clone https://github.com/binhtt/US2T.git
cd US2T
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## Usage

Run the interactive demo:

```bash
python src/main.py
```

The tool performs the following steps:

1. Read a user story.
2. Extract a semantic model.
3. Generate explainable test cases.
4. Construct requirement traceability links.
5. Export results.

Generated files:

```text
generated_test_cases.csv
traceability_matrix.csv
```

---

## Reproducing Experiments

Run the complete experimental evaluation:

```bash
python experiments/run_all.py
```

The scripts reproduce the results reported in the paper, including:

- Requirement coverage
- Precision
- Recall
- F1-score
- Traceability accuracy

---

## Experimental Results

Average performance of US2T:

| Metric | Value |
|--------|-------:|
| Requirement Coverage | 93.4% |
| Precision | 0.92 |
| Recall | 0.91 |
| F1-score | 0.91 |
| Traceability Accuracy | 91.7% |

---

## Technologies

- Python 3.11
- Qwen2.5-3B-Instruct
- HuggingFace Transformers
- Sentence-BERT
- PyTorch
- Pandas
- Scikit-learn

---

## Citation

If you use this repository, please cite:

```bibtex
@article{Thanh2026US2T,
  title={US2T: Explainable Test Case Generation from User Stories},
  author={Trinh, Thanh Binh and Van, Cuong Nguyen and Ngoc, Minh Le and Ha, Nguyen Viet},
  year={2026}
}
```

---

## License

This project is distributed under the MIT License.

---

## Contact

**Binh-Trinh Thanh**  
Faculty of Information Systems  
Phenikaa University, Hanoi, Vietnam

Email: binh.trinhthanh@phenikaa-uni.edu.vn

---

## Acknowledgement

This repository was developed as part of the research on explainable AI-assisted software testing and automated test generation from natural language requirements.
