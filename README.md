# US2T: Explainable Test Case Generation from User Stories

Official implementation and experimental artifacts for the paper:

> US2T: Explainable Test Case Generation from User Stories

## Features

- Semantic extraction from user stories
- LLM-based test case generation
- Requirement-to-test traceability
- Human-readable explanations
- Benchmark with 109 user stories and 325 acceptance criteria

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
python src/main.py
```

## Reproduce Experiments

```bash
python experiments/run_all.py
```

## Repository Structure

```text
src/            Source code
benchmark/      Experimental datasets
experiments/    Evaluation scripts
results/        Experimental results
paper/          Paper and supplementary materials
```

## Citation

```bibtex
@article{Thanh2026US2T,
  title={US2T: Explainable Test Case Generation from User Stories},
  author={Trinh Thanh Binh and others},
  year={2026}
}
```

## License

MIT License.
