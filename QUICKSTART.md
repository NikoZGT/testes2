# Guia de Início Rápido

## 5 Minutos para o Primeiro Sinal

### Passo 1: Instalar (1 minuto)

```bash
# Opção 1: Windows
install.bat

# Opção 2: Manual
pip install -r requirements.txt
```

### Passo 2: Abrir MetaTrader 5 (30 segundos)

1. Abra o MetaTrader 5
2. Faça login em sua conta (demo ou real)
3. Deixe aberto em segundo plano

### Passo 3: Testar Conexão (30 segundos)

```bash
python quick_test.py
```

Se funcionar, você verá:
- ✓ Conectado com sucesso!
- Tabela com candles analisados
- Sinal de trading (compra/venda)

### Passo 4: Análise Contínua com IA (3 minutos)

```bash
python main.py
```

**Primeira Execução:**
- Sistema vai treinar modelo ML (aguarde ~2 minutos)
- Depois disso, análise contínua a cada 60 segundos

**Próximas Execuções:**
- Carrega modelo treinado automaticamente
- Começa análise imediatamente

## O Que Você Verá

### Sinal de Compra Exemplo
```
╔═══════════════════════════════════════════════╗
║        SINAL DE TRADING - MetaTrader AI      ║
╠═══════════════════════════════════════════════╣
║ 🟢 ⬆️ COMPRA (ALTA)
║
║ Preço Atual: 1.08945
║ Confiança: 82.5%
║
║ RAZÃO:
║ REVERSÃO ALTA: Sobrevendido + Volume Alto
╚═══════════════════════════════════════════════╝

RECOMENDAÇÃO: COMPRA FORTE - Entre com posição maior
```

### Sinal de Venda Exemplo
```
╔═══════════════════════════════════════════════╗
║        SINAL DE TRADING - MetaTrader AI      ║
╠═══════════════════════════════════════════════╣
║ 🔴 ⬇️ VENDA (BAIXA)
║
║ Preço Atual: 1.09134
║ Confiança: 76.3%
║
║ RAZÃO:
║ SMART MONEY: Saída de Dinheiro Institucional
╚═══════════════════════════════════════════════╝

RECOMENDAÇÃO: VENDA MODERADA - Entre com posição padrão
```

## Interpretando os Sinais

### Níveis de Confiança
- **> 75%**: FORTE - Sinal muito confiável
- **60-75%**: MODERADO - Sinal confiável
- **< 60%**: FRACO - Aguardar confirmação
- **CONFLITO**: Sinais mistos - não operar

### Tipos de Estratégia
- **REVERSÃO**: Mercado mudando de direção
- **TENDÊNCIA**: Seguindo tendência forte
- **SMART MONEY**: Dinheiro institucional entrando
- **PADRÃO**: Padrão clássico de candlestick
- **BOLLINGER**: Extremo de preço
- **VOLUME CLIMÁTICO**: Exaustão do movimento

### Barras de Interesse
Quando você vir:
```
⚠️  BARRAS DE INTERESSE detectadas: 3
    (Entrada massiva de dinheiro no mercado)
```

**Significa:**
- Volume anormal (2x+ acima da média)
- Muito dinheiro entrando/saindo
- Momento importante do mercado
- Preste atenção extra!

### Smart Money
Quando você vir:
```
💰 SMART MONEY (Compra) detectado: 2 vezes
```

**Significa:**
- Traders institucionais (bancos, fundos) operando
- Entrada de grandes volumes contra tendência
- Possível reversão importante
- Sinal forte de mudança

## Personalizar Configurações

### Alterar Símbolo (em main.py)

```python
SYMBOL = "BTCUSD"  # Trocar para Bitcoin
SYMBOL = "XAUUSD"  # Trocar para Ouro
SYMBOL = "US30"    # Trocar para Dow Jones
```

### Alterar Timeframe (em main.py)

```python
# Mais rápido (scalping)
TIMEFRAME = mt5.TIMEFRAME_M1  # 1 minuto

# Médio (day trade)
TIMEFRAME = mt5.TIMEFRAME_M5   # 5 minutos
TIMEFRAME = mt5.TIMEFRAME_M15  # 15 minutos

# Mais lento (swing)
TIMEFRAME = mt5.TIMEFRAME_H1   # 1 hora
TIMEFRAME = mt5.TIMEFRAME_H4   # 4 horas
```

### Alterar Intervalo de Análise

```python
INTERVAL_SECONDS = 30   # Analisa a cada 30 segundos
INTERVAL_SECONDS = 300  # Analisa a cada 5 minutos
```

## Dicas Importantes

### Para Iniciantes
1. **Use conta DEMO primeiro!**
2. Comece com M5 ou M15 (menos ruído)
3. Observe por alguns dias antes de operar
4. Preste atenção em sinais com confiança > 70%

### Para Avançados
1. Combine com sua própria análise
2. Use stop loss sempre
3. Observe padrões de acerto do sistema
4. Ajuste thresholds em config.py

### Gestão de Risco
- **Nunca** arrisque mais de 1-2% por operação
- Use **stop loss** sempre
- **Diversifique** (não opere só um par)
- **Teste** em demo antes de usar real

## Comandos Úteis

### Análise Única
```bash
python quick_test.py
```

### Análise Contínua
```bash
python main.py
```

### Parar Sistema
- Pressione `Ctrl+C`
- Sistema salva modelo automaticamente

## Problemas Comuns

### "Falha ao conectar MT5"
**Solução:**
- Abra o MetaTrader 5
- Faça login
- Tente novamente

### "Dados insuficientes"
**Solução:**
- Aguarde mercado abrir (evite fins de semana)
- Verifique se símbolo existe no seu broker
- Tente timeframe maior

### Sistema muito lento
**Solução:**
- Aumente `INTERVAL_SECONDS` para 120 ou mais
- Use timeframe maior (M15, H1)
- Reduza `NUM_CANDLES` para 10

## Próximos Passos

1. ✅ Teste em conta demo
2. ✅ Observe por 1 semana
3. ✅ Anote acertos e erros
4. ✅ Ajuste configurações
5. ✅ Só então considere conta real

## Suporte

- Leia o README.md completo
- Veja exemplos em quick_test.py
- Teste módulos individualmente
- Ajuste config.example.py

---

**Boa sorte e bons trades! 📈**

**Lembre-se: Trading envolve risco. Use com responsabilidade!**
