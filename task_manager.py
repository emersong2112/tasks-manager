import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import json
from pathlib import Path

# --- FONTES E CORES ---
FONT_NORMAL = ("Helvetica", 12)
FONT_RISCADO = ("Helvetica", 12, "overstrike")
COR_FUNDO = "#f0f0f0"
COR_JANELA = "#ffffff"
COR_HOVER = "#eaf4ff"

class TaskFrame(tk.Frame):
    """Um Frame que representa uma única tarefa, com seus botões de ação."""
    def __init__(self, parent, task_data, task_index, app):
        super().__init__(parent, bg=COR_JANELA)
        self.task_data = task_data
        self.task_index = task_index
        self.app = app

        self.var_concluida = tk.BooleanVar(value=task_data['concluida'])
        
        self.checkbutton = tk.Checkbutton(
            self, text=task_data['texto'], variable=self.var_concluida,
            bg=COR_JANELA, anchor='w', command=self.alternar_tarefa
        )
        self.atualizar_estilo_checkbutton()
        
        self.entry_edicao = ttk.Entry(self, font=FONT_NORMAL)
        
        self.action_frame = tk.Frame(self, bg=COR_JANELA)
        
        btn_edit = ttk.Button(self.action_frame, text="✏️", width=3, command=self.iniciar_edicao)
        btn_edit.pack(side='left')
        btn_delete = ttk.Button(self.action_frame, text="🗑️", width=3, command=self.excluir_tarefa)
        btn_delete.pack(side='left')
        btn_up = ttk.Button(self.action_frame, text="▲", width=3, command=lambda: self.app.mover_tarefa(self.task_index, -1))
        if task_index > 0: btn_up.pack(side='left')
        btn_down = ttk.Button(self.action_frame, text="▼", width=3, command=lambda: self.app.mover_tarefa(self.task_index, 1))
        total_tasks = len(self.app.dados[self.app.lista_atual.get()])
        if task_index < total_tasks - 1: btn_down.pack(side='left')

        self.checkbutton.pack(side='left', fill='x', expand=True, padx=5, pady=2)
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.checkbutton.bind("<Enter>", self.on_enter)
        self.checkbutton.bind("<Leave>", self.on_leave)
        self.action_frame.bind("<Enter>", self.on_enter)
        self.action_frame.bind("<Leave>", self.on_leave)

    def on_enter(self, event=None):
        if not self.entry_edicao.winfo_viewable():
            self.configure(bg=COR_HOVER)
            self.checkbutton.configure(bg=COR_HOVER)
            self.action_frame.configure(bg=COR_HOVER)
            self.action_frame.pack(side='right', padx=5)

    def on_leave(self, event=None):
        if not self.winfo_containing(event.x_root, event.y_root) in self.action_frame.winfo_children():
            self.configure(bg=COR_JANELA)
            self.checkbutton.configure(bg=COR_JANELA)
            self.action_frame.configure(bg=COR_JANELA)
            self.action_frame.pack_forget()

    def alternar_tarefa(self):
        self.task_data['concluida'] = self.var_concluida.get()
        self.atualizar_estilo_checkbutton()
        self.app.salvar_e_repopular()

    def atualizar_estilo_checkbutton(self):
        font = FONT_RISCADO if self.task_data['concluida'] else FONT_NORMAL
        self.checkbutton.config(font=font)
        
    def excluir_tarefa(self): self.app.excluir_tarefa_pelo_indice(self.task_index)
    def iniciar_edicao(self):
        self.checkbutton.pack_forget()
        self.action_frame.pack_forget()
        self.entry_edicao.pack(side='left', fill='x', expand=True, padx=5)
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
        self.title("Bloco de Tarefas")
        self.full_geometry = "500x550"
        self.geometry(self.full_geometry)
        self.configure(bg=COR_FUNDO)
        self.data_file = Path("tasks.json")
        self.dados = self.carregar_dados()
        self.lista_atual = tk.StringVar()
        self.in_focus_mode = False
        self.criar_widgets()
        self.popular_listas_dropdown()
        self.protocol("WM_DELETE_WINDOW", self.ao_fechar)

    def criar_widgets(self):
        header_frame = tk.Frame(self, bg=COR_FUNDO)
        header_frame.pack(fill='x', padx=10, pady=(5,0))
        self.app_title_label = tk.Label(header_frame, text="Bloco de Tarefas", bg=COR_FUNDO, font=("Helvetica", 11, "bold"))
        self.app_title_label.pack(side='left')
        self.focus_button = ttk.Button(header_frame, text="Modo Foco 🔍", command=self.toggle_focus_mode)
        self.focus_button.pack(side='right')

        self.frame_listas = tk.Frame(self, bg=COR_FUNDO)
        self.frame_listas.pack(fill='x', padx=10, pady=5)
        tk.Label(self.frame_listas, text="Lista:", bg=COR_FUNDO).pack(side='left')
        self.dropdown_listas = ttk.Combobox(self.frame_listas, textvariable=self.lista_atual, state="readonly", width=20)
        self.dropdown_listas.pack(side='left', fill='x', expand=True, padx=5)
        self.dropdown_listas.bind("<<ComboboxSelected>>", lambda e: self.popular_tarefas())
        btn_nova_lista = ttk.Button(self.frame_listas, text="+", width=3, command=self.criar_nova_lista)
        btn_nova_lista.pack(side='left')
        btn_excluir_lista = ttk.Button(self.frame_listas, text="-", width=3, command=self.excluir_lista_atual)
        btn_excluir_lista.pack(side='left', padx=(5,0))

        self.canvas_frame = tk.Frame(self, bg=COR_JANELA, relief="solid", borderwidth=1)
        self.canvas_frame.pack(fill='both', expand=True, padx=10, pady=5)
        canvas = tk.Canvas(self.canvas_frame, bg=COR_JANELA, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.canvas_frame, orient="vertical", command=canvas.yview)
        self.frame_tarefas = tk.Frame(canvas, bg=COR_JANELA)
        self.frame_tarefas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.frame_tarefas, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.frame_tarefas.bind('<MouseWheel>', lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        canvas.bind('<MouseWheel>', lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        self.frame_adicionar = tk.Frame(self, bg=COR_FUNDO)
        self.frame_adicionar.pack(fill='x', padx=10, pady=5)
        self.entry_inteligente = tk.Text(self.frame_adicionar, height=1, font=FONT_NORMAL, relief="solid", borderwidth=1)
        self.entry_inteligente.pack(side='left', fill='x', expand=True, ipady=4)
        self.entry_inteligente.bind("<Return>", self.adicionar_tarefa_inteligente)
        btn_adicionar = ttk.Button(self.frame_adicionar, text="Adicionar", command=self.adicionar_tarefa_inteligente)
        btn_adicionar.pack(side='left', padx=(5,0))

        self.frame_opcoes = tk.Frame(self, bg=COR_FUNDO)
        self.frame_opcoes.pack(fill='x', padx=10, pady=(5, 10))
        btn_copiar_md = ttk.Button(self.frame_opcoes, text="Copiar (Markdown)", command=self.copiar_para_clipboard)
        btn_copiar_md.pack(fill='x', side='left', expand=True, padx=(0,5))
        btn_pendentes = ttk.Button(self.frame_opcoes, text="Criar Lista de Pendentes", command=self.criar_lista_de_pendentes)
        btn_pendentes.pack(fill='x', side='left', expand=True)

    def toggle_focus_mode(self):
        self.in_focus_mode = not self.in_focus_mode
        if self.in_focus_mode:
            self.frame_listas.pack_forget()
            self.frame_adicionar.pack_forget()
            self.frame_opcoes.pack_forget()
            self.focus_button.config(text="Expandir ↔️")
            # ATUALIZAÇÃO: Mostra o nome da lista atual no modo foco
            self.app_title_label.config(text=self.lista_atual.get())
            self.geometry("350x400")
        else:
            self.frame_listas.pack(fill='x', padx=10, pady=5, before=self.canvas_frame)
            self.frame_adicionar.pack(fill='x', padx=10, pady=5)
            self.frame_opcoes.pack(fill='x', padx=10, pady=(5, 10))
            self.focus_button.config(text="Modo Foco 🔍")
            self.app_title_label.config(text="Bloco de Tarefas")
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
            self.app_title_label.config(text=nome_lista)
        tarefas = self.dados.get(nome_lista, [])
        for i, tarefa_data in enumerate(tarefas):
            task_widget = TaskFrame(self.frame_tarefas, tarefa_data, i, self)
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