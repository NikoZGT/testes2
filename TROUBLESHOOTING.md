# Troubleshooting - MetaTrader AI

## Erro: "Could not find a version that satisfies the requirement MetaTrader5"

Este é o erro mais comum. Aqui estão TODAS as soluções possíveis:

### ✅ Solução 1: Verificar Requisitos do Sistema

**IMPORTANTE:** MetaTrader5 Python só funciona em:
- ✓ Windows (7, 8, 10, 11)
- ✓ Python 64-bit (não funciona com 32-bit)
- ✗ Linux (não suportado oficialmente)
- ✗ Mac (não suportado oficialmente)

**Verificar seu sistema:**
```bash
python -c "import platform; print(f'SO: {platform.system()}'); print(f'Arquitetura: {platform.architecture()[0]}')"
```

**Resultado esperado:**
```
SO: Windows
Arquitetura: 64bit
```

Se aparecer `32bit`, você precisa instalar Python 64-bit!

---

### ✅ Solução 2: Instalar Python 64-bit

1. Desinstale o Python atual
2. Baixe Python 64-bit em: https://www.python.org/downloads/
3. Durante instalação:
   - Marque "Add Python to PATH"
   - Escolha instalação customizada
   - Certifique-se que é versão 64-bit
4. Reinicie o computador
5. Tente novamente: `pip install MetaTrader5`

---

### ✅ Solução 3: Instalar sem Versão Específica

```bash
# Limpar cache do pip
pip cache purge

# Instalar sem especificar versão
pip install MetaTrader5
```

---

### ✅ Solução 4: Tentar Versões Diferentes

Execute este script que tenta várias versões:

```bash
install-fix-mt5.bat
```

Ou manualmente:
```bash
pip install MetaTrader5==5.0.45
pip install MetaTrader5==5.0.44
pip install MetaTrader5==5.0.43
pip install MetaTrader5==5.0.42
```

---

### ✅ Solução 5: Instalar Outras Dependências Primeiro

Às vezes funciona instalar as outras bibliotecas primeiro:

```bash
pip install pandas numpy scikit-learn joblib
pip install MetaTrader5
```

---

### ✅ Solução 6: Usar pip com --user

```bash
pip install --user MetaTrader5
```

---

### ✅ Solução 7: Verificar Firewall/Antivirus

Temporariamente desabilite:
1. Windows Defender
2. Firewall
3. Antivirus

Então tente:
```bash
pip install MetaTrader5
```

**Lembre-se de reativar depois!**

---

### ✅ Solução 8: Baixar Manualmente

Se nada funcionar, baixe o arquivo wheel (.whl) manualmente:

1. Vá para: https://pypi.org/project/MetaTrader5/#files
2. Baixe o arquivo .whl compatível com seu Python
3. Instale localmente:
```bash
pip install C:\caminho\para\MetaTrader5-5.0.45-py3-none-win_amd64.whl
```

---

## Outros Erros Comuns

### Erro: "pip não é reconhecido"

**Causa:** Python não está no PATH

**Solução:**
1. Adicionar ao PATH manualmente:
   - Windows + R → `sysdm.cpl`
   - Aba "Avançado" → "Variáveis de Ambiente"
   - Adicionar: `C:\Python39\Scripts` e `C:\Python39`

2. Ou reinstalar Python marcando "Add to PATH"

---

### Erro: "Microsoft Visual C++ 14.0 is required"

**Solução:**
Baixe e instale: https://aka.ms/vs/17/release/vc_redist.x64.exe

---

### Erro: "Access Denied" ou "Permission Denied"

**Solução 1:** Execute CMD como Administrador

**Solução 2:** Use --user flag
```bash
pip install --user MetaTrader5
```

---

### Erro: Conexão com MT5 falha

**Sintomas:**
```
Falha ao inicializar MT5
```

**Soluções:**
1. Certifique-se que o MT5 está aberto
2. Faça login em uma conta (demo ou real)
3. Execute o MT5 como Administrador
4. Verifique se o firewall não está bloqueando
5. Reinicie o MT5

---

### Erro: "Dados insuficientes"

**Causa:** Mercado fechado ou símbolo inválido

**Soluções:**
1. Aguarde mercado abrir (evite fins de semana)
2. Verifique se o símbolo existe:
   ```python
   import MetaTrader5 as mt5
   mt5.initialize()
   symbols = mt5.symbols_get()
   print([s.name for s in symbols[:10]])
   ```
3. Use símbolo válido do seu broker

---

## Verificação Completa

Execute este comando para diagnóstico completo:

```bash
python -c "
import sys
import platform

print('=== DIAGNÓSTICO DO SISTEMA ===')
print(f'Python: {sys.version}')
print(f'Arquitetura: {platform.architecture()[0]}')
print(f'Sistema: {platform.system()}')
print(f'Versão do SO: {platform.version()}')
print()

print('=== VERIFICANDO MÓDULOS ===')
modulos = [
    'MetaTrader5',
    'pandas',
    'numpy',
    'sklearn',
    'joblib',
    'ta'
]

for modulo in modulos:
    try:
        __import__(modulo)
        print(f'✓ {modulo}')
    except:
        print(f'✗ {modulo} - FALTANDO')
"
```

---

## Instalação Passo a Passo (Do Zero)

Se nada funcionar, siga este guia do zero:

### 1. Limpar Tudo

```bash
# Desinstalar Python atual
# Fazer isso pelo Painel de Controle do Windows
```

### 2. Instalar Python Correto

1. Baixe Python 3.9 ou 3.10 (64-bit): https://www.python.org/downloads/
2. Execute instalador
3. ✓ Marque "Add Python to PATH"
4. ✓ Escolha "Customize installation"
5. ✓ Marque todas as opções
6. ✓ Em "Advanced Options" marque "Install for all users"
7. Instale
8. Reinicie computador

### 3. Verificar Python

Abra CMD novo:
```bash
python --version
pip --version
```

Deve mostrar Python 3.9 ou 3.10

### 4. Atualizar pip

```bash
python -m pip install --upgrade pip setuptools wheel
```

### 5. Instalar MetaTrader5

```bash
pip install MetaTrader5
```

### 6. Instalar Resto

```bash
pip install pandas numpy scikit-learn joblib ta matplotlib seaborn python-dotenv
```

### 7. Testar

```bash
python check_dependencies.py
```

---

## Ainda Não Funciona?

Se depois de TUDO isso ainda não funcionar:

1. **Verifique se está no Windows**
   - MetaTrader5 Python não funciona em Linux/Mac nativamente

2. **Use ambiente virtual limpo**
   ```bash
   python -m venv venv_clean
   venv_clean\Scripts\activate
   pip install MetaTrader5
   ```

3. **Tente Python 3.9 especificamente**
   - MetaTrader5 funciona melhor com Python 3.9

4. **Verifique permissões da pasta**
   - Alguns antivirus bloqueiam instalação em certas pastas

5. **Entre em contato com suporte**
   - Envie resultado do diagnóstico completo acima

---

## Links Úteis

- Python Downloads: https://www.python.org/downloads/
- MetaTrader5 PyPI: https://pypi.org/project/MetaTrader5/
- Visual C++ Redistributable: https://aka.ms/vs/17/release/vc_redist.x64.exe
- MetaTrader 5: https://www.metatrader5.com/pt/download

---

**Última atualização:** Este guia cobre todos os problemas conhecidos de instalação.
