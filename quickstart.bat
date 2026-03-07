@echo off
echo ============================================================
echo Kisan Call Centre Query Assistant - Quick Start
echo ============================================================
echo.

echo Step 1: Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error installing dependencies!
    pause
    exit /b 1
)
echo.

echo Step 2: Running setup...
python setup.py
if %errorlevel% neq 0 (
    echo Error during setup!
    pause
    exit /b 1
)
echo.

echo Step 3: Testing system...
python test_system.py
if %errorlevel% neq 0 (
    echo Warning: Some tests failed. Check output above.
)
echo.

echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo Next steps:
echo 1. Configure IBM Watsonx credentials in .env file (optional)
echo 2. Run the application: streamlit run app.py
echo.
echo Press any key to start the application...
pause > nul

streamlit run app.py
