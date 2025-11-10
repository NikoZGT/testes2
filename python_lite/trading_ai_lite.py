"""
Trading AI Lite - Versão simplificada SEM biblioteca MetaTrader5
Lê dados de CSV exportados pelo Expert Advisor
"""
import pandas as pd
import numpy as np
import time
import os
import sys
from datetime import datetime
from pathlib import Path

# Importar módulos da versão completa
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from technical_analysis.candle_analyzer import CandleAnalyzer
from technical_analysis.volume_analyzer import VolumeAnalyzer
from ml_model.trading_model import TradingModel
from signal_generator.signal_generator import SignalGenerator

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TradingAILite:
    """Versão lite que lê dados de CSV (sem MetaTrader5)"""

    def __init__(self, data_folder):
        """
        Args:
            data_folder (str): Pasta onde o EA exporta os dados
        """
        self.data_folder = Path(data_folder)
        self.candles_file = self.data_folder / "candles_data.csv"
        self.signals_file = self.data_folder / "signals.csv"

        # Criar pasta se não existir
        self.data_folder.mkdir(parents=True, exist_ok=True)

        # Inicializar componentes
        self.candle_analyzer = CandleAnalyzer()
        self.volume_analyzer = VolumeAnalyzer()
        self.ml_model = TradingModel()
        self.signal_generator = SignalGenerator()

        logger.info("Trading AI Lite inicializado")
        logger.info(f"Pasta de dados: {self.data_folder}")

    def read_candles_from_csv(self):
        """Lê dados dos candles do CSV exportado pelo EA"""

        if not self.candles_file.exists():
            logger.warning(f"Arquivo não encontrado: {self.candles_file}")
            return None

        try:
            # Ler CSV
            df = pd.read_csv(self.candles_file)

            # Renomear colunas
            df = df.rename(columns={
                'time': 'time',
                'open': 'abertura',
                'high': 'maxima',
                'low': 'minima',
                'close': 'fechamento',
                'tick_volume': 'volume_ticks',
                'real_volume': 'volume_real'
            })

            # Converter time para datetime
            df['time'] = pd.to_datetime(df['time'])

            logger.info(f"✓ Lidos {len(df)} candles do CSV")
            return df

        except Exception as e:
            logger.error(f"Erro ao ler CSV: {e}")
            return None

    def analyze_and_generate_signals(self, df):
        """Faz análise completa e gera sinais"""

        if df is None or len(df) < 15:
            logger.warning("Dados insuficientes para análise")
            return None

        # Análise técnica
        logger.info("Realizando análise técnica...")
        df = self.candle_analyzer.analyze(df)

        # Análise de volume
        logger.info("Analisando volume...")
        df = self.volume_analyzer.analyze(df)

        # ML (se treinado)
        ml_predictions = None
        ml_confidence = None

        if self.ml_model.is_trained:
            logger.info("Aplicando modelo ML...")
            ml_predictions, ml_confidence = self.ml_model.predict(df)

        # Gerar sinais
        logger.info("Gerando sinais...")
        df = self.signal_generator.generate_signals(df, ml_predictions, ml_confidence)

        return df

    def save_signal_to_csv(self, signal_data):
        """Salva sinal no CSV para o EA ler"""

        if signal_data is None:
            return

        try:
            # Preparar dados
            data = {
                'timestamp': [signal_data['timestamp']],
                'sinal': [signal_data['sinal']],
                'confianca': [signal_data['confianca']],
                'estrategia': [signal_data['estrategia']],
                'razao': [signal_data['razao'].replace(',', ';')]  # Remover vírgulas
            }

            df_signal = pd.DataFrame(data)

            # Salvar (append se arquivo existe)
            if self.signals_file.exists():
                df_signal.to_csv(self.signals_file, mode='a', header=False, index=False)
            else:
                df_signal.to_csv(self.signals_file, index=False)

            logger.info(f"✓ Sinal salvo: {signal_data['estrategia']}")

        except Exception as e:
            logger.error(f"Erro ao salvar sinal: {e}")

    def run_continuous(self, interval_seconds=60):
        """Executa análise contínua"""

        logger.info("="*60)
        logger.info("Trading AI Lite - Modo Contínuo")
        logger.info(f"Intervalo: {interval_seconds}s")
        logger.info(f"Aguardando dados do Expert Advisor...")
        logger.info("="*60)

        iteration = 0

        try:
            while True:
                iteration += 1
                logger.info(f"\n{'='*60}")
                logger.info(f"Iteração #{iteration} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                logger.info(f"{'='*60}")

                # Ler dados do CSV
                df = self.read_candles_from_csv()

                if df is not None and len(df) >= 15:
                    # Analisar
                    df_analyzed = self.analyze_and_generate_signals(df)

                    if df_analyzed is not None:
                        # Obter último sinal
                        signal_data = self.signal_generator.get_latest_signal(df_analyzed)

                        # Exibir
                        print(self.signal_generator.format_signal_message(signal_data))
                        print(f"\nRECOMENDAÇÃO: {self.signal_generator.get_trading_recommendation(signal_data)}\n")

                        # Salvar sinal para EA
                        self.save_signal_to_csv(signal_data)

                        # Treinar ML periodicamente
                        if iteration % 20 == 0 and len(df_analyzed) >= 100:
                            logger.info("Re-treinando modelo ML...")
                            self.ml_model.train(df_analyzed)

                else:
                    logger.warning("⚠️  Aguardando dados do Expert Advisor...")
                    logger.warning(f"   Certifique-se que o EA está rodando no MT5")
                    logger.warning(f"   Arquivo esperado: {self.candles_file}")

                # Aguardar
                logger.info(f"Aguardando {interval_seconds} segundos...")
                time.sleep(interval_seconds)

        except KeyboardInterrupt:
            logger.info("\n\nInterrompido pelo usuário")
            self.stop()

    def stop(self):
        """Para o sistema"""
        logger.info("Salvando modelo final...")
        if self.ml_model.is_trained:
            self.ml_model.save_model('trading_model_lite.pkl')
        logger.info("Sistema finalizado!")


def main():
    """Função principal"""

    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║         Trading AI LITE - Versão Simplificada            ║
    ║         SEM necessidade de MetaTrader5 Python            ║
    ║                                                           ║
    ║  Lê dados exportados pelo Expert Advisor                 ║
    ║  Análise completa com Machine Learning                   ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)

    # Encontrar pasta de dados do MT5
    # Padrão: C:\Users\{USER}\AppData\Roaming\MetaQuotes\Terminal\{ID}\MQL5\Files\TradingAI
    terminal_data = os.path.expanduser("~\\AppData\\Roaming\\MetaQuotes\\Terminal")

    # Tentar encontrar pasta automaticamente
    data_folder = None

    if os.path.exists(terminal_data):
        # Procurar em todas as instalações do MT5
        for root, dirs, files in os.walk(terminal_data):
            if "TradingAI" in dirs:
                data_folder = os.path.join(root, "TradingAI")
                break

    # Se não encontrou, usar pasta local como fallback
    if data_folder is None or not os.path.exists(data_folder):
        logger.warning("Pasta do MT5 não encontrada automaticamente")
        data_folder = os.path.join(os.path.dirname(__file__), "data")
        logger.info(f"Usando pasta local: {data_folder}")

    logger.info(f"Pasta de dados: {data_folder}")

    # Criar sistema
    ai = TradingAILite(data_folder)

    # Tentar carregar modelo existente
    models_dir = Path("../models")
    if models_dir.exists():
        models = list(models_dir.glob("*.pkl"))
        if models:
            latest = sorted(models)[-1]
            logger.info(f"Carregando modelo: {latest.name}")
            ai.ml_model.load_model(latest.name)

    # Executar
    print("\n╔═══════════════════════════════════════════════════════════╗")
    print("║  Sistema iniciado!                                        ║")
    print("║                                                           ║")
    print("║  PASSOS:                                                  ║")
    print("║  1. Abra o MetaTrader 5                                   ║")
    print("║  2. Adicione o EA 'TradingAI_DataExporter' ao gráfico    ║")
    print("║  3. Este script vai detectar os dados automaticamente    ║")
    print("║                                                           ║")
    print("║  Pressione Ctrl+C para parar                              ║")
    print("╚═══════════════════════════════════════════════════════════╝\n")

    ai.run_continuous(interval_seconds=60)


if __name__ == "__main__":
    main()
