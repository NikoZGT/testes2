# MetaTrader AI Analysis com Machine Learning

Sistema avançado de análise de trading para MetaTrader 5 com inteligência artificial e aprendizado de máquina adaptativo.

## Características Principais

- **Análise Técnica Completa**: RSI, MACD, Bollinger Bands, EMA, SMA, ATR, Stochastic, ADX
- **Detecção de Padrões de Candlestick**: Doji, Hammer, Shooting Star, Engulfing, Marubozu
- **Análise de Volume Inteligente**: Detecta barras de interesse (entrada massiva de dinheiro)
- **Smart Money Detection**: Identifica possível entrada de dinheiro institucional
- **Machine Learning Adaptativo**: Aprende continuamente durante a sessão
- **7 Estratégias de Trading**: Sistema multi-estratégias com confirmação cruzada
- **Sinais Claros**: Setas de compra/venda com níveis de confiança
- **Auto-Save**: Salva modelo automaticamente para melhorias contínuas

## Como Funciona

O sistema analisa os últimos 15 candles do MetaTrader 5 e cruza múltiplas informações:

1. **Análise de Preços**: Máxima, mínima, abertura, fechamento
2. **Análise de Volume**: Detecta quando entra muito dinheiro no mercado
3. **Indicadores Técnicos**: 10+ indicadores profissionais
4. **Padrões de Candles**: Reconhecimento automático de padrões
5. **Machine Learning**: Modelo que aprende com os dados e fica mais preciso

### Estratégias Implementadas

1. **Reversão de Tendência com Volume**: Detecta mudanças de direção do mercado
2. **Confirmação de Tendência**: Segue tendências fortes confirmadas
3. **Smart Money**: Detecta entrada/saída de traders institucionais
4. **Padrões de Candlestick**: Usa padrões clássicos com confirmação
5. **Bollinger Bands**: Identifica extremos de preço
6. **Volume Climático**: Detecta exaustão de compradores/vendedores
7. **Machine Learning**: Predições baseadas em padrões aprendidos

## Instalação

### Requisitos

- Python 3.8+
- MetaTrader 5 instalado e configurado
- Windows (requerido pelo MT5)

### Passo a Passo

1. Clone o repositório:
```bash
git clone <seu-repositorio>
cd testes2
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Certifique-se de que o MetaTrader 5 está instalado e funcionando

## Uso

### Modo 1: Análise Contínua com Machine Learning (Recomendado)

Execute o sistema principal que analisa continuamente e aprende:

```bash
python main.py
```

**O que acontece:**
- Conecta ao MetaTrader 5
- Treina modelo ML com dados históricos (primeira vez)
- Analisa mercado a cada 60 segundos
- Gera sinais de compra/venda com setas
- Aprende continuamente e melhora precisão
- Salva modelo automaticamente

**Configurações no `main.py`:**
```python
SYMBOL = "EURUSD"           # Símbolo para análise
TIMEFRAME = mt5.TIMEFRAME_M1  # Timeframe (M1, M5, M15, etc.)
NUM_CANDLES = 15            # Número de candles para análise
INTERVAL_SECONDS = 60       # Intervalo entre análises
```

### Modo 2: Análise Rápida (Sem ML)

Para uma análise rápida sem machine learning:

```bash
python quick_test.py
```

**O que acontece:**
- Conecta ao MT5
- Coleta 15 candles
- Faz análise técnica completa
- Mostra sinais e recomendações
- Desconecta (análise única)

### Modo 3: Teste Individual de Componentes

Teste cada módulo individualmente:

```bash
# Testar coletor de dados
python src/data_collector/mt5_collector.py

# Testar análise técnica
python src/technical_analysis/candle_analyzer.py

# Testar análise de volume
python src/technical_analysis/volume_analyzer.py
```

## Estrutura do Projeto

```
testes2/
├── main.py                      # Script principal (análise contínua + ML)
├── quick_test.py               # Teste rápido (análise única)
├── config.example.py           # Configurações de exemplo
├── requirements.txt            # Dependências Python
├── README.md                   # Este arquivo
│
├── src/
│   ├── data_collector/         # Coleta de dados do MT5
│   │   └── mt5_collector.py
│   │
│   ├── technical_analysis/     # Análise técnica
│   │   ├── candle_analyzer.py   # Indicadores e padrões
│   │   └── volume_analyzer.py   # Análise de volume
│   │
│   ├── ml_model/               # Machine Learning
│   │   └── trading_model.py     # Modelo de ML adaptativo
│   │
│   └── signal_generator/       # Geração de sinais
│       └── signal_generator.py  # Sistema de sinais
│
├── models/                     # Modelos ML salvos
└── logs/                       # Logs do sistema
```

## Exemplo de Saída

```
╔═══════════════════════════════════════════════╗
║        SINAL DE TRADING - MetaTrader AI      ║
╠═══════════════════════════════════════════════╣
║ 🟢 ⬆️ COMPRA (ALTA)
║
║ Timestamp: 2024-01-15 14:30:00
║ Preço Atual: 1.08945
║ Confiança: 82.5%
║
║ Volume: 5420
║ RSI: 32.45
║ MACD: -0.00012
║
║ RAZÃO:
║ REVERSÃO ALTA: Sobrevendido + Volume Alto +
║ Candle de Alta | SMART MONEY: Entrada de
║ Dinheiro Institucional - COMPRA
╚═══════════════════════════════════════════════╝

RECOMENDAÇÃO: COMPRA FORTE - Entre com posição maior
```

## Indicadores Técnicos Analisados

### Momentum
- **RSI** (14 períodos): Identifica sobrecompra/sobrevenda
- **Stochastic** (K, D): Momentum de curto prazo
- **MACD**: Convergência/divergência de médias móveis

### Tendência
- **EMA** (9, 21): Médias exponenciais
- **SMA** (50): Média simples
- **ADX** (14): Força da tendência

### Volatilidade
- **ATR**: Average True Range
- **Bollinger Bands** (20, 2): Bandas de preço

### Volume
- **OBV**: On-Balance Volume
- **VPT**: Volume Price Trend
- **VWAP**: Volume Weighted Average Price
- **Barras de Interesse**: Picos de volume anormais

## Machine Learning

### Modelo Utilizado
- **Gradient Boosting Classifier**
- 100 estimadores
- Learning rate: 0.1
- Max depth: 5

### Features Utilizadas
- 30+ features derivadas de:
  - Indicadores técnicos
  - Padrões de candlestick
  - Análise de volume
  - Relações de preço
  - Momentum de preço e volume

### Aprendizado Contínuo
O modelo:
1. Treina inicialmente com 500 candles históricos
2. Re-treina a cada 20 iterações com novos dados
3. Salva automaticamente a cada 5 minutos
4. Melhora precisão ao longo do tempo

## Barras de Interesse (Smart Money)

O sistema detecta quando entra muito dinheiro no mercado:

- **Volume Spike**: Volume 2x acima da média
- **Volume Extremo**: Volume 3x+ acima da média
- **Smart Money Compra**: Volume alto em correção de baixa
- **Smart Money Venda**: Volume alto em correção de alta
- **Volume Climático**: Exaustão com volume extremo

## Configuração Avançada

Copie o arquivo de configuração:
```bash
cp config.example.py config.py
```

Edite `config.py` para ajustar:
- Símbolos e timeframes
- Thresholds de volume
- Parâmetros do ML
- Intervalos de execução
- Configurações de risco

## Logs

Todos os logs são salvos em:
- `logs/trading_ai.log` - Log completo do sistema

## Modelos Salvos

Modelos ML são salvos em:
- `models/trading_model_YYYYMMDD_HHMMSS.pkl` - Modelos automáticos
- `models/trading_model_final.pkl` - Modelo ao fechar sistema

Para usar um modelo existente, ele será carregado automaticamente na próxima execução.

## Dicas de Uso

1. **Primeira Vez**: Deixe treinar com dados históricos (leva ~1-2 minutos)
2. **Timeframes**: M5 ou M15 são bons para começar (menos ruído)
3. **Confiança**: Sinais com confiança > 75% são mais confiáveis
4. **Conflitos**: Sinais "CONFLITO" = aguardar próxima análise
5. **Volume**: Sempre observe barras de interesse (entrada de dinheiro)
6. **Aprendizado**: Quanto mais o sistema roda, mais preciso fica

## Símbolos Suportados

Qualquer símbolo disponível no seu MetaTrader 5:
- **Forex**: EURUSD, GBPUSD, USDJPY, etc.
- **Índices**: US30, NAS100, SP500, etc.
- **Commodities**: XAUUSD (ouro), XBRUSD (petróleo), etc.
- **Cripto**: BTCUSD, ETHUSD, etc. (se disponível)

## Timeframes Disponíveis

```python
mt5.TIMEFRAME_M1   # 1 minuto
mt5.TIMEFRAME_M5   # 5 minutos
mt5.TIMEFRAME_M15  # 15 minutos
mt5.TIMEFRAME_M30  # 30 minutos
mt5.TIMEFRAME_H1   # 1 hora
mt5.TIMEFRAME_H4   # 4 horas
mt5.TIMEFRAME_D1   # 1 dia
```

## Troubleshooting

### Erro ao conectar ao MT5
- Certifique-se de que o MetaTrader 5 está aberto
- Verifique se está logado em uma conta
- Execute o script com permissões adequadas

### Dados insuficientes
- Aguarde o mercado abrir (evite fins de semana)
- Verifique se o símbolo está correto
- Tente um timeframe maior

### Modelo não treina
- Precisa de pelo menos 50 candles com dados válidos
- Aumente `historical_candles` em config.py
- Verifique conexão com MT5

## Performance e Recursos

- **CPU**: Leve (análise ML rápida)
- **RAM**: ~200-500 MB
- **Disco**: ~10-50 MB (modelos salvos)
- **Rede**: Apenas comunicação local com MT5

## Avisos Importantes

⚠️ **AVISO DE RISCO**: Este sistema é para fins educacionais e de pesquisa. Trading envolve risco significativo de perda. Sempre:
- Teste em conta demo primeiro
- Use gestão de risco adequada
- Não invista mais do que pode perder
- Não confie 100% em sistemas automatizados
- Faça sua própria análise

⚠️ **MACHINE LEARNING**: O modelo aprende com dados históricos, mas o mercado é imprevisível. Performance passada não garante resultados futuros.

## Melhorias Futuras

- [ ] Adicionar mais estratégias de trading
- [ ] Implementar backtesting automático
- [ ] Interface gráfica (GUI)
- [ ] Suporte para múltiplos símbolos simultâneos
- [ ] Sistema de notificações (email/telegram)
- [ ] Gestão de risco automática
- [ ] Deep Learning (LSTM/Transformer)

## Licença

Este projeto é fornecido "como está", sem garantias.

## Suporte

Para questões e suporte:
- Abra uma issue no repositório
- Leia a documentação do MetaTrader 5
- Consulte exemplos em `quick_test.py`

## Créditos

Desenvolvido com:
- MetaTrader5 API
- scikit-learn
- pandas
- ta (Technical Analysis library)

---

**Desenvolvido para análise inteligente de mercados financeiros com IA**

**Boa sorte e bons trades! 📈**
