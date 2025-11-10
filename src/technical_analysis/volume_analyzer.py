"""
Módulo para análise de volume e detecção de barras de interesse
"""
import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VolumeAnalyzer:
    """Analisa volume e detecta barras de interesse (entrada massiva de dinheiro)"""

    def __init__(self, volume_spike_threshold=2.0, large_volume_threshold=1.5):
        """
        Args:
            volume_spike_threshold (float): Multiplicador para detectar picos de volume
            large_volume_threshold (float): Multiplicador para volume grande
        """
        self.volume_spike_threshold = volume_spike_threshold
        self.large_volume_threshold = large_volume_threshold

    def analyze_volume(self, df):
        """
        Analisa volume e detecta barras de interesse

        Args:
            df (pd.DataFrame): DataFrame com dados dos candles

        Returns:
            pd.DataFrame: DataFrame com análise de volume
        """
        df = df.copy()

        # Usar volume_ticks se volume_real não estiver disponível
        volume_col = 'volume_real' if 'volume_real' in df.columns else 'volume_ticks'

        # Garantir que existe a coluna de volume
        if volume_col not in df.columns:
            logger.warning("Coluna de volume não encontrada. Usando volume padrão.")
            df['volume'] = 1000
            volume_col = 'volume'
        else:
            df['volume'] = df[volume_col]

        # Média móvel de volume
        df['volume_ma_10'] = df['volume'].rolling(window=10, min_periods=1).mean()
        df['volume_ma_20'] = df['volume'].rolling(window=20, min_periods=1).mean()

        # Desvio padrão do volume
        df['volume_std'] = df['volume'].rolling(window=10, min_periods=1).std()

        # Detectar picos de volume (barras de interesse)
        df['volume_spike'] = (
            df['volume'] > df['volume_ma_10'] * self.volume_spike_threshold
        ).astype(int)

        # Volume grande (acima da média)
        df['volume_grande'] = (
            df['volume'] > df['volume_ma_20'] * self.large_volume_threshold
        ).astype(int)

        # Volume extremo (muito acima da média)
        df['volume_extremo'] = (
            df['volume'] > df['volume_ma_10'] * (self.volume_spike_threshold * 1.5)
        ).astype(int)

        # Calcular razão volume/média
        df['volume_ratio'] = df['volume'] / (df['volume_ma_10'] + 1e-10)

        # Detectar divergência de volume e preço
        df['preco_subindo'] = (df['fechamento'] > df['fechamento'].shift(1)).astype(int)
        df['volume_subindo'] = (df['volume'] > df['volume'].shift(1)).astype(int)

        # Volume climático (alta ou baixa com volume extremo)
        df['volume_climatico_alta'] = (
            (df['volume_extremo'] == 1) &
            (df['fechamento'] > df['abertura'])
        ).astype(int)

        df['volume_climatico_baixa'] = (
            (df['volume_extremo'] == 1) &
            (df['fechamento'] < df['abertura'])
        ).astype(int)

        logger.info("Análise de volume concluída")
        return df

    def detect_smart_money(self, df):
        """
        Detecta possível entrada de dinheiro institucional (smart money)

        Args:
            df (pd.DataFrame): DataFrame com análise de volume

        Returns:
            pd.DataFrame: DataFrame com detecção de smart money
        """
        df = df.copy()

        # Smart money geralmente entra em correções durante uma tendência
        # Procurar por: volume alto + candle contra-tendência

        df['smart_money_compra'] = 0
        df['smart_money_venda'] = 0

        for i in range(2, len(df)):
            # Compra: tendência de baixa recente + candle de alta com volume alto
            tendencia_baixa = (
                df.iloc[i-2]['fechamento'] > df.iloc[i-1]['fechamento']
            )
            candle_alta = df.iloc[i]['fechamento'] > df.iloc[i]['abertura']
            volume_alto = df.iloc[i]['volume_spike'] == 1

            if tendencia_baixa and candle_alta and volume_alto:
                df.iloc[i, df.columns.get_loc('smart_money_compra')] = 1

            # Venda: tendência de alta recente + candle de baixa com volume alto
            tendencia_alta = (
                df.iloc[i-2]['fechamento'] < df.iloc[i-1]['fechamento']
            )
            candle_baixa = df.iloc[i]['fechamento'] < df.iloc[i]['abertura']

            if tendencia_alta and candle_baixa and volume_alto:
                df.iloc[i, df.columns.get_loc('smart_money_venda')] = 1

        logger.info("Detecção de smart money concluída")
        return df

    def calculate_volume_indicators(self, df):
        """
        Calcula indicadores baseados em volume

        Args:
            df (pd.DataFrame): DataFrame com dados dos candles

        Returns:
            pd.DataFrame: DataFrame com indicadores de volume
        """
        df = df.copy()

        # OBV (On-Balance Volume)
        df['obv'] = 0
        for i in range(1, len(df)):
            if df.iloc[i]['fechamento'] > df.iloc[i-1]['fechamento']:
                df.iloc[i, df.columns.get_loc('obv')] = (
                    df.iloc[i-1]['obv'] + df.iloc[i]['volume']
                )
            elif df.iloc[i]['fechamento'] < df.iloc[i-1]['fechamento']:
                df.iloc[i, df.columns.get_loc('obv')] = (
                    df.iloc[i-1]['obv'] - df.iloc[i]['volume']
                )
            else:
                df.iloc[i, df.columns.get_loc('obv')] = df.iloc[i-1]['obv']

        # Volume Price Trend (VPT)
        df['vpt'] = 0
        for i in range(1, len(df)):
            price_change = (
                (df.iloc[i]['fechamento'] - df.iloc[i-1]['fechamento']) /
                (df.iloc[i-1]['fechamento'] + 1e-10)
            )
            df.iloc[i, df.columns.get_loc('vpt')] = (
                df.iloc[i-1]['vpt'] + df.iloc[i]['volume'] * price_change
            )

        # VWAP aproximado (Volume Weighted Average Price)
        df['vwap'] = (
            (df['fechamento'] * df['volume']).rolling(window=10).sum() /
            df['volume'].rolling(window=10).sum()
        )

        logger.info("Indicadores de volume calculados")
        return df

    def analyze(self, df):
        """
        Executa análise completa de volume

        Args:
            df (pd.DataFrame): DataFrame com dados dos candles

        Returns:
            pd.DataFrame: DataFrame com análise completa de volume
        """
        logger.info("Iniciando análise de volume...")

        # Analisar volume básico
        df = self.analyze_volume(df)

        # Detectar smart money
        df = self.detect_smart_money(df)

        # Calcular indicadores de volume
        df = self.calculate_volume_indicators(df)

        logger.info("Análise de volume completa finalizada")
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

    # Simular alguns picos de volume
    data['volume_ticks'][10] = 5000
    data['volume_ticks'][25] = 4500
    data['volume_ticks'][40] = 6000

    df = pd.DataFrame(data)

    analyzer = VolumeAnalyzer()
    result = analyzer.analyze(df)

    print("\n=== Análise de Volume ===")
    print(result[['time', 'volume', 'volume_spike', 'volume_extremo', 'smart_money_compra']].tail(10))
