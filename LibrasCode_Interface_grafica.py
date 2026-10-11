import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

from librascodebd import conexao_banco
from login import fazer_login


# ==========================
# CONFIGURAÇÃO
# ==========================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

conexao = conexao_banco()
cursor = conexao.cursor()


# ==========================
# JANELA PRINCIPAL
# ==========================

janela_inicial = ctk.CTk()
janela_inicial.title("LibrasCode")
janela_inicial.geometry("1920x1080")




imagem_login = ctk.CTkImage(
        light_image=Image.open("./500x400.jpeg"),
        dark_image=Image.open("./500x400.jpeg"),
        size=(500, 400)
    )

try:
    img = ctk.CTkImage(
        light_image=Image.open("./cartão librascode.jpeg"),
        dark_image=Image.open("./cartão librascode.jpeg"),
        size=(1920, 1080)
    )

    fundo = ctk.CTkLabel(
        janela_inicial,
        text="",
        image=img
    )

    fundo.place(x=0, y=0, relwidth=1, relheight=1)

except:
    pass


titulo = ctk.CTkLabel(
    janela_inicial,
    text="LIBRASCODE",
    font=("Arial", 50, "bold")
)

titulo.pack(pady=30)


# ==========================
# CADASTRAR USUÁRIO
# ==========================

def abrir_cadastro():

    janela = ctk.CTkToplevel(janela_inicial)
    janela.title("Cadastro")
    janela.geometry("1920x1080")
    label_fundo = ctk.CTkLabel(
        janela,
        text="",
        image=img,
    )
    
    label_fundo.place(x=0, y=0, relwidth=1, relheight=1)
    
    ctk.CTkLabel(
        janela,
        text="Nome de Usuário"
    ).pack(pady=10)

    campo_usuario = ctk.CTkEntry(janela, width=300)
    campo_usuario.pack()

    ctk.CTkLabel(
        janela,
        text="Email"
    ).pack(pady=10)

    campo_email = ctk.CTkEntry(janela, width=300)
    campo_email.pack()

    ctk.CTkLabel(
        janela,
        text="Senha"
    ).pack(pady=10)

    campo_senha = ctk.CTkEntry(
        janela,
        show="*",
        width=300
    )
    campo_senha.pack()

    def cadastrar():

        usuario = campo_usuario.get().strip()
        email = campo_email.get().strip()
        senha = campo_senha.get()

        if len(usuario) < 3 or len(usuario) > 15:
            messagebox.showerror(
                "Erro",
                "Usuário deve ter entre 3 e 15 caracteres."
            )
            return

        if "@ufrpe.br" not in email:
            messagebox.showerror(
                "Erro",
                "Email precisa conter @ufrpe.br"
            )
            return

        if len(senha) < 8 or len(senha) > 15:
            messagebox.showerror(
                "Erro",
                "Senha deve ter entre 8 e 15 caracteres."
            )
            return

        try:

            cursor.execute(
                """
                INSERT INTO cadastrolibrascode
                (usuario, senha, email)
                VALUES (%s,%s,%s)
                """,
                (usuario, senha, email)
            )

            conexao.commit()

            messagebox.showinfo(
                "Sucesso",
                "Usuário cadastrado com sucesso!"
            )

            janela.destroy()

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                str(erro)
            )

    ctk.CTkButton(
        janela,
        text="Cadastrar",
        command=cadastrar
    ).pack(pady=20)


# ==========================
# MENU DO USUÁRIO
# ==========================

def abrir_menu_usuario(email):

    janela = ctk.CTkToplevel(janela_inicial)
    janela.title("Área do Usuário")
    janela.geometry("1920x1080")
    label_fundo_user = ctk.CTkLabel(
        janela,
        text="",
        image=img,
    )
    
    label_fundo_user.place(x=0, y=0, relwidth=1, relheight=1)
    
    ctk.CTkLabel(
        janela,
        text=f"Usuário logado:\n{email}",
        font=("Arial", 20)
    ).pack(pady=20)


    def alterar_senha():

        dialog = ctk.CTkInputDialog(
            text="Digite a nova senha",
            title="Alterar senha"
        )

        nova_senha = dialog.get_input()

        if not nova_senha:
            return

        cursor.execute(
            """
            UPDATE cadastrolibrascode
            SET senha=%s
            WHERE email=%s
            """,
            (nova_senha, email)
        )

        conexao.commit()

        messagebox.showinfo(
            "Sucesso",
            "Senha alterada!"
        )


    def alterar_email():

        dialog = ctk.CTkInputDialog(
            text="Digite o novo email",
            title="Alterar email"
        )

        novo_email = dialog.get_input()

        if not novo_email:
            return

        cursor.execute(
            """
            UPDATE cadastrolibrascode
            SET email=%s
            WHERE email=%s
            """,
            (novo_email, email)
        )

        conexao.commit()

        messagebox.showinfo(
            "Sucesso",
            "Email alterado!"
        )


    def deletar_conta():

        resposta = messagebox.askyesno(
            "Confirmação",
            "Deseja realmente deletar sua conta?"
        )

        if resposta:

            cursor.execute(
                """
                DELETE FROM cadastrolibrascode
                WHERE email=%s
                """,
                (email,)
            )

            conexao.commit()

            messagebox.showinfo(
                "Sucesso",
                "Conta deletada!"
            )

            janela.destroy()


    ctk.CTkButton(
        janela,
        text="Alterar Senha",
        width=250,
        command=alterar_senha
    ).pack(pady=10)

    ctk.CTkButton(
        janela,
        text="Alterar Email",
        width=250,
        command=alterar_email
    ).pack(pady=10)

    ctk.CTkButton(
        janela,
        text="Deletar Conta",
        width=250,
        fg_color="red",
        hover_color="#990000",
        command=deletar_conta
    ).pack(pady=10)

    ctk.CTkButton(
        janela,
        text="Sair",
        width=250,
        command=janela.destroy
    ).pack(pady=10)


# ==========================
# LOGIN
# ==========================

def abrir_login():

    janela = ctk.CTkToplevel(janela_inicial)
    janela.title("Login")
    janela.geometry("500x400")
    label_texto_login = ctk.CTkLabel(
        janela,
        text="Login",
        font=("arial", 20, "bold")
    )
    
    label_texto_login.place(x=200, y=20)
    
    label_fundo_login = ctk.CTkLabel(
        janela,
        text="",
        image=imagem_login
    )
    label_fundo_login.place(x=0, y=0, relwidth=1, relheight=1)
    
    ctk.CTkLabel(
        janela,
        text="Email"
    ).pack(pady=10)

    campo_email = ctk.CTkEntry(
        janela,
        width=300
    )

    campo_email.pack()

    ctk.CTkLabel(
        janela,
        text="Senha"
    ).pack(pady=10)

    campo_senha = ctk.CTkEntry(
        janela,
        width=300,
        show="*"
    )

    campo_senha.pack()

    def logar():

        email = campo_email.get()
        senha = campo_senha.get()

        resultado = fazer_login(
            email,
            senha
        )

        if resultado:

            messagebox.showinfo(
                "Sucesso",
                "Login realizado!"
            )

            abrir_menu_usuario(email)

            janela.destroy()

        else:

            messagebox.showerror(
                "Erro",
                "Email ou senha incorretos."
            )

    ctk.CTkButton(
        janela,
        text="Entrar",
        command=logar
    ).pack(pady=20)


# ==========================
# BOTÕES PRINCIPAIS
# ==========================

ctk.CTkButton(
    janela_inicial,
    text="CADASTRE-SE",
    width=250,
    height=50,
    command=abrir_cadastro
).pack(pady=15)

ctk.CTkButton(
    janela_inicial,
    text="LOGAR",
    width=250,
    height=50,
    command=abrir_login
).pack(pady=15)

ctk.CTkButton(
    janela_inicial,
    text="SAIR",
    width=250,
    height=50,
    command=janela_inicial.destroy
).pack(pady=15)

janela_inicial.mainloop()