name: CI

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install playwright pydantic PyYAML openai python-docx pypdf tenacity rapidfuzz
        playwright install --with-deps

    - name: Lint Python code
      run: |
        pip install flake8
        flake8 auto_resume_agent.py

    - name: Run dry-run test
      run: |
        python auto_resume_agent.py apply \
          --url "https://example.com/job/123" \
          --profile ./tests/profile.yaml \
          --resume ./tests/resume.pdf \
          --dry-run

    - name: Archive test artifacts
      if: always()
      uses: actions/upload-artifact@v3
      with:
        name: test-logs
        path: ./
