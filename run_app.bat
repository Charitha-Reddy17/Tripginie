@echo off
echo Installing requirements (if not installed)...
python -m pip install -r requirements.txt
echo.
echo Starting TripGenie AI Trip Planner...
python -m streamlit run a.py
pause
