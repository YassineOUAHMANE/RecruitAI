




activate-virtualenv:
	source .venv/bin/activate

launch-streamlit:
	streamlit run .src//frontend/app.py --server.port 8081 --server.address 0.0.0.0

launch-backend:
	uvicorn backend.main:app --reload