.venv:
	@poetry install

.PHONY: run
run: .venv
	@poetry run streamlit run main.py --browser.gatherUsageStats=false --server.headless=false --server.address=0.0.0.0
