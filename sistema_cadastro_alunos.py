
import tkinter as tk
from tkinter import ttk, messagebox
from conexao import conectar


# FUNÇÃO AUXILIAR PARA CONSULTAS
def consultar(sql, parametros=()):
    conexao = conectar()

    try:
        with conexao.cursor() as cursor:
            cursor.execute(sql, parametros)
            return cursor.fetchall()
    finally:
        conexao.close()


# FUNÇÃO AUXILIAR PARA ALTERAÇÕES
def executar(sql, parametros):
    conexao = conectar()

    try:
        with conexao.cursor() as cursor:
            cursor.execute(sql, parametros)
        conexao.commit()
    except Exception:
        conexao.rollback()
        raise
    finally:
        conexao.close()


# VALIDAR OS DADOS
def obter_dados():
    nome = campo_nome.get().strip()
    idade = campo_idade.get().strip()
    curso = campo_curso.get().strip()

    if not nome or not idade or not curso:
        messagebox.showwarning(
            "Atenção", "Preencha todos os campos!"
        )
        return None

    try:
        idade = int(idade)
        if idade <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror(
            "Erro", "Informe uma idade válida!"
        )
        return None

    return nome, idade, curso


# CREATE - CADASTRAR
def cadastrar():
    dados = obter_dados()

    if dados is None:
        return

    try:
        executar(
            """
            INSERT INTO alunos (nome, idade, curso)
            VALUES (%s, %s, %s)
            """,
            dados
        )

        messagebox.showinfo(
            "Sucesso", "Aluno cadastrado!"
        )
        limpar()
        listar()

    except Exception as erro:
        messagebox.showerror("Erro", str(erro))


# READ - LISTAR
def listar():
    try:
        registros = consultar(
            """
            SELECT id, nome, idade, curso
            FROM alunos
            ORDER BY id
            """
        )
        preencher_tabela(registros)

    except Exception as erro:
        messagebox.showerror("Erro", str(erro))


# READ - PESQUISAR
def pesquisar():
    nome = campo_busca.get().strip()

    try:
        registros = consultar(
            """
            SELECT id, nome, idade, curso
            FROM alunos
            WHERE nome ILIKE %s
            ORDER BY id
            """,
            (f"%{nome}%",)
        )
        preencher_tabela(registros)

    except Exception as erro:
        messagebox.showerror("Erro", str(erro))


# PREENCHER A TABELA VISUAL
def preencher_tabela(registros):
    for item in tabela.get_children():
        tabela.delete(item)

    for registro in registros:
        tabela.insert(
            "", tk.END, values=registro
        )


# SELECIONAR ALUNO
def selecionar(evento):
    selecionados = tabela.selection()

    if not selecionados:
        return

    dados = tabela.item(
        selecionados[0], "values"
    )

    limpar_campos()

    campo_nome.insert(0, dados[1])
    campo_idade.insert(0, dados[2])
    campo_curso.insert(0, dados[3])


# UPDATE - ATUALIZAR
def atualizar():
    selecionados = tabela.selection()

    if not selecionados:
        messagebox.showwarning(
            "Atenção", "Selecione um aluno!"
        )
        return

    dados = obter_dados()

    if dados is None:
        return

    id_aluno = tabela.item(
        selecionados[0], "values"
    )[0]

    try:
        executar(
            """
            UPDATE alunos
            SET nome = %s,
                idade = %s,
                curso = %s
            WHERE id = %s
            """,
            (*dados, id_aluno)
        )

        messagebox.showinfo(
            "Sucesso", "Aluno atualizado!"
        )
        limpar()
        listar()

    except Exception as erro:
        messagebox.showerror("Erro", str(erro))


# DELETE - EXCLUIR
def excluir():
    selecionados = tabela.selection()

    if not selecionados:
        messagebox.showwarning(
            "Atenção", "Selecione um aluno!"
        )
        return

    confirmar = messagebox.askyesno(
        "Confirmação",
        "Deseja realmente excluir este aluno?"
    )

    if not confirmar:
        return

    id_aluno = tabela.item(
        selecionados[0], "values"
    )[0]

    try:
        executar(
            "DELETE FROM alunos WHERE id = %s",
            (id_aluno,)
        )

        messagebox.showinfo(
            "Sucesso", "Aluno excluído!"
        )
        limpar()
        listar()

    except Exception as erro:
        messagebox.showerror("Erro", str(erro))


# LIMPAR CAMPOS
def limpar_campos():
    campo_nome.delete(0, tk.END)
    campo_idade.delete(0, tk.END)
    campo_curso.delete(0, tk.END)


def limpar():
    limpar_campos()

    for item in tabela.selection():
        tabela.selection_remove(item)


# CRIAR JANELA
janela = tk.Tk()
janela.title("Sistema Escolar - CRUD")
janela.geometry("850x600")
janela.configure(bg="#F4F6F8")


# TÍTULO
titulo = tk.Label(
    janela,
    text="SISTEMA DE CADASTRO DE ALUNOS",
    font=("Arial", 18, "bold"),
    bg="#F4F6F8"
)
titulo.pack(pady=20)


# FORMULÁRIO
formulario = tk.Frame(
    janela, bg="#F4F6F8"
)
formulario.pack(pady=10)

tk.Label(
    formulario, text="Nome:",
    bg="#F4F6F8"
).grid(row=0, column=0, pady=5)

campo_nome = tk.Entry(
    formulario, width=35
)
campo_nome.grid(row=0, column=1, padx=10)

tk.Label(
    formulario, text="Idade:",
    bg="#F4F6F8"
).grid(row=1, column=0, pady=5)

campo_idade = tk.Entry(
    formulario, width=35
)
campo_idade.grid(row=1, column=1, padx=10)

tk.Label(
    formulario, text="Curso:",
    bg="#F4F6F8"
).grid(row=2, column=0, pady=5)

campo_curso = tk.Entry(
    formulario, width=35
)
campo_curso.grid(row=2, column=1, padx=10)


# BOTÕES CRUD
botoes = tk.Frame(
    janela, bg="#F4F6F8"
)
botoes.pack(pady=15)

tk.Button(
    botoes, text="Cadastrar",
    command=cadastrar,
    bg="#198754", fg="white",
    width=12
).grid(row=0, column=0, padx=5)

tk.Button(
    botoes, text="Atualizar",
    command=atualizar,
    width=12
).grid(row=0, column=1, padx=5)

tk.Button(
    botoes, text="Excluir",
    command=excluir,
    bg="#DC3545", fg="white",
    width=12
).grid(row=0, column=2, padx=5)

tk.Button(
    botoes, text="Limpar",
    command=limpar,
    width=12
).grid(row=0, column=3, padx=5)


# ÁREA DE PESQUISA
pesquisa = tk.Frame(
    janela, bg="#F4F6F8"
)
pesquisa.pack(pady=10)

campo_busca = tk.Entry(
    pesquisa, width=35
)
campo_busca.grid(row=0, column=0, padx=5)

tk.Button(
    pesquisa, text="Pesquisar",
    command=pesquisar
).grid(row=0, column=1, padx=5)

tk.Button(
    pesquisa, text="Listar todos",
    command=listar
).grid(row=0, column=2, padx=5)


# TABELA TREEVIEW
colunas = ("ID", "Nome", "Idade", "Curso")

tabela = ttk.Treeview(
    janela,
    columns=colunas,
    show="headings"
)

for coluna in colunas:
    tabela.heading(coluna, text=coluna)
    tabela.column(coluna, width=150)

tabela.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=15
)

tabela.bind(
    "<<TreeviewSelect>>", selecionar
)


# CARREGAR DADOS INICIAIS
listar()

janela.mainloop()
