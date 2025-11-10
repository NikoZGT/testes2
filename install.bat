@echo off
echo ================================================
echo MetaTrader AI Analysis - Instalador
echo ================================================
echo.

echo Instalando dependencias Python...
pip install -r requirements.txt

echo.
echo ================================================
echo Instalacao concluida!
echo ================================================
echo.
echo Para executar:
echo   - Analise continua com ML: python main.py
echo   - Teste rapido: python quick_test.py
echo.
pause
