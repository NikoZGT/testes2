@echo off
echo ================================================
echo Trading AI LITE - Instalador Simplificado
echo ================================================
echo.
echo Esta versao NAO precisa da biblioteca MetaTrader5!
echo Apenas 5 bibliotecas essenciais.
echo.
pause

echo Verificando Python...
python --version
if errorlevel 1 (
    echo.
    echo [ERRO] Python nao encontrado!
    echo Instale Python de: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo Atualizando pip...
python -m pip install --upgrade pip

echo.
echo ================================================
echo Instalando apenas 5 bibliotecas essenciais...
echo ================================================
echo.

pip install pandas
pip install numpy
pip install scikit-learn
pip install joblib
pip install ta

if errorlevel 1 (
    echo.
    echo [ERRO] Falha na instalacao
    echo Tente manualmente:
    echo   pip install pandas
    echo   pip install numpy
    echo   pip install scikit-learn
    echo   pip install joblib
    echo   pip install ta
    pause
    exit /b 1
)

echo.
echo ================================================
echo Verificando instalacao...
echo ================================================

python -c "import pandas; print('[OK] pandas')"
python -c "import numpy; print('[OK] numpy')"
python -c "import sklearn; print('[OK] scikit-learn')"
python -c "import joblib; print('[OK] joblib')"
python -c "import ta; print('[OK] ta')"

echo.
echo ================================================
echo INSTALACAO CONCLUIDA COM SUCESSO!
echo ================================================
echo.
echo PROXIMOS PASSOS:
echo.
echo 1. Abra o MetaTrader 5
echo 2. Adicione o Expert Advisor ao grafico
echo    (arquivo: mt5_expert_advisor\TradingAI_DataExporter.mq5)
echo 3. Execute: python trading_ai_lite.py
echo.
echo Leia INSTALL_LITE.md para instrucoes completas
echo.
pause
