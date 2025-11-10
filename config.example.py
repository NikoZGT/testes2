"""
Arquivo de configuração de exemplo
Copie este arquivo para config.py e ajuste as configurações
"""
import MetaTrader5 as mt5

# ====== CONFIGURAÇÕES DO METATRADER ======
MT5_CONFIG = {
    # Símbolo para análise (ex: EURUSD, BTCUSD, GBPUSD, etc.)
    'symbol': 'EURUSD',

    # Timeframe - opções disponíveis:
    # mt5.TIMEFRAME_M1  (1 minuto)
    # mt5.TIMEFRAME_M5  (5 minutos)
    # mt5.TIMEFRAME_M15 (15 minutos)
    # mt5.TIMEFRAME_M30 (30 minutos)
    # mt5.TIMEFRAME_H1  (1 hora)
    # mt5.TIMEFRAME_H4  (4 horas)
    # mt5.TIMEFRAME_D1  (1 dia)
    'timeframe': mt5.TIMEFRAME_M1,

    # Número de candles para análise em tempo real
    'num_candles': 15,

    # Número de candles históricos para treinamento inicial
    'historical_candles': 500,
}

# ====== CONFIGURAÇÕES DO MODELO ML ======
ML_CONFIG = {
    # Diretório para salvar modelos
    'model_dir': 'models',

    # Quantos candles olhar à frente para criar labels
    'lookahead': 3,

    # Threshold mínimo de movimento para considerar sinal (em porcentagem)
    'threshold': 0.0001,  # 0.01%

    # Intervalo para retreinamento automático (em iterações)
    'retrain_interval': 20,

    # Tamanho do conjunto de teste
    'test_size': 0.2,
}

# ====== CONFIGURAÇÕES DE VOLUME ======
VOLUME_CONFIG = {
    # Multiplicador para detectar picos de volume (barras de interesse)
    'volume_spike_threshold': 2.0,  # Volume 2x acima da média

    # Multiplicador para volume grande
    'large_volume_threshold': 1.5,  # Volume 1.5x acima da média
}

# ====== CONFIGURAÇÕES DE EXECUÇÃO ======
EXECUTION_CONFIG = {
    # Intervalo entre análises (em segundos)
    'interval_seconds': 60,

    # Intervalo para auto-save do modelo (em segundos)
    'auto_save_interval': 300,  # 5 minutos

    # Ativar logs detalhados
    'verbose': True,
}

# ====== CONFIGURAÇÕES DE SINAIS ======
SIGNAL_CONFIG = {
    # Confiança mínima para gerar sinal (0-1)
    'min_confidence': 0.6,

    # Ativar alertas visuais
    'show_alerts': True,

    # Salvar histórico de sinais
    'save_signal_history': True,
}

# ====== CONFIGURAÇÕES DE RISCO ======
RISK_CONFIG = {
    # Stop loss em % do preço
    'stop_loss_pct': 0.5,  # 0.5%

    # Take profit em % do preço
    'take_profit_pct': 1.0,  # 1.0%

    # Tamanho de posição padrão
    'position_size': 0.01,  # 0.01 lote
}
