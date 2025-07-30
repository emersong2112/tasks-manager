"""
Script para compilar o Gerenciador de Tarefas em um executável
Executa: python build_exe.py
"""

import os
import subprocess
import sys

def instalar_pyinstaller():
    """Instala PyInstaller se não estiver instalado"""
    try:
        import PyInstaller
        print("✓ PyInstaller já está instalado")
    except ImportError:
        print("📦 Instalando PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller instalado com sucesso!")

def compilar_executavel():
    """Compila o task_manager.py em um executável"""
    print("🔨 Compilando o Gerenciador de Tarefas...")
    
    # Comando para gerar o executável
    cmd = [
        "pyinstaller",
        "--onefile",                    # Arquivo único
        "--windowed",                   # Sem console (sem terminal)
        "--name=GerenciadorTarefas",    # Nome do executável
        "task_manager.py"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ Compilação concluída com sucesso!")
        print("📁 O executável está em: dist/GerenciadorTarefas.exe")
        print("💡 Você pode copiar o arquivo .exe para qualquer lugar e executar sem Python!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro na compilação: {e}")
    except FileNotFoundError:
        print("❌ PyInstaller não encontrado. Tentando instalar...")
        instalar_pyinstaller()
        print("🔄 Tentando compilar novamente...")
        subprocess.run(cmd, check=True)

if __name__ == "__main__":
    print("🚀 Compilador do Gerenciador de Tarefas")
    print("=" * 50)
    
    # Verificar se o arquivo principal existe
    if not os.path.exists("task_manager.py"):
        print("❌ Arquivo task_manager.py não encontrado!")
        print("💡 Execute este script na mesma pasta do task_manager.py")
        input("Pressione Enter para sair...")
        sys.exit(1)
    
    instalar_pyinstaller()
    compilar_executavel()
    
    print("\n🎉 Processo concluído!")
    print("📋 Instruções:")
    print("   1. O executável está na pasta 'dist'")
    print("   2. Pode executar sem ter Python instalado")
    print("   3. Os dados das tarefas ficam na mesma pasta do .exe")
    
    input("\nPressione Enter para sair...")
