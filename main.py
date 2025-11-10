"""
MetaTrader AI Analysis - Script Principal
Análise inteligente de candles com Machine Learning
"""
import sys
import os
import time
import MetaTrader5 as mt5
from datetime import datetime
import pandas as pd

# Adicionar diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_collector.mt5_collector import MT5DataCollector
from technical_analysis.candle_analyzer import CandleAnalyzer
from technical_analysis.volume_analyzer import VolumeAnalyzer
from ml_model.trading_model import TradingModel
from signal_generator.signal_generator import SignalGenerator

import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/trading_ai.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class TradingAI:
    """Sistema principal de IA para trading"""

    def __init__(self, symbol="EURUSD", timeframe=mt5.TIMEFRAME_M1, num_candles=15):
        """
        Args:
            symbol (str): Símbolo para análise
            timeframe: Timeframe do MT5
            num_candles (int): Número de candles para análise
        """
        self.symbol = symbol
        self.timeframe = timeframe
        self.num_candles = num_candles

        # Inicializar componentes
        self.collector = MT5DataCollector()
        self.candle_analyzer = CandleAnalyzer()
        self.volume_analyzer = VolumeAnalyzer()
        self.ml_model = TradingModel()
        self.signal_generator = SignalGenerator()

        # Estado
        self.is_running = False
        self.historical_data = []
        self.performance_metrics = {
            'total_signals': 0,
            'correct_predictions': 0,
            'incorrect_predictions': 0,
            'accuracy': 0.0
        }

    def initialize(self):
        """Inicializa o sistema"""
        logger.info("="*60)
        logger.info("Inicializando MetaTrader AI Analysis System")
        logger.info("="*60)

        # Conectar ao MT5
        if not self.collector.connect():
            logger.error("Falha ao conectar ao MetaTrader 5")
            return False

        # Tentar carregar modelo existente
        logger.info("Verificando modelos salvos...")
        models = [f for f in os.listdir('models') if f.endswith('.pkl')]

        if models:
            latest_model = sorted(models)[-1]
            logger.info(f"Modelo encontrado: {latest_model}")
            if self.ml_model.load_model(latest_model):
                logger.info("Modelo carregado com sucesso!")
            else:
                logger.warning("Falha ao carregar modelo. Será necessário treinar um novo.")
        else:
            logger.info("Nenhum modelo salvo encontrado. Será treinado um novo modelo.")

        logger.info("Sistema inicializado com sucesso!")
        return True

    def train_initial_model(self, num_candles=500):
        """
        Treina modelo inicial com dados históricos

        Args:
            num_candles (int): Número de candles históricos para treinar
        """
        logger.info(f"Coletando {num_candles} candles históricos para treinamento...")

        # Coletar dados históricos
        df = self.collector.get_candles(self.symbol, self.timeframe, num_candles)

        if df is None or len(df) < 50:
            logger.error("Dados insuficientes para treinamento")
            return False

        # Análise completa
        logger.info("Realizando análise técnica...")
        df = self.candle_analyzer.analyze(df)

        logger.info("Realizando análise de volume...")
        df = self.volume_analyzer.analyze(df)

        # Treinar modelo
        logger.info("Treinando modelo de Machine Learning...")
        metrics = self.ml_model.train(df, lookahead=3, threshold=0.0001)

        if metrics['status'] == 'success':
            logger.info(f"✓ Modelo treinado com sucesso!")
            logger.info(f"  - Acurácia treino: {metrics['train_score']*100:.2f}%")
            logger.info(f"  - Acurácia teste: {metrics['test_score']*100:.2f}%")
            logger.info(f"  - Amostras: {metrics['n_samples']}")
            logger.info(f"  - Features: {metrics['n_features']}")

            # Salvar modelo
            model_path = self.ml_model.save_model()
            logger.info(f"Modelo salvo em: {model_path}")
            return True
        else:
            logger.error("Falha no treinamento do modelo")
            return False

    def analyze_current_market(self):
        """
        Analisa o mercado atual e gera sinais

        Returns:
            dict: Dados da análise e sinal
        """
        # Coletar candles atuais (pegar mais que 15 para calcular indicadores)
        df = self.collector.get_candles(self.symbol, self.timeframe, self.num_candles + 50)

        if df is None or len(df) == 0:
            logger.error("Falha ao coletar dados")
            return None

        # Análise técnica
        df = self.candle_analyzer.analyze(df)

        # Análise de volume
        df = self.volume_analyzer.analyze(df)

        # Predição ML (se modelo está treinado)
        ml_predictions = None
        ml_confidence = None

        if self.ml_model.is_trained:
            ml_predictions, ml_confidence = self.ml_model.predict(df)

        # Gerar sinais
        df = self.signal_generator.generate_signals(df, ml_predictions, ml_confidence)

        # Pegar apenas os últimos N candles para exibição
        df_display = df.tail(self.num_candles)

        # Obter sinal mais recente
        signal_data = self.signal_generator.get_latest_signal(df_display)

        return {
            'dataframe': df_display,
            'signal': signal_data,
            'full_df': df
        }

    def run_continuous(self, interval_seconds=60, auto_save_interval=300):
        """
        Executa análise contínua

        Args:
            interval_seconds (int): Intervalo entre análises
            auto_save_interval (int): Intervalo para salvar modelo automaticamente
        """
        logger.info("="*60)
        logger.info("Iniciando modo de análise contínua")
        logger.info(f"Símbolo: {self.symbol}")
        logger.info(f"Timeframe: {self.timeframe}")
        logger.info(f"Intervalo: {interval_seconds}s")
        logger.info("="*60)

        self.is_running = True
        last_save_time = time.time()
        iteration = 0

        try:
            while self.is_running:
                iteration += 1
                logger.info(f"\n{'='*60}")
                logger.info(f"Iteração #{iteration} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                logger.info(f"{'='*60}")

                # Analisar mercado
                result = self.analyze_current_market()

                if result is not None:
                    signal_data = result['signal']
                    df = result['dataframe']

                    # Exibir sinal
                    print(self.signal_generator.format_signal_message(signal_data))
                    print(f"\nRECOMENDAÇÃO: {self.signal_generator.get_trading_recommendation(signal_data)}\n")

                    # Atualizar métricas
                    if signal_data['sinal'] != 0:
                        self.performance_metrics['total_signals'] += 1

                    # Exibir últimos candles
                    logger.info("\nÚltimos 5 candles:")
                    display_cols = ['time', 'abertura', 'maxima', 'minima', 'fechamento',
                                  'volume', 'rsi', 'sinal', 'estrategia']
                    available_cols = [col for col in display_cols if col in df.columns]
                    print(df[available_cols].tail(5).to_string())

                    # Salvar dados históricos
                    self.historical_data.append({
                        'timestamp': datetime.now(),
                        'signal': signal_data,
                        'dataframe': df.tail(1)
                    })

                    # Manter apenas últimas 100 iterações
                    if len(self.historical_data) > 100:
                        self.historical_data = self.historical_data[-100:]

                    # Aprendizado contínuo (retreinar periodicamente)
                    if iteration % 20 == 0 and self.ml_model.is_trained:
                        logger.info("\n" + "="*60)
                        logger.info("Realizando aprendizado contínuo...")
                        logger.info("="*60)

                        # Coletar mais dados
                        full_df = result['full_df']

                        if len(full_df) >= 100:
                            # Re-treinar com novos dados
                            metrics = self.ml_model.train(full_df, lookahead=3, threshold=0.0001)

                            if metrics['status'] == 'success':
                                logger.info(f"✓ Modelo atualizado!")
                                logger.info(f"  - Nova acurácia: {metrics['test_score']*100:.2f}%")

                # Auto-save modelo
                current_time = time.time()
                if current_time - last_save_time > auto_save_interval and self.ml_model.is_trained:
                    logger.info("Salvando modelo automaticamente...")
                    self.ml_model.save_model()
                    last_save_time = current_time

                # Aguardar próxima iteração
                logger.info(f"\nAguardando {interval_seconds} segundos...")
                time.sleep(interval_seconds)

        except KeyboardInterrupt:
            logger.info("\n\nInterrompido pelo usuário")
            self.stop()

        except Exception as e:
            logger.error(f"Erro durante execução: {e}", exc_info=True)
            self.stop()

    def stop(self):
        """Para o sistema"""
        logger.info("Parando sistema...")
        self.is_running = False

        # Salvar modelo final
        if self.ml_model.is_trained:
            logger.info("Salvando modelo final...")
            self.ml_model.save_model('trading_model_final.pkl')

        # Desconectar MT5
        self.collector.disconnect()

        # Exibir estatísticas finais
        logger.info("\n" + "="*60)
        logger.info("ESTATÍSTICAS DA SESSÃO")
        logger.info("="*60)
        logger.info(f"Total de sinais gerados: {self.performance_metrics['total_signals']}")
        logger.info(f"Total de iterações: {len(self.historical_data)}")
        logger.info("="*60)

        logger.info("Sistema finalizado com sucesso!")


def main():
    """Função principal"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║         MetaTrader AI Analysis System                    ║
    ║         com Machine Learning Adaptativo                  ║
    ║                                                           ║
    ║  Análise inteligente de candles, volume e padrões        ║
    ║  Aprendizado contínuo durante a sessão                   ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)

    # Configurações
    SYMBOL = "EURUSD"  # Altere para o símbolo desejado
    TIMEFRAME = mt5.TIMEFRAME_M1  # M1, M5, M15, M30, H1, H4, D1
    NUM_CANDLES = 15
    INTERVAL_SECONDS = 60  # Análise a cada 60 segundos

    # Criar sistema
    ai = TradingAI(symbol=SYMBOL, timeframe=TIMEFRAME, num_candles=NUM_CANDLES)

    # Inicializar
    if not ai.initialize():
        logger.error("Falha ao inicializar sistema")
        return

    # Verificar se precisa treinar modelo
    if not ai.ml_model.is_trained:
        print("\n╔═══════════════════════════════════════════════════════════╗")
        print("║  Nenhum modelo treinado encontrado                        ║")
        print("║  Iniciando treinamento com dados históricos...           ║")
        print("╚═══════════════════════════════════════════════════════════╝\n")

        if not ai.train_initial_model(num_candles=500):
            logger.error("Falha ao treinar modelo inicial")
            return

    # Executar análise contínua
    print("\n╔═══════════════════════════════════════════════════════════╗")
    print("║  Sistema iniciado!                                        ║")
    print("║  Pressione Ctrl+C para parar                              ║")
    print("╚═══════════════════════════════════════════════════════════╝\n")

    ai.run_continuous(interval_seconds=INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
