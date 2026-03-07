@echo off
echo ============================================================
echo Kisan Call Centre Query Assistant - Complete Setup
echo ============================================================
echo.

echo Step 1: Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

echo Step 2: Setting up the system...
python setup.py
if errorlevel 1 (
    echo ERROR: Setup failed
    pause
    exit /b 1
)
echo.

echo Step 3: Launching the application...
echo.
echo The app will open in your browser at http://localhost:8501
echo.
streamlit run app.py
pause
