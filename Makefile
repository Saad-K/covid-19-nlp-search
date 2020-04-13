
DIR := ${CURDIR}

install:
	python3 -m venv .venv
	source ${DIR}/.venv/bin/activate \
		&& pip install --upgrade pip \
		&& pip install -Ur requirements.txt;

run-api:
	source ${DIR}/.venv/bin/activate && uvicorn app:app;

run-ui:
	source ${DIR}/.venv/bin/activate && streamlit run ui.py;
