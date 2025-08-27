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
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
        cache: 'pip'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install playwright pydantic PyYAML openai python-docx pypdf tenacity rapidfuzz
        python -m playwright install --with-deps

    # 可选：先看下脚本头部，快速排 YAML 混入等低级错误
    - name: Show script head
      run: sed -n '1,40p' auto_resume_agent.py

    # 不阻塞 CI 的 lint（等稳定后再打开严格模式）
    - name: Lint Python code (non-blocking)
      run: |
        pip install flake8
        flake8 auto_resume_agent.py || true

    # 路径自检，避免因为文件不存在导致失败
    - name: Check test files exist
      run: |
        test -f ./tests/profile.yaml || (echo "missing tests/profile.yaml" && exit 1)
        test -f ./tests/resume.pdf  || (echo "missing tests/resume.pdf" && exit 1)

    - name: Run dry-run test
      run: |
        python auto_resume_agent.py apply \
          --url "https://example.com/job/123" \
          --profile ./tests/profile.yaml \
          --resume ./tests/resume.pdf \
          --dry-run \
          --max-steps 1

    - name: Archive test artifacts
      if: always()
      uses: actions/upload-artifact@v4
      with:
        name: test-logs
        path: ./
