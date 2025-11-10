# Guia de Instalação - MetaTrader AI

## Passo a Passo para Windows

### 1. Instalar Python (se ainda não tiver)

1. Baixe Python 3.8+ em: https://www.python.org/downloads/
2. Durante instalação, MARQUE: "Add Python to PATH"
3. Verifique instalação:
```bash
python --version
```

### 2. Instalar Dependências

Abra o **Prompt de Comando** (CMD) ou **PowerShell** na pasta do projeto e execute:

```bash
pip install -r requirements.txt
```

Ou instale manualmente uma por uma:

```bash
pip install MetaTrader5
pip install pandas
pip install numpy
pip install scikit-learn
pip install joblib
pip install ta
pip install matplotlib
pip install seaborn
pip install python-dotenv
```

### 3. Verificar Instalação do MetaTrader5

```bash
python -c "import MetaTrader5; print('MetaTrader5 instalado com sucesso!')"
```

Se der erro, tente:

```bash
pip install --upgrade MetaTrader5
```

### 4. Instalar MetaTrader 5 (aplicativo)

1. Baixe em: https://www.metatrader5.com/pt/download
2. Instale e configure uma conta (demo ou real)
3. Deixe o MT5 aberto e logado

### 5. Testar Sistema

```bash
python quick_test.py
```

---

## Problemas Comuns

### Erro: "ModuleNotFoundError: No module named 'MetaTrader5'"

**Solução:**
```bash
pip install MetaTrader5
```

Se continuar com erro:
```bash
python -m pip install --upgrade pip
pip install --upgrade MetaTrader5
```

### Erro: "Could not find a version that satisfies the requirement MetaTrader5"

**Problema:** O MetaTrader5 só está disponível para Windows

**Solução 1 - Verificar Sistema Operacional:**
- MetaTrader5 Python só funciona no Windows
- Se está no Linux/Mac, não é possível usar esta biblioteca
- Alternativa: Use Wine no Linux ou VM Windows

**Solução 2 - Instalar sem especificar versão:**
```bash
pip install MetaTrader5
```

**Solução 3 - Usar repositório alternativo (se disponível):**
```bash
pip install --index-url https://pypi.org/simple MetaTrader5
```

**Solução 4 - Instalar versão específica:**
```bash
# Tente versões diferentes
pip install MetaTrader5==5.0.45
pip install MetaTrader5==5.0.44
pip install MetaTrader5==5.0.43
```

**Solução 5 - Verificar arquitetura do Python:**
```bash
python -c "import platform; print(platform.architecture())"
```
- Se mostrar 32-bit, instale Python 64-bit
- MetaTrader5 requer Python 64-bit no Windows

### Erro: "pip não é reconhecido"

**Solução:** Python não está no PATH

1. Desinstale Python
2. Reinstale marcando "Add Python to PATH"

Ou adicione manualmente:
```bash
set PATH=%PATH%;C:\Python39\Scripts
```

### Erro: "Microsoft Visual C++ 14.0 is required"

**Solução:** Instale Visual C++ Redistributable
- Download: https://aka.ms/vs/17/release/vc_redist.x64.exe

### Erro ao conectar ao MT5

**Soluções:**
1. Certifique-se que o MetaTrader 5 está aberto
2. Faça login em uma conta
3. Execute o script novamente

### Erro: "Access denied"

**Solução:** Execute CMD/PowerShell como Administrador

---

## Instalação Alternativa (Virtual Environment)

Recomendado para evitar conflitos:

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar (Windows)
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Executar
python main.py
```

---

## Verificação Completa

Execute este script para verificar tudo:

```bash
python -c "
import sys
print(f'Python: {sys.version}')

try:
    import MetaTrader5
    print('✓ MetaTrader5')
except: print('✗ MetaTrader5 - Execute: pip install MetaTrader5')

try:
    import pandas
    print('✓ pandas')
except: print('✗ pandas - Execute: pip install pandas')

try:
    import numpy
    print('✓ numpy')
except: print('✗ numpy - Execute: pip install numpy')

try:
    import sklearn
    print('✓ scikit-learn')
except: print('✗ scikit-learn - Execute: pip install scikit-learn')

try:
    import joblib
    print('✓ joblib')
except: print('✗ joblib - Execute: pip install joblib')

try:
    import ta
    print('✓ ta')
except: print('✗ ta - Execute: pip install ta')

print('\\nSe todos marcados com ✓, está pronto!')
"
```

---

## Suporte

Se continuar com problemas:

1. Verifique versão do Python: `python --version` (precisa ser 3.8+)
2. Atualize pip: `python -m pip install --upgrade pip`
3. Tente instalar um pacote de cada vez
4. Use ambiente virtual (venv)
5. Execute como Administrador

---

**Depois de instalar tudo, execute:**
```bash
python quick_test.py
```

Boa sorte! 🚀
