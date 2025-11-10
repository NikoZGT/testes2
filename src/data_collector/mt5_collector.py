"""
Módulo para coletar dados do MetaTrader 5
"""
import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MT5DataCollector:
    """Coleta dados de candles do MetaTrader 5"""

    def __init__(self):
        self.connected = False

    def connect(self):
        """Conecta ao MetaTrader 5"""
        if not mt5.initialize():
            logger.error(f"Falha ao inicializar MT5: {mt5.last_error()}")
            return False

        self.connected = True
        logger.info("Conectado ao MetaTrader 5 com sucesso!")
        logger.info(f"Versão MT5: {mt5.version()}")
        return True

    def disconnect(self):
        """Desconecta do MetaTrader 5"""
        mt5.shutdown()
        self.connected = False
        logger.info("Desconectado do MetaTrader 5")

    def get_candles(self, symbol="EURUSD", timeframe=mt5.TIMEFRAME_M1, num_candles=15):
        """
        Coleta os últimos N candles do símbolo especificado

        Args:
            symbol (str): Símbolo do ativo (ex: EURUSD, BTCUSD)
            timeframe: Timeframe do MT5 (ex: TIMEFRAME_M1, TIMEFRAME_M5)
            num_candles (int): Número de candles para coletar

        Returns:
            pd.DataFrame: DataFrame com dados dos candles
        """
        if not self.connected:
            logger.error("Não conectado ao MT5. Execute connect() primeiro.")
            return None

        # Obter dados dos candles
        rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_candles)

        if rates is None or len(rates) == 0:
            logger.error(f"Erro ao obter candles: {mt5.last_error()}")
            return None

        # Converter para DataFrame
        df = pd.DataFrame(rates)

        # Converter timestamp para datetime
        df['time'] = pd.to_datetime(df['time'], unit='s')

        # Renomear colunas para português
        df = df.rename(columns={
            'open': 'abertura',
            'high': 'maxima',
            'low': 'minima',
            'close': 'fechamento',
            'tick_volume': 'volume_ticks',
            'real_volume': 'volume_real'
        })

        logger.info(f"Coletados {len(df)} candles de {symbol}")
        return df

    def get_tick_data(self, symbol="EURUSD", num_ticks=100):
        """
        Coleta dados de ticks para análise mais detalhada

        Args:
            symbol (str): Símbolo do ativo
            num_ticks (int): Número de ticks para coletar

        Returns:
            pd.DataFrame: DataFrame com dados dos ticks
        """
        if not self.connected:
            logger.error("Não conectado ao MT5. Execute connect() primeiro.")
            return None

        # Obter ticks
        ticks = mt5.copy_ticks_from_pos(symbol, 0, num_ticks, mt5.COPY_TICKS_ALL)

        if ticks is None or len(ticks) == 0:
            logger.error(f"Erro ao obter ticks: {mt5.last_error()}")
            return None

        # Converter para DataFrame
        df = pd.DataFrame(ticks)
        df['time'] = pd.to_datetime(df['time'], unit='s')

        return df

    def get_symbol_info(self, symbol="EURUSD"):
        """
        Obtém informações sobre o símbolo

        Args:
            symbol (str): Símbolo do ativo

        Returns:
            dict: Informações do símbolo
        """
        if not self.connected:
            logger.error("Não conectado ao MT5. Execute connect() primeiro.")
            return None

        info = mt5.symbol_info(symbol)

        if info is None:
            logger.error(f"Erro ao obter informações de {symbol}")
            return None

        return {
            'nome': info.name,
            'descricao': info.description,
            'ponto': info.point,
            'digitos': info.digits,
            'spread': info.spread,
            'volume_min': info.volume_min,
            'volume_max': info.volume_max,
        }


if __name__ == "__main__":
    # Teste do coletor
    collector = MT5DataCollector()

    if collector.connect():
        # Testar coleta de candles
        df = collector.get_candles("EURUSD", mt5.TIMEFRAME_M1, 15)
        if df is not None:
            print("\n=== Últimos 15 Candles ===")
            print(df)

        # Testar informações do símbolo
        info = collector.get_symbol_info("EURUSD")
        if info:
            print("\n=== Informações do Símbolo ===")
            for key, value in info.items():
                print(f"{key}: {value}")

        collector.disconnect()
