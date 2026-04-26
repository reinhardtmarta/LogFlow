# main.py
from logiflow.engine import LogiflowEngine
from logiflow.ui import LogiflowUI
import sys

def main():
    print("🚀 Initializing Logiflow System...")
    engine = LogiflowEngine()

    # Verifica se está rodando em um ambiente interativo (Jupyter/Kaggle)
    if 'ipykernel' in sys.modules:
        print("🌐 Interactive Mode Detected. Launching Dashboard...")
        ui = LogiflowUI(engine)
        ui.render()
    else:
        print("💻 CLI Mode Detected. Running Automated Simulation...")
        # Aqui você chama a função de simulação que criamos para o modo headless
        # engine.run_automated_simulation() 

if __name__ == "__main__":
    main()
