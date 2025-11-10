"""
Script para verificar se todas as dependências estão instaladas
"""
import sys

def check_dependencies():
    """Verifica todas as dependências"""

    print("="*60)
    print("Verificando Dependências - MetaTrader AI")
    print("="*60)
    print()

    # Versão do Python
    print(f"Python: {sys.version}")
    print()

    # Lista de dependências
    dependencies = [
        ('MetaTrader5', 'MetaTrader5'),
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('sklearn', 'scikit-learn'),
        ('joblib', 'joblib'),
        ('ta', 'ta'),
        ('matplotlib', 'matplotlib'),
        ('seaborn', 'seaborn'),
        ('dotenv', 'python-dotenv'),
    ]

    missing = []
    installed = []

    for module_name, package_name in dependencies:
        try:
            __import__(module_name)
            print(f"✓ {package_name:<20} instalado")
            installed.append(package_name)
        except ImportError:
            print(f"✗ {package_name:<20} NÃO instalado")
            missing.append(package_name)

    print()
    print("="*60)

    if missing:
        print("PACOTES FALTANDO:")
        print("="*60)
        print()
        print("Execute o seguinte comando para instalar:")
        print()
        print(f"pip install {' '.join(missing)}")
        print()
        print("Ou instale um por um:")
        for package in missing:
            print(f"  pip install {package}")
        print()
        print("="*60)
        return False
    else:
        print("✓ TUDO INSTALADO COM SUCESSO!")
        print("="*60)
        print()
        print("Próximos passos:")
        print("  1. Abra o MetaTrader 5 e faça login")
        print("  2. Execute: python quick_test.py")
        print()
        return True


if __name__ == "__main__":
    success = check_dependencies()

    if not success:
        sys.exit(1)
