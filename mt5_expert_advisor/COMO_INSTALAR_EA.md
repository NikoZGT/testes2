# Como Instalar o Expert Advisor no MT5

## Método 1: Copiar e Colar (MAIS FÁCIL)

### 1. Abrir MetaEditor
- No MT5, pressione **F4**
- Ou: Menu **Tools → MetaQuotes Language Editor**

### 2. Criar Novo EA
- File → New
- Selecione: **Expert Advisor (template)**
- Next
- Nome: `TradingAI_DataExporter`
- Next → Next → Finish

### 3. Copiar Código
- Abra o arquivo: `TradingAI_DataExporter.mq5` (este diretório)
- Selecione TUDO (Ctrl+A)
- Copie (Ctrl+C)

### 4. Colar no MetaEditor
- No MetaEditor, selecione tudo (Ctrl+A)
- Cole o código copiado (Ctrl+V)
- Salve (Ctrl+S)

### 5. Compilar
- Clique no botão **Compile** ou pressione **F7**
- Deve aparecer: **0 error(s), 0 warning(s)**
- Se der erro, verifique se copiou todo o código

### 6. Adicionar ao Gráfico
- Volte ao MT5
- Abra o **Navigator** (Ctrl+N)
- Expanda: **Expert Advisors**
- **Arraste** `TradingAI_DataExporter` para o gráfico desejado
- Clique **OK** na janela de configuração

### 7. Verificar Funcionamento
- Deve aparecer um **sorriso 😊** no canto superior direito do gráfico
- Abra a aba **Experts** (Ctrl+T na parte inferior)
- Deve mostrar:
  ```
  ==============================================
  Trading AI Expert Advisor Iniciado
  ==============================================
  Símbolo: EURUSD
  Timeframe: M5
  Candles: 15
  Pasta de dados: C:\Users\...\MQL5\Files\TradingAI
  ==============================================
  Dados exportados: 65 candles
  ```

---

## Método 2: Copiar Arquivo Compilado

### 1. Compilar o EA
- Siga passos 1-5 do Método 1

### 2. Localizar Arquivo Compilado
- No MetaEditor: File → Open Data Folder
- Navegue para: `MQL5\Experts\`
- Encontre: `TradingAI_DataExporter.ex5`

### 3. Copiar para Outra Instalação (opcional)
- Copie o arquivo `.ex5`
- Cole em outra instalação do MT5: `MQL5\Experts\`

---

## Configurações do EA

Clique com botão direito no EA → **Expert Advisors → Properties → Inputs**

### Parâmetros Principais:

| Parâmetro | Padrão | Descrição |
|-----------|---------|-----------|
| DataFolder | TradingAI | Pasta para arquivos CSV |
| Symbol_Name | (vazio) | Símbolo (vazio = atual) |
| Timeframe | PERIOD_M5 | M1, M5, M15, M30, H1, H4, D1 |
| NumCandles | 15 | Quantos candles analisar |
| UpdateInterval | 60 | Segundos entre atualizações |
| ShowSignals | true | Mostrar setas no gráfico |
| EnableAlerts | true | Ativar alertas sonoros |

### Timeframes Disponíveis:
- `PERIOD_M1` - 1 minuto
- `PERIOD_M5` - 5 minutos (recomendado)
- `PERIOD_M15` - 15 minutos
- `PERIOD_M30` - 30 minutos
- `PERIOD_H1` - 1 hora
- `PERIOD_H4` - 4 horas
- `PERIOD_D1` - 1 dia

---

## Ativar Trading Automático

Para o EA funcionar:

1. **Tools → Options → Expert Advisors**
   - ✅ Marque: **Allow automated trading**
   - ✅ Marque: **Allow DLL imports**

2. **Botão AutoTrading**
   - Na barra de ferramentas do MT5
   - Clique para ficar **VERDE**

3. **Configurar EA**
   - Clique com botão direito no EA
   - Expert Advisors → **Allow live trading**

---

## Verificar Arquivos Gerados

### Localizar Pasta de Dados:
1. No MetaEditor: **File → Open Data Folder**
2. Navegue para: `MQL5\Files\TradingAI\`

### Arquivos que devem existir:
```
MQL5\Files\TradingAI\
├── candles_data.csv     ← EA cria este arquivo (dados dos candles)
└── signals.csv          ← Python cria este arquivo (sinais de trading)
```

### Verificar conteúdo:
```csv
# candles_data.csv (exemplo)
time,open,high,low,close,tick_volume,real_volume,spread
2024.01.15 14:30,1.08945,1.08967,1.08932,1.08956,234,0,2
```

---

## Problemas Comuns

### Cara Triste ☹️ no Gráfico

**Causa:** Trading automático não está ativado

**Solução:**
1. Tools → Options → Expert Advisors
2. Marque "Allow automated trading"
3. Clique no botão "AutoTrading" (deve ficar verde)
4. Remova e adicione o EA novamente

---

### EA Não Compila

**Erro:** "X error(s) found"

**Solução:**
1. Verifique se copiou **TODO** o código
2. Não deve ter código anterior misturado
3. Salve o arquivo
4. Compile novamente (F7)

---

### Nenhum Arquivo Criado

**Causa:** EA não está executando

**Solução:**
1. Verifique aba "Experts" (Ctrl+T)
2. Deve mostrar "Trading AI Expert Advisor Iniciado"
3. Se não mostrar nada, EA não está rodando
4. Remova do gráfico e adicione novamente

---

### Arquivo CSV Vazio

**Causa:** Sem dados de mercado

**Solução:**
1. Aguarde mercado abrir (evite fins de semana)
2. Verifique se o símbolo é válido
3. Aguarde 60 segundos (UpdateInterval padrão)

---

## Testar se Está Funcionando

### No MT5:
1. Aba **Experts** (Ctrl+T)
2. Deve mostrar a cada 60 segundos:
   ```
   Dados exportados: X candles
   ```

### Manualmente:
1. File → Open Data Folder (no MetaEditor)
2. Navegue: `MQL5\Files\TradingAI\`
3. Abra `candles_data.csv`
4. Deve ter linhas com dados de preços

### Com Python:
1. Execute: `python trading_ai_lite.py`
2. Deve mostrar: "✓ Lidos X candles do CSV"

---

## Remover EA

1. Clique com botão direito no gráfico
2. Expert Advisors → Remove

Ou:

1. Ctrl+E (lista de EAs)
2. Selecione o EA
3. Delete

---

## Adicionar em Múltiplos Gráficos

Você pode adicionar o mesmo EA em vários gráficos:

1. Cada gráfico terá seu próprio símbolo
2. Mas compartilham a mesma pasta `TradingAI`
3. Python analisa o último arquivo exportado
4. Recomendado: Use apenas 1 gráfico por vez

---

## Próximos Passos

1. ✅ EA instalado e funcionando
2. ✅ Arquivo CSV sendo criado
3. ✅ Execute: `python trading_ai_lite.py`
4. ✅ Aguarde sinais aparecerem no gráfico

---

**Dúvidas? Veja INSTALL_LITE.md para guia completo!**
