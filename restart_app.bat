@echo off
echo Clearing Streamlit cache...
rmdir /s /q .streamlit 2>nul
echo.
echo Restarting application with fresh configuration...
echo.
streamlit run app.py
