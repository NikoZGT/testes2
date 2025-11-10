@echo off
echo ================================================
echo MetaTrader AI Analysis - Instalador
echo ================================================
echo.

echo Verificando Python...
python --version
if errorlevel 1 (
    echo.
    echo [ERRO] Python nao encontrado!
    echo Por favor, instale Python 3.8+ de: https://www.python.org/downloads/
    echo IMPORTANTE: Marque "Add Python to PATH" durante a instalacao
    echo.
    pause
    exit /b 1
)

echo.
echo Atualizando pip...
python -m pip install --upgrade pip

echo.
echo ================================================
echo Instalando dependencias Python...
echo ================================================
echo.

pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [AVISO] Houve erros na instalacao!
    echo Tente instalar manualmente:
    echo.
    echo pip install MetaTrader5
    echo pip install pandas numpy scikit-learn joblib ta matplotlib seaborn python-dotenv
    echo.
    pause
    exit /b 1
)

echo.
echo ================================================
echo Verificando instalacao...
echo ================================================
echo.

python -c "import MetaTrader5; print('[OK] MetaTrader5 instalado')" 2>nul
if errorlevel 1 (
    echo [ERRO] MetaTrader5 nao foi instalado corretamente
    echo Execute: pip install MetaTrader5
)

python -c "import pandas; print('[OK] pandas instalado')" 2>nul
python -c "import numpy; print('[OK] numpy instalado')" 2>nul
python -c "import sklearn; print('[OK] scikit-learn instalado')" 2>nul
python -c "import ta; print('[OK] ta instalado')" 2>nul

echo.
echo ================================================
echo Instalacao concluida!
echo ================================================
echo.
echo PROXIMO PASSO:
echo   1. Abra o MetaTrader 5 e faca login
echo   2. Execute um dos comandos abaixo:
echo.
echo   - Teste rapido:           python quick_test.py
echo   - Analise continua com ML: python main.py
echo.
echo Consulte INSTALL.md para mais detalhes
echo.
pause
