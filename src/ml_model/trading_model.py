"""
Módulo de Machine Learning para previsão de sinais de trading
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import logging
import os
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TradingModel:
    """Modelo de ML para prever sinais de compra/venda"""

    def __init__(self, model_dir='models'):
        """
        Args:
            model_dir (str): Diretório para salvar/carregar modelos
        """
        self.model_dir = model_dir
        self.model = None
        self.scaler = StandardScaler()
        self.feature_columns = []
        self.is_trained = False

        # Criar diretório de modelos se não existir
        os.makedirs(model_dir, exist_ok=True)

        # Histórico de predições para aprendizado contínuo
        self.prediction_history = []
        self.feedback_history = []

    def prepare_features(self, df):
        """
        Prepara features para o modelo

        Args:
            df (pd.DataFrame): DataFrame com análise técnica e volume

        Returns:
            pd.DataFrame: Features preparadas
        """
        df = df.copy()

        # Selecionar features importantes
        self.feature_columns = [
            # Indicadores técnicos
            'rsi', 'macd', 'macd_diff', 'bb_width', 'atr',
            'stoch_k', 'stoch_d', 'adx',

            # Padrões de candlestick
            'corpo', 'sombra_superior', 'sombra_inferior',
            'doji', 'hammer', 'shooting_star', 'marubozu',
            'engulfing_alta', 'engulfing_baixa',

            # Tendência
            'tendencia_ema', 'tendencia_forte', 'momentum_positivo',
            'sobrecomprado', 'sobrevendido', 'volatilidade_alta',

            # Volume
            'volume_spike', 'volume_grande', 'volume_extremo',
            'volume_ratio', 'smart_money_compra', 'smart_money_venda',
            'volume_climatico_alta', 'volume_climatico_baixa',
            'obv', 'vpt',

            # Relações de preço
            'candle_alta', 'candle_baixa',
        ]

        # Adicionar features de momentum
        df['momentum_preco'] = df['fechamento'].pct_change(periods=3)
        df['momentum_volume'] = df['volume'].pct_change(periods=3)
        self.feature_columns.extend(['momentum_preco', 'momentum_volume'])

        # Adicionar features de posição relativa
        df['preco_vs_bb_high'] = (df['fechamento'] - df['bb_high']) / df['bb_high']
        df['preco_vs_bb_low'] = (df['fechamento'] - df['bb_low']) / df['bb_low']
        self.feature_columns.extend(['preco_vs_bb_high', 'preco_vs_bb_low'])

        # Remover NaN
        df = df.fillna(0)

        return df

    def create_labels(self, df, lookahead=3, threshold=0.0001):
        """
        Cria labels para treinamento (compra, venda, neutro)

        Args:
            df (pd.DataFrame): DataFrame com dados
            lookahead (int): Quantos candles olhar à frente
            threshold (float): Threshold mínimo de movimento para considerar sinal

        Returns:
            pd.Series: Labels (1=compra, -1=venda, 0=neutro)
        """
        df = df.copy()

        # Calcular retorno futuro
        df['retorno_futuro'] = df['fechamento'].shift(-lookahead) - df['fechamento']
        df['retorno_futuro_pct'] = df['retorno_futuro'] / df['fechamento']

        # Criar labels
        labels = pd.Series(0, index=df.index)
        labels[df['retorno_futuro_pct'] > threshold] = 1  # Compra
        labels[df['retorno_futuro_pct'] < -threshold] = -1  # Venda

        return labels

    def train(self, df, lookahead=3, threshold=0.0001, test_size=0.2):
        """
        Treina o modelo com dados históricos

        Args:
            df (pd.DataFrame): DataFrame com análise completa
            lookahead (int): Quantos candles olhar à frente
            threshold (float): Threshold para labels
            test_size (float): Proporção de dados para teste

        Returns:
            dict: Métricas de treinamento
        """
        logger.info("Preparando dados para treinamento...")

        # Preparar features
        df = self.prepare_features(df)

        # Criar labels
        labels = self.create_labels(df, lookahead, threshold)

        # Remover últimos candles sem labels
        valid_idx = labels.index[:-lookahead]
        X = df.loc[valid_idx, self.feature_columns]
        y = labels.loc[valid_idx]

        # Remover amostras com label neutro para balanceamento
        # (manter apenas sinais claros)
        non_neutral_idx = y != 0
        X = X[non_neutral_idx]
        y = y[non_neutral_idx]

        if len(X) < 10:
            logger.warning("Dados insuficientes para treinamento")
            return {'status': 'insufficient_data'}

        # Split treino/teste
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )

        # Normalizar features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # Treinar modelo (Gradient Boosting para melhor performance)
        logger.info("Treinando modelo de Machine Learning...")
        self.model = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )

        self.model.fit(X_train_scaled, y_train)
        self.is_trained = True

        # Avaliar
        train_score = self.model.score(X_train_scaled, y_train)
        test_score = self.model.score(X_test_scaled, y_test)

        logger.info(f"Treinamento concluído! Train Score: {train_score:.3f}, Test Score: {test_score:.3f}")

        return {
            'status': 'success',
            'train_score': train_score,
            'test_score': test_score,
            'n_samples': len(X),
            'n_features': len(self.feature_columns)
        }

    def predict(self, df):
        """
        Faz previsão para novos dados

        Args:
            df (pd.DataFrame): DataFrame com análise completa

        Returns:
            np.array: Predições (1=compra, -1=venda, 0=neutro)
        """
        if not self.is_trained:
            logger.warning("Modelo não treinado. Execute train() primeiro.")
            return np.zeros(len(df))

        # Preparar features
        df = self.prepare_features(df)

        # Selecionar features
        X = df[self.feature_columns]

        # Normalizar
        X_scaled = self.scaler.transform(X)

        # Prever
        predictions = self.model.predict(X_scaled)

        # Obter probabilidades para confiança
        probabilities = self.model.predict_proba(X_scaled)
        confidence = np.max(probabilities, axis=1)

        # Armazenar para aprendizado contínuo
        self.prediction_history.append({
            'timestamp': datetime.now(),
            'predictions': predictions,
            'confidence': confidence
        })

        return predictions, confidence

    def update_with_feedback(self, df, actual_results):
        """
        Atualiza modelo com feedback dos resultados reais (aprendizado contínuo)

        Args:
            df (pd.DataFrame): DataFrame com features
            actual_results (np.array): Resultados reais (1=acerto compra, -1=acerto venda, 0=erro)

        Returns:
            dict: Status da atualização
        """
        if not self.is_trained:
            logger.warning("Modelo não treinado ainda.")
            return {'status': 'not_trained'}

        # Preparar features
        df = self.prepare_features(df)
        X = df[self.feature_columns]
        X_scaled = self.scaler.transform(X)

        # Treinar incrementalmente
        self.model.fit(X_scaled, actual_results)

        # Armazenar feedback
        self.feedback_history.append({
            'timestamp': datetime.now(),
            'results': actual_results
        })

        logger.info(f"Modelo atualizado com {len(actual_results)} novos resultados")

        return {'status': 'updated', 'n_samples': len(actual_results)}

    def save_model(self, filename=None):
        """
        Salva o modelo treinado

        Args:
            filename (str): Nome do arquivo (opcional)

        Returns:
            str: Caminho do arquivo salvo
        """
        if not self.is_trained:
            logger.warning("Nenhum modelo para salvar")
            return None

        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"trading_model_{timestamp}.pkl"

        filepath = os.path.join(self.model_dir, filename)

        # Salvar modelo, scaler e configurações
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'feature_columns': self.feature_columns,
            'timestamp': datetime.now(),
            'prediction_history': self.prediction_history,
            'feedback_history': self.feedback_history
        }

        joblib.dump(model_data, filepath)
        logger.info(f"Modelo salvo em: {filepath}")

        return filepath

    def load_model(self, filename):
        """
        Carrega modelo salvo

        Args:
            filename (str): Nome do arquivo

        Returns:
            bool: Sucesso ou falha
        """
        filepath = os.path.join(self.model_dir, filename)

        if not os.path.exists(filepath):
            logger.error(f"Arquivo não encontrado: {filepath}")
            return False

        try:
            model_data = joblib.load(filepath)

            self.model = model_data['model']
            self.scaler = model_data['scaler']
            self.feature_columns = model_data['feature_columns']
            self.prediction_history = model_data.get('prediction_history', [])
            self.feedback_history = model_data.get('feedback_history', [])
            self.is_trained = True

            logger.info(f"Modelo carregado de: {filepath}")
            return True

        except Exception as e:
            logger.error(f"Erro ao carregar modelo: {e}")
            return False

    def get_feature_importance(self):
        """
        Retorna importância das features

        Returns:
            pd.DataFrame: Features ordenadas por importância
        """
        if not self.is_trained:
            logger.warning("Modelo não treinado")
            return None

        importance = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)

        return importance


if __name__ == "__main__":
    logger.info("Teste do modelo de ML")
