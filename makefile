.PHONY: run
run:
	@poetry run python main.py

.PHONY: streamlit
streamlit:
	@poetry run streamlit run frontend.py -- --browser.gatherUsageStats=false --server.headless=false --server.address=0.0.0.0
