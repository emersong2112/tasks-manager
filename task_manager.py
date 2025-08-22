import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import json
from pathlib import Path

# --- FONTES E CORES MODERNAS ---
# Paleta de cores moderna e elegante
COR_FUNDO = "#f8fafc"          # Fundo principal - cinza muito claro
COR_JANELA = "#ffffff"         # Fundo dos painéis - branco puro  
COR_HOVER = "#e2e8f0"          # Hover suave - cinza azulado claro
COR_BORDER = "#e2e8f0"         # Bordas sutis
COR_ACCENT = "#3b82f6"         # Azul moderno para destaque
COR_SUCCESS = "#10b981"        # Verde para concluídas
COR_TEXT = "#1e293b"           # Texto principal - cinza escuro
COR_TEXT_LIGHT = "#64748b"     # Texto secundário
COR_SHADOW = "#f1f5f9"         # Sombra sutil
COR_COMPLETED_BG = "#f0fdf4"   # Fundo suave para tarefas concluídas

# Tipografia moderna com hierarquia
FONT_TITLE = ("Segoe UI", 16, "bold")      # Título principal
FONT_SUBTITLE = ("Segoe UI", 11, "bold")   # Subtítulos
FONT_NORMAL = ("Segoe UI", 11)             # Texto normal
FONT_RISCADO = ("Segoe UI", 11, "overstrike")  # Tarefas concluídas
FONT_SMALL = ("Segoe UI", 9)               # Texto pequeno

class TaskFrame(tk.Frame):
    """Um Frame que representa uma única tarefa, com seus botões de ação."""
    def __init__(self, parent, task_data, task_index, app):
        super().__init__(parent, bg=COR_JANELA, relief="flat", bd=0)
        self.task_data = task_data
        self.task_index = task_index
        self.app = app

        # Container principal com padding elegante
        self.main_container = tk.Frame(self, bg=COR_JANELA, relief="flat", bd=0)
        self.main_container.pack(fill='x', padx=8, pady=3)

        self.var_concluida = tk.BooleanVar(value=task_data['concluida'])
        
        # Checkbutton estilizado
        self.checkbutton = tk.Checkbutton(
            self.main_container, 
            text=task_data['texto'], 
            variable=self.var_concluida,
            bg=COR_JANELA, 
            fg=COR_TEXT,
            anchor='w', 
            command=self.alternar_tarefa,
            relief="flat",
            bd=0,
            highlightthickness=0,
            activebackground=COR_HOVER,
            selectcolor=COR_ACCENT
        )
        self.atualizar_estilo_checkbutton()
        
        # Entry para edição com estilo moderno
        style = ttk.Style()
        style.configure("Modern.TEntry", 
                       fieldbackground=COR_JANELA,
                       borderwidth=1,
                       relief="solid")
        self.entry_edicao = ttk.Entry(self.main_container, font=FONT_NORMAL, style="Modern.TEntry")
        
        # Frame de ações com estilo moderno
        self.action_frame = tk.Frame(self.main_container, bg=COR_JANELA)
        
        # Botões com ícones mais modernos e estilizados
        btn_edit = ttk.Button(self.action_frame, text="✏️", width=3, command=self.iniciar_edicao)
        btn_edit.pack(side='left', padx=1)
        btn_delete = ttk.Button(self.action_frame, text="🗑️", width=3, command=self.excluir_tarefa)
        btn_delete.pack(side='left', padx=1)
        btn_up = ttk.Button(self.action_frame, text="↑", width=3, command=lambda: self.app.mover_tarefa(self.task_index, -1))
        if task_index > 0: btn_up.pack(side='left', padx=1)
        btn_down = ttk.Button(self.action_frame, text="↓", width=3, command=lambda: self.app.mover_tarefa(self.task_index, 1))
        total_tasks = len(self.app.dados[self.app.lista_atual.get()])
        if task_index < total_tasks - 1: btn_down.pack(side='left', padx=1)

        self.checkbutton.pack(side='left', fill='x', expand=True, padx=(8, 5), pady=8)
        
        # Adicionar linha separadora sutil
        self.separator = tk.Frame(self, height=1, bg=COR_BORDER)
        self.separator.pack(fill='x', padx=16)
        
        # Eventos de hover
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.main_container.bind("<Enter>", self.on_enter)
        self.main_container.bind("<Leave>", self.on_leave)
        self.checkbutton.bind("<Enter>", self.on_enter)
        self.checkbutton.bind("<Leave>", self.on_leave)
        self.action_frame.bind("<Enter>", self.on_enter)
        self.action_frame.bind("<Leave>", self.on_leave)

    def on_enter(self, event=None):
        if not self.entry_edicao.winfo_viewable():
            # Efeito hover mais suave e moderno
            hover_color = COR_HOVER if not self.task_data['concluida'] else "#dcfce7"
            self.configure(bg=hover_color)
            self.main_container.configure(bg=hover_color)
            self.checkbutton.configure(bg=hover_color, activebackground=hover_color)
            self.action_frame.configure(bg=hover_color)
            self.action_frame.pack(side='right', padx=(5, 8))

    def on_leave(self, event=None):
        if not self.winfo_containing(event.x_root, event.y_root) in self.action_frame.winfo_children():
            # Restaurar cor original baseada no status
            bg_color = COR_COMPLETED_BG if self.task_data['concluida'] else COR_JANELA
            self.configure(bg=bg_color)
            self.main_container.configure(bg=bg_color)
            self.checkbutton.configure(bg=bg_color, activebackground=COR_HOVER)
            self.action_frame.configure(bg=bg_color)
            self.action_frame.pack_forget()

    def alternar_tarefa(self):
        self.task_data['concluida'] = self.var_concluida.get()
        self.atualizar_estilo_checkbutton()
        self.app.salvar_e_repopular()

    def atualizar_estilo_checkbutton(self):
        if self.task_data['concluida']:
            font = FONT_RISCADO
            color = COR_SUCCESS
            bg_color = COR_COMPLETED_BG
        else:
            font = FONT_NORMAL
            color = COR_TEXT
            bg_color = COR_JANELA
            
        self.checkbutton.config(font=font, fg=color)
        # Atualizar cores de fundo para indicar status
        self.configure(bg=bg_color)
        self.main_container.configure(bg=bg_color)
        if not self.winfo_containing(self.winfo_rootx(), self.winfo_rooty()) == self:
            self.checkbutton.configure(bg=bg_color, activebackground=COR_HOVER)
        
    def excluir_tarefa(self): self.app.excluir_tarefa_pelo_indice(self.task_index)
    
    def iniciar_edicao(self):
        self.checkbutton.pack_forget()
        self.action_frame.pack_forget()
        self.entry_edicao.pack(side='left', fill='x', expand=True, padx=(8, 5), pady=4)
        self.entry_edicao.insert(0, self.task_data['texto'])
        self.entry_edicao.focus()
        self.entry_edicao.bind("<Return>", self.salvar_edicao)
        self.entry_edicao.bind("<FocusOut>", self.salvar_edicao)

    def salvar_edicao(self, event=None):
        novo_texto = self.entry_edicao.get().strip()
        if novo_texto: self.app.atualizar_texto_tarefa(self.task_index, novo_texto)
        
class ToDoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("✨ Gerenciador de Tarefas")
        self.full_geometry = "520x600"
        self.geometry(self.full_geometry)
        self.configure(bg=COR_FUNDO)
        self.resizable(True, True)
        
        # Configurar estilo moderno
        self.configure_modern_styles()
        
        self.data_file = Path("tasks.json")
        self.dados = self.carregar_dados()
        self.lista_atual = tk.StringVar()
        self.in_focus_mode = False
        self.criar_widgets()
        self.popular_listas_dropdown()
        self.protocol("WM_DELETE_WINDOW", self.ao_fechar)

    def configure_modern_styles(self):
        """Configura estilos modernos para os widgets ttk"""
        style = ttk.Style()
        
        # Estilo moderno para botões principais
        style.configure("Modern.TButton",
                       padding=(12, 8),
                       font=FONT_NORMAL,
                       borderwidth=1,
                       relief="solid")
        
        # Estilo moderno para combobox
        style.configure("Modern.TCombobox",
                       fieldbackground=COR_JANELA,
                       borderwidth=1,
                       font=FONT_NORMAL,
                       relief="solid")
        
        # Estilo para botões pequenos de ação
        style.configure("Action.TButton",
                       padding=(8, 6),
                       font=FONT_SMALL,
                       borderwidth=1,
                       relief="solid")
        
        # Mapas de estado para efeitos hover
        style.map("Modern.TButton",
                 background=[('active', COR_HOVER),
                            ('pressed', COR_ACCENT)])
        
        style.map("Action.TButton",
                 background=[('active', COR_HOVER),
                            ('pressed', COR_ACCENT)])

    def criar_widgets(self):
        # Header moderno com melhor visual hierarchy
        header_frame = tk.Frame(self, bg=COR_FUNDO, relief="flat", bd=0)
        header_frame.pack(fill='x', padx=20, pady=(15, 5))
        
        # Título principal com fonte maior e moderna
        self.app_title_label = tk.Label(
            header_frame, 
            text="✨ Gerenciador de Tarefas", 
            bg=COR_FUNDO, 
            fg=COR_TEXT,
            font=FONT_TITLE
        )
        self.app_title_label.pack(side='left')
        
        # Botão modo foco com estilo moderno
        self.focus_button = ttk.Button(
            header_frame, 
            text="🔍 Modo Foco", 
            command=self.toggle_focus_mode,
            style="Modern.TButton"
        )
        self.focus_button.pack(side='right')

        # Frame de listas com visual moderno
        self.frame_listas = tk.Frame(self, bg=COR_FUNDO, relief="flat", bd=0)
        self.frame_listas.pack(fill='x', padx=20, pady=(10, 15))
        
        # Label com estilo moderno
        lista_label = tk.Label(
            self.frame_listas, 
            text="📋 Lista:", 
            bg=COR_FUNDO, 
            fg=COR_TEXT,
            font=FONT_SUBTITLE
        )
        lista_label.pack(side='left', padx=(0, 8))
        
        # Dropdown com estilo moderno
        self.dropdown_listas = ttk.Combobox(
            self.frame_listas, 
            textvariable=self.lista_atual, 
            state="readonly", 
            width=25,
            style="Modern.TCombobox"
        )
        self.dropdown_listas.pack(side='left', fill='x', expand=True, padx=(0, 10))
        self.dropdown_listas.bind("<<ComboboxSelected>>", lambda e: self.popular_tarefas())
        
        # Botões de lista com melhor espaçamento
        btn_nova_lista = ttk.Button(
            self.frame_listas, 
            text="➕", 
            width=4, 
            command=self.criar_nova_lista,
            style="Action.TButton"
        )
        btn_nova_lista.pack(side='left', padx=(0, 5))
        
        btn_excluir_lista = ttk.Button(
            self.frame_listas, 
            text="➖", 
            width=4, 
            command=self.excluir_lista_atual,
            style="Action.TButton"
        )
        btn_excluir_lista.pack(side='left')

        # Container principal das tarefas com visual moderno
        self.canvas_frame = tk.Frame(
            self, 
            bg=COR_JANELA, 
            relief="solid", 
            borderwidth=1,
            highlightbackground=COR_BORDER,
            highlightthickness=1
        )
        self.canvas_frame.pack(fill='both', expand=True, padx=20, pady=(0, 15))
        
        # Canvas com scroll personalizado
        canvas = tk.Canvas(
            self.canvas_frame, 
            bg=COR_JANELA, 
            highlightthickness=0,
            relief="flat",
            bd=0
        )
        
        # Scrollbar com estilo moderno
        scrollbar = ttk.Scrollbar(self.canvas_frame, orient="vertical", command=canvas.yview)
        
        # Frame de tarefas
        self.frame_tarefas = tk.Frame(canvas, bg=COR_JANELA, relief="flat", bd=0)
        self.frame_tarefas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.frame_tarefas, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Eventos de scroll
        self.frame_tarefas.bind('<MouseWheel>', lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        canvas.bind('<MouseWheel>', lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        # Frame de adicionar tarefa com visual moderno
        self.frame_adicionar = tk.Frame(self, bg=COR_FUNDO, relief="flat", bd=0)
        self.frame_adicionar.pack(fill='x', padx=20, pady=(0, 10))
        
        # Text widget com bordas modernas
        self.entry_inteligente = tk.Text(
            self.frame_adicionar, 
            height=2, 
            font=FONT_NORMAL, 
            relief="solid", 
            borderwidth=1,
            bg=COR_JANELA,
            fg=COR_TEXT,
            insertbackground=COR_ACCENT,
            highlightbackground=COR_BORDER,
            highlightcolor=COR_ACCENT,
            highlightthickness=1
        )
        self.entry_inteligente.pack(side='left', fill='x', expand=True, padx=(0, 10), ipady=6)
        self.entry_inteligente.bind("<Return>", self.adicionar_tarefa_inteligente)
        
        # Botão adicionar com estilo moderno
        btn_adicionar = ttk.Button(
            self.frame_adicionar, 
            text="➕ Adicionar", 
            command=self.adicionar_tarefa_inteligente,
            style="Modern.TButton"
        )
        btn_adicionar.pack(side='left')

        # Frame de opções com visual moderno
        self.frame_opcoes = tk.Frame(self, bg=COR_FUNDO, relief="flat", bd=0)
        self.frame_opcoes.pack(fill='x', padx=20, pady=(0, 20))
        
        # Botões de opção com melhor estilo
        btn_copiar_md = ttk.Button(
            self.frame_opcoes, 
            text="📋 Exportar MD", 
            command=self.copiar_para_clipboard,
            style="Modern.TButton"
        )
        btn_copiar_md.pack(fill='x', side='left', expand=True, padx=(0, 10))
        
        btn_pendentes = ttk.Button(
            self.frame_opcoes, 
            text="📝 Lista Pendentes", 
            command=self.criar_lista_de_pendentes,
            style="Modern.TButton"
        )
        btn_pendentes.pack(fill='x', side='left', expand=True)

    def toggle_focus_mode(self):
        self.in_focus_mode = not self.in_focus_mode
        if self.in_focus_mode:
            self.frame_listas.pack_forget()
            self.frame_adicionar.pack_forget()
            self.frame_opcoes.pack_forget()
            self.focus_button.config(text="↔️ Expandir")
            # ATUALIZAÇÃO: Mostra o nome da lista atual no modo foco
            self.app_title_label.config(text=f"🔍 {self.lista_atual.get()}")
            self.geometry("380x450")
        else:
            self.frame_listas.pack(fill='x', padx=20, pady=(10, 15), before=self.canvas_frame)
            self.frame_adicionar.pack(fill='x', padx=20, pady=(0, 10))
            self.frame_opcoes.pack(fill='x', padx=20, pady=(0, 20))
            self.focus_button.config(text="🔍 Modo Foco")
            self.app_title_label.config(text="✨ Gerenciador de Tarefas")
            self.geometry(self.full_geometry)

    def salvar_e_repopular(self):
        self.salvar_dados()
        self.popular_tarefas()
    def popular_tarefas(self):
        for widget in self.frame_tarefas.winfo_children(): widget.destroy()
        nome_lista = self.lista_atual.get()
        if not nome_lista: return
        # ATUALIZAÇÃO: Se estiver em modo foco, atualiza o título caso a lista tenha sido alterada
        if self.in_focus_mode:
            self.app_title_label.config(text=f"🔍 {nome_lista}")
        
        tarefas = self.dados.get(nome_lista, [])
        
        # Separar tarefas pendentes e concluídas para melhor organização visual
        pendentes = [t for i, t in enumerate(tarefas) if not t['concluida']]
        concluidas = [t for i, t in enumerate(tarefas) if t['concluida']]
        
        # Mostrar pendentes primeiro
        for i, tarefa_data in enumerate(pendentes):
            original_index = tarefas.index(tarefa_data)
            task_widget = TaskFrame(self.frame_tarefas, tarefa_data, original_index, self)
            task_widget.pack(fill='x', expand=True)
        
        # Adicionar separador visual se houver ambos tipos
        if pendentes and concluidas:
            separator_frame = tk.Frame(self.frame_tarefas, bg=COR_JANELA, height=10)
            separator_frame.pack(fill='x', pady=5)
            separator_label = tk.Label(
                separator_frame, 
                text="─────── ✓ Concluídas ───────", 
                bg=COR_JANELA, 
                fg=COR_TEXT_LIGHT,
                font=FONT_SMALL
            )
            separator_label.pack()
        
        # Mostrar concluídas por último
        for i, tarefa_data in enumerate(concluidas):
            original_index = tarefas.index(tarefa_data)
            task_widget = TaskFrame(self.frame_tarefas, tarefa_data, original_index, self)
            task_widget.pack(fill='x', expand=True)
    def excluir_tarefa_pelo_indice(self, index):
        nome_lista = self.lista_atual.get()
        if nome_lista and 0 <= index < len(self.dados[nome_lista]):
            del self.dados[nome_lista][index]
            self.salvar_e_repopular()
    def mover_tarefa(self, index, direcao):
        nome_lista = self.lista_atual.get()
        tarefas = self.dados[nome_lista]
        novo_index = index + direcao
        if 0 <= novo_index < len(tarefas):
            tarefas[index], tarefas[novo_index] = tarefas[novo_index], tarefas[index]
            self.salvar_e_repopular()
    def atualizar_texto_tarefa(self, index, novo_texto):
        nome_lista = self.lista_atual.get()
        if nome_lista and 0 <= index < len(self.dados[nome_lista]):
            self.dados[nome_lista][index]['texto'] = novo_texto
            self.salvar_e_repopular()

    def adicionar_tarefa_inteligente(self, event=None):
        nome_lista = self.lista_atual.get()
        if not nome_lista:
            messagebox.showwarning("Nenhuma Lista", "Crie ou selecione uma lista.")
            return "break"
        texto_bloco = self.entry_inteligente.get("1.0", tk.END).strip()
        if not texto_bloco: return "break"
        for linha in texto_bloco.split('\n'):
            if linha.strip(): self.dados[nome_lista].append({"texto": linha.strip(), "concluida": False})
        self.entry_inteligente.delete("1.0", tk.END)
        self.salvar_e_repopular()
        return "break"
    def carregar_dados(self):
        if not self.data_file.exists(): return {"Minha Primeira Lista": []}
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f: return json.load(f) or {"Minha Primeira Lista": []}
        except (json.JSONDecodeError, IOError): return {"Minha Primeira Lista": []}
    def salvar_dados(self):
        with open(self.data_file, 'w', encoding='utf-8') as f: json.dump(self.dados, f, indent=4, ensure_ascii=False)
    def popular_listas_dropdown(self):
        listas = list(self.dados.keys())
        self.dropdown_listas['values'] = listas
        if listas and not self.lista_atual.get(): self.lista_atual.set(listas[0])
        self.popular_tarefas()
    def criar_nova_lista(self):
        nome = simpledialog.askstring("Nova Lista", "Nome da nova lista?")
        if nome and nome.strip():
            nome = nome.strip()
            if nome in self.dados: messagebox.showwarning("Existente", "Lista já existe.")
            else:
                self.dados[nome] = []
                self.salvar_dados()
                self.popular_listas_dropdown()
                self.lista_atual.set(nome)
    def excluir_lista_atual(self):
        nome = self.lista_atual.get()
        if not nome: return
        if len(self.dados) <= 1:
            messagebox.showerror("Inválido", "Não é possível excluir a última lista.")
            return
        if messagebox.askyesno("Confirmar", f"Excluir a lista '{nome}'?"):
            del self.dados[nome]
            self.lista_atual.set('')
            self.salvar_dados()
            self.popular_listas_dropdown()
    def criar_lista_de_pendentes(self):
        origem = self.lista_atual.get()
        if not origem: return
        pendentes = [t.copy() for t in self.dados[origem] if not t['concluida']]
        if not pendentes:
            messagebox.showinfo("Nada a Fazer", "Nenhuma tarefa pendente.")
            return
        nome_nova = simpledialog.askstring("Nova Lista", "Nome para a lista de pendentes:", initialvalue=f"{origem} - Pendentes")
        if nome_nova and nome_nova.strip():
            nome_nova = nome_nova.strip()
            if nome_nova in self.dados: messagebox.showwarning("Existente", "Lista já existe.")
            else:
                self.dados[nome_nova] = pendentes
                self.salvar_dados()
                self.popular_listas_dropdown()
                self.lista_atual.set(nome_nova)
    def copiar_para_clipboard(self):
        nome = self.lista_atual.get()
        if not nome or not self.dados.get(nome): return
        md_lines = [f"- [{'x' if t['concluida'] else ' '}] {t['texto']}" for t in self.dados[nome]]
        self.clipboard_clear()
        self.clipboard_append("\n".join(md_lines))
        messagebox.showinfo("Sucesso", "Lista copiada como Markdown!")
    def ao_fechar(self):
        self.salvar_dados()
        self.destroy()

if __name__ == "__main__":
    app = ToDoApp()
    app.mainloop()