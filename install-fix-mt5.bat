@echo off
echo ================================================
echo Fix MetaTrader5 Installation
echo ================================================
echo.

echo Verificando Python...
python --version
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    pause
    exit /b 1
)

echo.
echo Verificando arquitetura do Python...
python -c "import platform; import sys; print(f'Python: {platform.architecture()[0]}'); print(f'Windows: {platform.system()}')"

echo.
echo ================================================
echo Tentando instalar MetaTrader5...
echo ================================================
echo.

echo [Tentativa 1] Instalando versao mais recente...
pip install MetaTrader5
if errorlevel 0 goto :success

echo.
echo [Tentativa 2] Instalando com upgrade...
pip install --upgrade MetaTrader5
if errorlevel 0 goto :success

echo.
echo [Tentativa 3] Instalando versao 5.0.45...
pip install MetaTrader5==5.0.45
if errorlevel 0 goto :success

echo.
echo [Tentativa 4] Instalando versao 5.0.44...
pip install MetaTrader5==5.0.44
if errorlevel 0 goto :success

echo.
echo [Tentativa 5] Instalando versao 5.0.43...
pip install MetaTrader5==5.0.43
if errorlevel 0 goto :success

echo.
echo [Tentativa 6] Limpando cache e reinstalando...
pip cache purge
pip install --no-cache-dir MetaTrader5
if errorlevel 0 goto :success

:error
echo.
echo ================================================
echo ERRO: Nao foi possivel instalar MetaTrader5
echo ================================================
echo.
echo Possiveis causas:
echo   1. Voce nao esta no Windows
echo   2. Python 32-bit (precisa ser 64-bit)
echo   3. Problema de conexao com internet
echo   4. Firewall/Antivirus bloqueando
echo.
echo Tente:
echo   1. Verificar se esta no Windows
echo   2. Instalar Python 64-bit
echo   3. Desabilitar antivirus temporariamente
echo   4. Baixar wheel manualmente de pypi.org
echo.
pause
exit /b 1

:success
echo.
echo ================================================
echo MetaTrader5 instalado com sucesso!
echo ================================================
echo.
python -c "import MetaTrader5; print(f'Versao instalada: {MetaTrader5.__version__}')"
echo.
echo Agora instale as outras dependencias:
echo   pip install pandas numpy scikit-learn joblib ta matplotlib seaborn python-dotenv
echo.
pause
