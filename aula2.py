#formulario simples


import tkinter as tk
from tkinter import messagebox, ttk #Importa o módulo messagebox, que permite exibir caixas de mensagens. e tkk
#dispõe citens adicionais de Tkinter como o Combobox, que é uma caixa de seleção suspensa.

janela = tk.Tk()
janela.title("Sistema Escolar")
janela.geometry("500x3400")

def cadastrar():
    nome = campo_nome.get().strip() # .GET() Obtém o valor do campo de entrada "Nome" e .STRIP() remove espaços em branco
    idade = campo_idade.get().strip()
    telefone = campo_telefone.get().strip()
    curso = campo_curso.get().strip() # .GET() Obtém o valor do campo de entrada "Curso" e .STRIP() remove espaços em branco

 
    if not nome or not idade or not curso or not telefone: #SE não houver NOME ou não houver CURSO ou não houver IDADE ou não houver TELEFONE, exibe uma mensagem de aviso e retorna da função.
        #metodo.showwarning() exibe uma caixa de aviso.
        messagebox.showwarning( 
            "Atenção",
            "Preencha todos os campos!"
        )
        return  
    # Verifica se a idade é um número inteiro válido
    try:
        idade_numero = int(idade)
        if idade_numero < 0:
            raise ValueError
    except ValueError:
        messagebox.showwarning(
            "Atenção",
            "Digite uma idade inteira válida!"
        )
        return

#Exibindo a mensagem de cadastro
#.showinfo() show exibe, info informação
    messagebox.showinfo(
        "Cadastro",
        f"Aluno: {nome}\nIdade: {idade}\nTelefone: {telefone}\nCurso: {curso}\n"
        "Cadastrado com sucesso!"
    )

#Limpar os campos após o cadastro para digitar novamente novos dados
def limpar():
    campo_nome.delete(0, tk.END)
    campo_idade.delete(0, tk.END)
    campo_telefone.delete(0, tk.END)
    campo_curso.set("")

    
#Criando o título da interface
#tk.label() cria componente visual que exibe texto ou imagem na janela.
#janela Indica que o Label pertence à janela principal.
#text Define o texto exibido no Label.
titulo = tk.Label(
    janela,
    text="Sistema Escolar",
    font=("Arial", 18, "bold")
)
titulo.pack(pady=15)
#.pack() organiza e posiciona os comonentes detro da janela. O argumento pady adiciona espaçamento vertical externo de 15px acima e abaixo do componente.

tk.Label(janela, text="Nome:").pack()
#tk.Label(): cria um componente de texto.
#janela: indica onde ele será colocado.
#text="Nome:": define o texto.
#.pack(): posiciona o componente.
#VAI COLOCAR O NOME DO ALUNO DENTRO DA CX

#Criando o campo de digitação do nome
campo_nome = tk.Entry(janela, width=35)
campo_nome.pack(pady=5)
#tk.Entry(): cria um campo onde o usuário pode digitar texto.
#janela: indica que o campo pertence à janela.
#width=35: define uma largura aproximada

tk.Label(janela, text="Idade:").pack()

campo_idade = tk.Entry(janela, width=35)
campo_idade.pack(pady=5)

tk.Label(janela, text="Telefone:").pack()
campo_telefone = tk.Entry(janela, width=35)
campo_telefone.pack(pady=5)

# tkk.Combobox() = Cria uma lista suspensa
#janela = Define onde o componente será colocado
#values = define as opçõ9es disponiveis
#state="readonly" = Permite selecionar, mas não digitar outras opções

campo_curso = ttk.Combobox(
    janela,
    values=[
        "Informática",
        "Administrativo",
        "Inteligência Artificial"
    ],
    state="readonly",
    width=32
)
campo_curso.pack(pady=5)


#Criando o botão Cadastrar
#command=cadastrar Significa que, quando o usuário clicar no botão, o Tkinter deverá executar a função cadastrar.
botao = tk.Button(
    janela,
    text="Cadastrar",
    command=cadastrar,
    bg="#4373DA",
    fg="white"
)
botao.pack(pady=15)
#Posiciona o botão na interface e adiciona espaçamento vertical.

botao_limpar = tk.Button(
    janela,
    text="Limpar",
    command=limpar,
    bg="red",
    fg="white"
)
botao_limpar.pack(pady=5)

janela.mainloop()


 #INFORMA      #ALERTA
#showinfo() e showwarning()
#  Se algum campo estiver vazio, o programa utiliza showwarning() para alertar o usuário.
# Se todos os campos estiverem preenchidos, utiliza showinfo() para informar que os dados foram preenchidos corretamente.
