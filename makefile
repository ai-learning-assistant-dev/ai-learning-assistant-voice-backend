.PHONY: format
format:
    @echo "Running black..."
    python -m black .
    
    @echo "Running isort..."
    python -m isort .
    
    @echo "Running flake8..."
    python -m flake8

.PHONY: install
install:
    pip install black isort flake8