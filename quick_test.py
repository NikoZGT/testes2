"""
Script de teste rápido - Análise única
Execute este script para fazer uma análise rápida do mercado
"""
import sys
import os
import MetaTrader5 as mt5

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_collector.mt5_collector import MT5DataCollector
from technical_analysis.candle_analyzer import CandleAnalyzer
from technical_analysis.volume_analyzer import VolumeAnalyzer
from signal_generator.signal_generator import SignalGenerator


def quick_analysis(symbol="EURUSD", timeframe=mt5.TIMEFRAME_M5, num_candles=15):
    """
    Faz uma análise rápida do mercado sem ML

    Args:
        symbol (str): Símbolo para análise
        timeframe: Timeframe do MT5
        num_candles (int): Número de candles
    """
    print(f"""
    ╔════════════════════════════════════════════════╗
    ║     Análise Rápida - MetaTrader AI            ║
    ║     Símbolo: {symbol:<30} ║
    ╚════════════════════════════════════════════════╝
    """)

    # Inicializar componentes
    collector = MT5DataCollector()
    candle_analyzer = CandleAnalyzer()
    volume_analyzer = VolumeAnalyzer()
    signal_generator = SignalGenerator()

    # Conectar
    print("Conectando ao MetaTrader 5...")
    if not collector.connect():
        print("❌ Erro ao conectar ao MT5")
        return

    print("✓ Conectado com sucesso!")

    # Coletar dados (pegar mais candles para calcular indicadores)
    print(f"\nColetando {num_candles + 50} candles...")
    df = collector.get_candles(symbol, timeframe, num_candles + 50)

    if df is None or len(df) == 0:
        print("❌ Erro ao coletar dados")
        collector.disconnect()
        return

    print(f"✓ {len(df)} candles coletados!")

    # Análise técnica
    print("\nRealizando análise técnica...")
    df = candle_analyzer.analyze(df)
    print("✓ Análise técnica concluída!")

    # Análise de volume
    print("Realizando análise de volume...")
    df = volume_analyzer.analyze(df)
    print("✓ Análise de volume concluída!")

    # Gerar sinais (sem ML)
    print("Gerando sinais...")
    df = signal_generator.generate_signals(df)
    print("✓ Sinais gerados!")

    # Mostrar últimos candles
    df_display = df.tail(num_candles)

    print("\n" + "="*80)
    print("ÚLTIMOS CANDLES ANALISADOS")
    print("="*80)

    # Mostrar colunas importantes
    display_cols = ['time', 'fechamento', 'volume', 'rsi', 'macd',
                   'volume_spike', 'sinal', 'confianca', 'estrategia']
    available_cols = [col for col in display_cols if col in df_display.columns]

    print(df_display[available_cols].to_string(index=False))

    # Sinal mais recente
    print("\n" + "="*80)
    print("SINAL ATUAL")
    print("="*80)

    signal_data = signal_generator.get_latest_signal(df_display)
    print(signal_generator.format_signal_message(signal_data))

    # Recomendação
    recommendation = signal_generator.get_trading_recommendation(signal_data)
    print(f"\n📊 RECOMENDAÇÃO: {recommendation}\n")

    # Estatísticas
    print("\n" + "="*80)
    print("ESTATÍSTICAS DA ANÁLISE")
    print("="*80)
    print(f"Total de candles analisados: {len(df)}")
    print(f"Sinais de COMPRA: {len(df_display[df_display['sinal'] == 1])}")
    print(f"Sinais de VENDA: {len(df_display[df_display['sinal'] == -1])}")
    print(f"Sinais NEUTROS: {len(df_display[df_display['sinal'] == 0])}")

    # Detectar barras de interesse
    volume_spikes = df_display[df_display['volume_spike'] == 1]
    if len(volume_spikes) > 0:
        print(f"\n⚠️  BARRAS DE INTERESSE detectadas: {len(volume_spikes)}")
        print("    (Entrada massiva de dinheiro no mercado)")

    # Smart money
    smart_money_buy = df_display[df_display['smart_money_compra'] == 1]
    smart_money_sell = df_display[df_display['smart_money_venda'] == 1]

    if len(smart_money_buy) > 0:
        print(f"\n💰 SMART MONEY (Compra) detectado: {len(smart_money_buy)} vezes")

    if len(smart_money_sell) > 0:
        print(f"\n💰 SMART MONEY (Venda) detectado: {len(smart_money_sell)} vezes")

    print("\n" + "="*80)

    # Desconectar
    collector.disconnect()
    print("\n✓ Análise concluída!")


if __name__ == "__main__":
    # Configurações
    SYMBOL = "EURUSD"
    TIMEFRAME = mt5.TIMEFRAME_M5  # 5 minutos
    NUM_CANDLES = 15

    # Executar análise
    quick_analysis(symbol=SYMBOL, timeframe=TIMEFRAME, num_candles=NUM_CANDLES)
