# Instalação LITE - Versão Simplificada SEM MetaTrader5 Python

## 🎯 Esta é a solução MAIS FÁCIL e LEVE!

Sem precisar instalar a biblioteca MetaTrader5 complicada!
Funciona com Expert Advisor que exporta dados para CSV.

---

## 📋 O Que Você Precisa

✅ **Python 3.8+** (qualquer versão, 32 ou 64-bit)
✅ **MetaTrader 5** (aplicativo normal)
✅ **5 bibliotecas Python básicas** (pandas, numpy, scikit-learn, joblib, ta)

❌ **NÃO precisa** da biblioteca MetaTrader5
❌ **NÃO precisa** Python 64-bit obrigatoriamente
❌ **NÃO precisa** configurações complexas

---

## 🚀 Instalação em 3 Passos

### Passo 1: Instalar Python Básico

```bash
# Apenas 5 bibliotecas essenciais!
pip install pandas numpy scikit-learn joblib ta
```

Ou use o arquivo pronto:
```bash
cd python_lite
pip install -r requirements_lite.txt
```

**Pronto! Sem complicação!**

---

### Passo 2: Instalar Expert Advisor no MT5

1. **Abra o MetaTrader 5**

2. **Abra o MetaEditor** (F4 ou menu Tools → MetaEditor)

3. **Criar novo Expert Advisor:**
   - File → New → Expert Advisor (template)
   - Nome: `TradingAI_DataExporter`
   - Next → Next → Finish

4. **Copiar o código:**
   - Abra o arquivo: `mt5_expert_advisor/TradingAI_DataExporter.mq5`
   - Copie TUDO
   - Cole no MetaEditor (substitua tudo)

5. **Compilar:**
   - Clique em "Compile" (F7)
   - Deve mostrar "0 errors"

6. **Adicionar ao gráfico:**
   - Volte ao MT5
   - Navegador (Ctrl+N) → Expert Advisors
   - Arraste `TradingAI_DataExporter` para o gráfico
   - Clique OK

7. **Verificar:**
   - Deve aparecer um sorriso 😊 no canto superior direito do gráfico
   - Na aba "Experts" (Ctrl+T) deve mostrar: "Trading AI Expert Advisor Iniciado"

---

### Passo 3: Executar Python

```bash
cd python_lite
python trading_ai_lite.py
```

**E pronto! Está funcionando!**

---

## 🔄 Como Funciona

```
┌─────────────────┐         ┌──────────────┐         ┌─────────────────┐
│  MetaTrader 5   │ ──CSV──→│    Pasta     │ ──CSV──→│  Python Lite    │
│  Expert Advisor │         │ Compartilhada│         │  (Análise IA)   │
└─────────────────┘         └──────────────┘         └─────────────────┘
         ↑                                                      │
         │                 ┌──────────────┐                    │
         └─────CSV────────│    Sinais    │←──────CSV──────────┘
                          │  (Setas MT5) │
                          └──────────────┘
```

1. **EA no MT5** exporta candles para CSV a cada 60 segundos
2. **Python** lê o CSV, faz análise completa com IA
3. **Python** salva sinais em outro CSV
4. **EA** lê os sinais e mostra setas no gráfico do MT5

---

## 📁 Estrutura de Arquivos

```
C:\Users\{SEU_USER}\AppData\Roaming\MetaQuotes\Terminal\{ID}\MQL5\Files\TradingAI\
├── candles_data.csv     ← EA exporta aqui
└── signals.csv          ← Python salva aqui
```

O Python detecta essa pasta automaticamente!

---

## ✅ Verificar se Está Funcionando

### No MetaTrader 5:
- Aba "Experts" deve mostrar: "Dados exportados: X candles"
- Arquivo criado em: `MQL5\Files\TradingAI\candles_data.csv`

### No Python:
- Deve mostrar: "✓ Lidos X candles do CSV"
- Depois: "✓ Sinal salvo: {estratégia}"

### No MT5 novamente:
- Setas aparecem no gráfico (🟢 compra, 🔴 venda)
- Alertas sonoros quando há sinal forte

---

## ⚙️ Configurações

### No Expert Advisor (MT5):

Clique com botão direito no EA → Properties → Inputs:

```
DataFolder = "TradingAI"          // Nome da pasta
Symbol_Name = ""                  // Vazio = símbolo atual
Timeframe = PERIOD_M5             // M1, M5, M15, H1, etc.
NumCandles = 15                   // Quantos candles analisar
UpdateInterval = 60               // Segundos entre atualizações
ShowSignals = true                // Mostrar setas no gráfico
EnableAlerts = true               // Alertas sonoros
```

### No Python:

Edite `trading_ai_lite.py`:

```python
ai.run_continuous(interval_seconds=60)  # Mudar intervalo
```

---

## 🎨 Sinais no Gráfico

Quando o Python detecta um sinal, o EA mostra:

- **🟢 Seta Verde para CIMA** = Sinal de COMPRA
- **🔴 Seta Vermelha para BAIXO** = Sinal de VENDA
- **Texto** = Nome da estratégia + % de confiança
- **Alerta Sonoro** = Quando confiança > 70%

---

## 🐛 Resolução de Problemas

### Python não encontra os dados

**Sintoma:**
```
⚠️  Aguardando dados do Expert Advisor...
```

**Soluções:**
1. Verifique se EA está rodando no MT5 (sorriso 😊 no gráfico)
2. Olhe na aba "Experts" se aparece "Dados exportados"
3. Verifique manualmente se o arquivo existe:
   ```
   C:\Users\{USER}\AppData\Roaming\MetaQuotes\Terminal\{ID}\MQL5\Files\TradingAI\candles_data.csv
   ```
4. Se não encontrar, o Python usa pasta local: `python_lite/data/`

### EA não compila

**Sintoma:** "Errors: X" no MetaEditor

**Solução:**
- Certifique-se de copiar TODO o código
- Salve o arquivo
- Compile novamente (F7)

### EA não inicia no gráfico

**Sintoma:** Cara triste ☹️ no gráfico

**Soluções:**
1. Tools → Options → Expert Advisors:
   - ✅ Marque "Allow automated trading"
   - ✅ Marque "Allow DLL imports"
2. Clique em "AutoTrading" na barra de ferramentas (deve ficar verde)
3. Remova e adicione o EA novamente

### Python dá erro ao importar

**Sintoma:**
```
ModuleNotFoundError: No module named 'pandas'
```

**Solução:**
```bash
pip install pandas numpy scikit-learn joblib ta
```

---

## 🔥 Vantagens desta Solução

✅ **Muito mais leve** - Apenas 5 bibliotecas
✅ **Sem MetaTrader5 complicado** - Não precisa da biblioteca problemática
✅ **Funciona em qualquer Python** - 32-bit ou 64-bit
✅ **Fácil de debugar** - Arquivos CSV são legíveis
✅ **Separação clara** - MT5 faz uma coisa, Python faz outra
✅ **Mesma IA poderosa** - Todas as estratégias e ML funcionam

---

## 📊 Exemplo de Uso

1. **Manhã:** Abrir MT5, adicionar EA ao gráfico
2. **Executar:** `python trading_ai_lite.py` em outra janela
3. **Observar:** Sinais aparecem automaticamente no MT5
4. **Negociar:** Seguir recomendações da IA
5. **Fechar:** Ctrl+C no Python, fechar MT5

---

## 🎓 Próximos Passos

1. ✅ Instale Python básico: `pip install -r requirements_lite.txt`
2. ✅ Adicione o EA ao MT5
3. ✅ Execute: `python trading_ai_lite.py`
4. ✅ Observe por alguns dias
5. ✅ Use em conta demo primeiro
6. ✅ Só depois considere conta real

---

## 💡 Dicas

- **Timeframe M5** é bom para começar
- **UpdateInterval = 60s** no EA é suficiente
- **Deixe treinar 1-2 horas** para ML melhorar
- **Preste atenção em sinais > 75% confiança**
- **Use stop loss sempre!**

---

## 📞 Suporte

Se tiver problemas:

1. Verifique aba "Experts" no MT5 (Ctrl+T)
2. Veja mensagens do Python
3. Confirme que arquivos CSV existem
4. Leia mensagens de erro com atenção

---

**Pronto! Agora você tem uma IA de trading poderosa sem complicação! 🚀**

**Boa sorte e bons trades! 📈**
