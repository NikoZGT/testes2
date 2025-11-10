"""
Módulo para geração de sinais de trading
"""
import pandas as pd
import numpy as np
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SignalGenerator:
    """Gera sinais de compra/venda baseado em análises e ML"""

    def __init__(self):
        self.signals_history = []

    def generate_signals(self, df, ml_predictions=None, ml_confidence=None):
        """
        Gera sinais de trading baseado em múltiplas análises

        Args:
            df (pd.DataFrame): DataFrame com análise técnica e volume completa
            ml_predictions (np.array): Predições do modelo ML
            ml_confidence (np.array): Confiança das predições

        Returns:
            pd.DataFrame: DataFrame com sinais e estratégias
        """
        df = df.copy()

        # Inicializar colunas de sinal
        df['sinal'] = 0  # 0=neutro, 1=compra, -1=venda
        df['confianca'] = 0.0
        df['estrategia'] = 'NEUTRO'
        df['razao'] = ''

        # Processar cada candle
        for i in range(len(df)):
            signal_data = self._analyze_signal(df.iloc[i], i, df, ml_predictions, ml_confidence)

            df.iloc[i, df.columns.get_loc('sinal')] = signal_data['sinal']
            df.iloc[i, df.columns.get_loc('confianca')] = signal_data['confianca']
            df.iloc[i, df.columns.get_loc('estrategia')] = signal_data['estrategia']
            df.iloc[i, df.columns.get_loc('razao')] = signal_data['razao']

        logger.info("Sinais gerados com sucesso")
        return df

    def _analyze_signal(self, row, idx, full_df, ml_predictions, ml_confidence):
        """
        Analisa um único candle e gera sinal

        Args:
            row: Linha do DataFrame
            idx: Índice da linha
            full_df: DataFrame completo
            ml_predictions: Predições ML
            ml_confidence: Confiança ML

        Returns:
            dict: Dados do sinal
        """
        sinais_compra = []
        sinais_venda = []
        confiancas = []
        razoes = []

        # === ESTRATÉGIA 1: Reversão de Tendência com Volume ===
        if row['sobrevendido'] == 1 and row['volume_spike'] == 1 and row['candle_alta'] == 1:
            sinais_compra.append(1)
            confiancas.append(0.8)
            razoes.append("REVERSÃO ALTA: Sobrevendido + Volume Alto + Candle de Alta")

        if row['sobrecomprado'] == 1 and row['volume_spike'] == 1 and row['candle_baixa'] == 1:
            sinais_venda.append(1)
            confiancas.append(0.8)
            razoes.append("REVERSÃO BAIXA: Sobrecomprado + Volume Alto + Candle de Baixa")

        # === ESTRATÉGIA 2: Confirmação de Tendência ===
        if (row['tendencia_ema'] == 1 and row['tendencia_forte'] == 1 and
            row['momentum_positivo'] == 1 and row['candle_alta'] == 1):
            sinais_compra.append(1)
            confiancas.append(0.75)
            razoes.append("TENDÊNCIA ALTA: Confirmação de Tendência de Alta Forte")

        if (row['tendencia_ema'] == -1 and row['tendencia_forte'] == 1 and
            row['momentum_positivo'] == 0 and row['candle_baixa'] == 1):
            sinais_venda.append(1)
            confiancas.append(0.75)
            razoes.append("TENDÊNCIA BAIXA: Confirmação de Tendência de Baixa Forte")

        # === ESTRATÉGIA 3: Smart Money ===
        if row['smart_money_compra'] == 1:
            sinais_compra.append(1)
            confiancas.append(0.85)
            razoes.append("SMART MONEY: Entrada de Dinheiro Institucional - COMPRA")

        if row['smart_money_venda'] == 1:
            sinais_venda.append(1)
            confiancas.append(0.85)
            razoes.append("SMART MONEY: Saída de Dinheiro Institucional - VENDA")

        # === ESTRATÉGIA 4: Padrões de Candlestick ===
        if row['engulfing_alta'] == 1 and row['volume_grande'] == 1:
            sinais_compra.append(1)
            confiancas.append(0.7)
            razoes.append("PADRÃO ALTA: Engulfing de Alta com Volume")

        if row['engulfing_baixa'] == 1 and row['volume_grande'] == 1:
            sinais_venda.append(1)
            confiancas.append(0.7)
            razoes.append("PADRÃO BAIXA: Engulfing de Baixa com Volume")

        if row['hammer'] == 1 and row['sobrevendido'] == 1:
            sinais_compra.append(1)
            confiancas.append(0.65)
            razoes.append("PADRÃO ALTA: Hammer em Zona de Sobrevenda")

        if row['shooting_star'] == 1 and row['sobrecomprado'] == 1:
            sinais_venda.append(1)
            confiancas.append(0.65)
            razoes.append("PADRÃO BAIXA: Shooting Star em Zona de Sobrecompra")

        # === ESTRATÉGIA 5: Bollinger Bands ===
        if row['preco_vs_bb_low'] < -0.001 and row['rsi'] < 35:
            sinais_compra.append(1)
            confiancas.append(0.6)
            razoes.append("BOLLINGER: Preço abaixo da banda inferior + RSI baixo")

        if row['preco_vs_bb_high'] > 0.001 and row['rsi'] > 65:
            sinais_venda.append(1)
            confiancas.append(0.6)
            razoes.append("BOLLINGER: Preço acima da banda superior + RSI alto")

        # === ESTRATÉGIA 6: Volume Climático ===
        if row['volume_climatico_alta'] == 1 and row['tendencia_ema'] == -1:
            sinais_compra.append(1)
            confiancas.append(0.75)
            razoes.append("VOLUME CLIMÁTICO: Exaustão de Venda - Reversão para Alta")

        if row['volume_climatico_baixa'] == 1 and row['tendencia_ema'] == 1:
            sinais_venda.append(1)
            confiancas.append(0.75)
            razoes.append("VOLUME CLIMÁTICO: Exaustão de Compra - Reversão para Baixa")

        # === ESTRATÉGIA 7: Machine Learning ===
        if ml_predictions is not None and idx < len(ml_predictions):
            ml_signal = ml_predictions[idx]
            ml_conf = ml_confidence[idx] if ml_confidence is not None else 0.5

            if ml_signal == 1 and ml_conf > 0.6:
                sinais_compra.append(1)
                confiancas.append(ml_conf)
                razoes.append(f"ML PREDICTION: Compra com {ml_conf*100:.1f}% confiança")

            elif ml_signal == -1 and ml_conf > 0.6:
                sinais_venda.append(1)
                confiancas.append(ml_conf)
                razoes.append(f"ML PREDICTION: Venda com {ml_conf*100:.1f}% confiança")

        # === CONSOLIDAR SINAIS ===
        sinal_final = 0
        confianca_final = 0.0
        estrategia_final = "NEUTRO"
        razao_final = "Sem sinal claro"

        # Compra: se há mais sinais de compra
        if len(sinais_compra) > len(sinais_venda) and len(sinais_compra) > 0:
            sinal_final = 1
            confianca_final = np.mean(confiancas[:len(sinais_compra)])
            estrategia_final = "COMPRA (ALTA)"
            razao_final = " | ".join(razoes[:len(sinais_compra)])

        # Venda: se há mais sinais de venda
        elif len(sinais_venda) > len(sinais_compra) and len(sinais_venda) > 0:
            sinal_final = -1
            confianca_final = np.mean(confiancas[len(sinais_compra):])
            estrategia_final = "VENDA (BAIXA)"
            razao_final = " | ".join(razoes[len(sinais_compra):])

        # Conflito: sinais mistos
        elif len(sinais_compra) > 0 and len(sinais_venda) > 0:
            sinal_final = 0
            confianca_final = 0.3
            estrategia_final = "CONFLITO"
            razao_final = "Sinais mistos - aguardar confirmação"

        return {
            'sinal': sinal_final,
            'confianca': confianca_final,
            'estrategia': estrategia_final,
            'razao': razao_final
        }

    def get_latest_signal(self, df):
        """
        Obtém o sinal mais recente

        Args:
            df (pd.DataFrame): DataFrame com sinais

        Returns:
            dict: Dados do último sinal
        """
        if len(df) == 0:
            return None

        last_row = df.iloc[-1]

        signal_data = {
            'timestamp': last_row['time'],
            'preco': last_row['fechamento'],
            'sinal': last_row['sinal'],
            'confianca': last_row['confianca'],
            'estrategia': last_row['estrategia'],
            'razao': last_row['razao'],
            'volume': last_row['volume'],
            'rsi': last_row['rsi'],
            'macd': last_row['macd']
        }

        return signal_data

    def format_signal_message(self, signal_data):
        """
        Formata mensagem do sinal para exibição

        Args:
            signal_data (dict): Dados do sinal

        Returns:
            str: Mensagem formatada
        """
        if signal_data is None:
            return "Nenhum sinal disponível"

        seta = "🟢 ⬆️" if signal_data['sinal'] == 1 else "🔴 ⬇️" if signal_data['sinal'] == -1 else "⚪ ➡️"

        message = f"""
╔═══════════════════════════════════════════════╗
║        SINAL DE TRADING - MetaTrader AI      ║
╠═══════════════════════════════════════════════╣
║ {seta} {signal_data['estrategia']}
║
║ Timestamp: {signal_data['timestamp']}
║ Preço Atual: {signal_data['preco']:.5f}
║ Confiança: {signal_data['confianca']*100:.1f}%
║
║ Volume: {signal_data['volume']}
║ RSI: {signal_data['rsi']:.2f}
║ MACD: {signal_data['macd']:.5f}
║
║ RAZÃO:
║ {signal_data['razao']}
╚═══════════════════════════════════════════════╝
"""
        return message

    def get_trading_recommendation(self, signal_data):
        """
        Retorna recomendação de trading baseada no sinal

        Args:
            signal_data (dict): Dados do sinal

        Returns:
            str: Recomendação
        """
        if signal_data is None or signal_data['sinal'] == 0:
            return "AGUARDAR - Sem sinal claro no momento"

        if signal_data['sinal'] == 1:
            if signal_data['confianca'] > 0.75:
                return "COMPRA FORTE - Entre com posição maior"
            elif signal_data['confianca'] > 0.6:
                return "COMPRA MODERADA - Entre com posição padrão"
            else:
                return "COMPRA FRACA - Entre com posição reduzida ou aguarde"

        if signal_data['sinal'] == -1:
            if signal_data['confianca'] > 0.75:
                return "VENDA FORTE - Entre com posição maior"
            elif signal_data['confianca'] > 0.6:
                return "VENDA MODERADA - Entre com posição padrão"
            else:
                return "VENDA FRACA - Entre com posição reduzida ou aguarde"


if __name__ == "__main__":
    logger.info("Teste do gerador de sinais")
