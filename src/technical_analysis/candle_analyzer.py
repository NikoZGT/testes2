"""
Módulo para análise técnica de candles
"""
import pandas as pd
import numpy as np
import ta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CandleAnalyzer:
    """Analisa padrões técnicos em candles"""

    def __init__(self):
        pass

    def calculate_indicators(self, df):
        """
        Calcula indicadores técnicos nos dados

        Args:
            df (pd.DataFrame): DataFrame com colunas abertura, maxima, minima, fechamento, volume

        Returns:
            pd.DataFrame: DataFrame com indicadores adicionados
        """
        df = df.copy()

        # RSI (Relative Strength Index)
        df['rsi'] = ta.momentum.RSIIndicator(df['fechamento'], window=14).rsi()

        # MACD (Moving Average Convergence Divergence)
        macd = ta.trend.MACD(df['fechamento'])
        df['macd'] = macd.macd()
        df['macd_signal'] = macd.macd_signal()
        df['macd_diff'] = macd.macd_diff()

        # Bollinger Bands
        bollinger = ta.volatility.BollingerBands(df['fechamento'], window=20)
        df['bb_high'] = bollinger.bollinger_hband()
        df['bb_mid'] = bollinger.bollinger_mavg()
        df['bb_low'] = bollinger.bollinger_lband()
        df['bb_width'] = bollinger.bollinger_wband()

        # EMA (Exponential Moving Average)
        df['ema_9'] = ta.trend.EMAIndicator(df['fechamento'], window=9).ema_indicator()
        df['ema_21'] = ta.trend.EMAIndicator(df['fechamento'], window=21).ema_indicator()

        # SMA (Simple Moving Average)
        df['sma_50'] = ta.trend.SMAIndicator(df['fechamento'], window=50).sma_indicator()

        # ATR (Average True Range) - Volatilidade
        df['atr'] = ta.volatility.AverageTrueRange(
            df['maxima'], df['minima'], df['fechamento'], window=14
        ).average_true_range()

        # Stochastic Oscillator
        stoch = ta.momentum.StochasticOscillator(df['maxima'], df['minima'], df['fechamento'])
        df['stoch_k'] = stoch.stoch()
        df['stoch_d'] = stoch.stoch_signal()

        # ADX (Average Directional Index) - Força da tendência
        df['adx'] = ta.trend.ADXIndicator(
            df['maxima'], df['minima'], df['fechamento'], window=14
        ).adx()

        logger.info(f"Indicadores técnicos calculados: {len(df)} candles")
        return df

    def detect_candlestick_patterns(self, df):
        """
        Detecta padrões de candlestick

        Args:
            df (pd.DataFrame): DataFrame com dados dos candles

        Returns:
            pd.DataFrame: DataFrame com padrões detectados
        """
        df = df.copy()

        # Calcular corpo e sombra do candle
        df['corpo'] = abs(df['fechamento'] - df['abertura'])
        df['sombra_superior'] = df['maxima'] - df[['abertura', 'fechamento']].max(axis=1)
        df['sombra_inferior'] = df[['abertura', 'fechamento']].min(axis=1) - df['minima']
        df['range_total'] = df['maxima'] - df['minima']

        # Determinar se é candle de alta ou baixa
        df['candle_alta'] = (df['fechamento'] > df['abertura']).astype(int)
        df['candle_baixa'] = (df['fechamento'] < df['abertura']).astype(int)

        # Doji - corpo muito pequeno
        df['doji'] = (df['corpo'] <= df['range_total'] * 0.1).astype(int)

        # Hammer - corpo pequeno, sombra inferior longa
        df['hammer'] = (
            (df['corpo'] <= df['range_total'] * 0.3) &
            (df['sombra_inferior'] >= df['corpo'] * 2) &
            (df['sombra_superior'] <= df['corpo'] * 0.5)
        ).astype(int)

        # Shooting Star - corpo pequeno, sombra superior longa
        df['shooting_star'] = (
            (df['corpo'] <= df['range_total'] * 0.3) &
            (df['sombra_superior'] >= df['corpo'] * 2) &
            (df['sombra_inferior'] <= df['corpo'] * 0.5)
        ).astype(int)

        # Marubozu - corpo grande, sem sombras
        df['marubozu'] = (
            (df['corpo'] >= df['range_total'] * 0.9)
        ).astype(int)

        # Engulfing pattern (precisa de 2 candles)
        df['engulfing_alta'] = 0
        df['engulfing_baixa'] = 0

        for i in range(1, len(df)):
            # Engulfing de alta
            if (df.iloc[i-1]['candle_baixa'] == 1 and
                df.iloc[i]['candle_alta'] == 1 and
                df.iloc[i]['abertura'] <= df.iloc[i-1]['fechamento'] and
                df.iloc[i]['fechamento'] >= df.iloc[i-1]['abertura']):
                df.iloc[i, df.columns.get_loc('engulfing_alta')] = 1

            # Engulfing de baixa
            if (df.iloc[i-1]['candle_alta'] == 1 and
                df.iloc[i]['candle_baixa'] == 1 and
                df.iloc[i]['abertura'] >= df.iloc[i-1]['fechamento'] and
                df.iloc[i]['fechamento'] <= df.iloc[i-1]['abertura']):
                df.iloc[i, df.columns.get_loc('engulfing_baixa')] = 1

        logger.info("Padrões de candlestick detectados")
        return df

    def analyze_trend(self, df):
        """
        Analisa a tendência do mercado

        Args:
            df (pd.DataFrame): DataFrame com indicadores

        Returns:
            pd.DataFrame: DataFrame com análise de tendência
        """
        df = df.copy()

        # Tendência baseada em EMAs
        df['tendencia_ema'] = 0  # 0 = lateral, 1 = alta, -1 = baixa
        df.loc[df['ema_9'] > df['ema_21'], 'tendencia_ema'] = 1
        df.loc[df['ema_9'] < df['ema_21'], 'tendencia_ema'] = -1

        # Força da tendência baseada em ADX
        df['tendencia_forte'] = (df['adx'] > 25).astype(int)

        # Momentum baseado em MACD
        df['momentum_positivo'] = (df['macd'] > df['macd_signal']).astype(int)

        # Condições de sobrecompra/sobrevenda (RSI)
        df['sobrecomprado'] = (df['rsi'] > 70).astype(int)
        df['sobrevendido'] = (df['rsi'] < 30).astype(int)

        # Volatilidade alta
        df['volatilidade_alta'] = (df['bb_width'] > df['bb_width'].rolling(10).mean()).astype(int)

        logger.info("Análise de tendência concluída")
        return df

    def analyze(self, df):
        """
        Executa análise completa

        Args:
            df (pd.DataFrame): DataFrame com dados brutos dos candles

        Returns:
            pd.DataFrame: DataFrame com análise completa
        """
        logger.info("Iniciando análise técnica completa...")

        # Calcular indicadores
        df = self.calculate_indicators(df)

        # Detectar padrões de candlestick
        df = self.detect_candlestick_patterns(df)

        # Analisar tendência
        df = self.analyze_trend(df)

        logger.info("Análise técnica completa finalizada")
        return df


if __name__ == "__main__":
    # Teste do analisador com dados simulados
    data = {
        'time': pd.date_range(start='2024-01-01', periods=50, freq='1min'),
        'abertura': np.random.uniform(1.0850, 1.0950, 50),
        'maxima': np.random.uniform(1.0860, 1.0960, 50),
        'minima': np.random.uniform(1.0840, 1.0940, 50),
        'fechamento': np.random.uniform(1.0850, 1.0950, 50),
        'volume_ticks': np.random.randint(100, 1000, 50),
    }

    df = pd.DataFrame(data)
    df['maxima'] = df[['abertura', 'maxima', 'fechamento']].max(axis=1)
    df['minima'] = df[['abertura', 'minima', 'fechamento']].min(axis=1)

    analyzer = CandleAnalyzer()
    result = analyzer.analyze(df)

    print("\n=== Análise Técnica ===")
    print(result[['time', 'fechamento', 'rsi', 'macd', 'tendencia_ema']].tail(5))
