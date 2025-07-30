# Gerenciador de Tarefas - Bloco Inteligente

Um programa simples e inteligente em Python para organizar suas tarefas diárias com interface interativa.

## 🚀 Como usar

### Executar direto (requer Python):
```
python task_manager.py
```

### Compilar para executável (sem terminal):
```
python build_exe.py
```
ou clique duas vezes em `compilar.bat`

## ✨ Funcionalidades Principais

### 📝 **Entrada Inteligente de Tarefas**
- **Digite uma tarefa** e pressione Enter para adicionar
- **Cole múltiplas linhas** - cada linha vira uma tarefa automaticamente
- **Detecção automática** de listas coladas de outros aplicativos

### 🎯 **Gerenciamento Avançado de Tarefas**
- **Passe o mouse** sobre uma tarefa para ver opções:
  - ✏️ **Editar** o texto da tarefa
  - ↑ **Mover para cima** na lista
  - ↓ **Mover para baixo** na lista  
  - 🗑️ **Excluir** a tarefa
- **Clique no checkbox** para marcar como concluída
- **Separação visual** entre pendentes e concluídas

### 📋 **Exportação em Markdown**
- Botão **"Copiar Lista (Markdown)"** 
- Formato compatível com GitHub, Notion, Obsidian
- Tarefas concluídas: `- [x] tarefa`
- Tarefas pendentes: `- [ ] tarefa`

### 📂 **Múltiplas Listas**
- **Criar novas listas** com o botão "+"
- **Excluir listas** com o botão "-"
- **Lista de Pendentes** - cria nova lista só com tarefas não concluídas
- **Dropdown** para alternar entre listas

### 💾 **Salvamento Automático**
- Todas as alterações são salvas automaticamente
- Dados preservados ao reiniciar o computador
- Arquivo `tasks.json` na mesma pasta do programa

## 🎮 Experiência de Uso

### Interface Interativa:
1. **Digite** uma tarefa e pressione Enter
2. **Cole uma lista** inteira de qualquer lugar
3. **Passe o mouse** sobre tarefas para editá-las
4. **Reorganize** a ordem arrastando com ↑↓
5. **Exporte** em Markdown para documentar

### Exemplo de Uso Múltiplo:
Cole este texto no campo:
```
Comprar leite
- Fazer exercícios  
* Estudar Python
• Ligar para médico
Terminar relatório
```
→ **5 tarefas criadas automaticamente!**

## 🔧 Instalação e Execução

### Opção 1: Python (Terminal)
```bash
python task_manager.py
```

### Opção 2: Executável (Sem Terminal)
1. Execute: `python build_exe.py` ou `compilar.bat`
2. Encontre o arquivo `.exe` na pasta `dist`
3. Execute o `.exe` - funciona sem Python instalado!

## 📋 Requisitos
- **Para Python**: Python 3.x (tkinter incluído)
- **Para Executável**: PyInstaller (instalado automaticamente)

## 💡 Dicas Avançadas

### Reorganização Rápida:
- Use ↑↓ para reordenar tarefas por prioridade
- Tarefas pendentes ficam sempre no topo
- Mantenha sua lista organizada visualmente

### Fluxo de Trabalho:
1. **Cole** uma lista de tarefas do email/documento
2. **Reorganize** por prioridade com ↑↓
3. **Marque** como concluído conforme avança
4. **Crie Lista Pendentes** para renovar periodicamente
5. **Exporte MD** para documentar progresso

### Produtividade:
- Use múltiplas listas para diferentes projetos
- Export para Markdown facilita relatórios
- Interface sem terminal = menos distrações
- Salvamento automático = nunca perca dados

🎊 **Perfeito para organizar tarefas diárias, projetos e listas de qualquer tipo!**
