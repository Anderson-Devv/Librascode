import customtkinter as ctk
from PIL import Image
import cadastro_L_Cfinal  

janela_inicial = ctk.CTk()
janela_inicial.title('LibrasCode')
janela_inicial.geometry('1920x1080')

img1 = ctk.CTkImage(light_image=Image.open('./cartão librascode.jpeg'), dark_image=Image.open('./cartão librascode.jpeg'), size=(1920, 1080))
label_fundo = ctk.CTkLabel(janela_inicial, text="", image=img1)
label_fundo.place(x=0, y=0, relwidth=1, relheight=1) 

titulo_principal = ctk.CTkLabel(janela_inicial, text='LibrasCode', font=('arial bold', 80), fg_color='transparent', bg_color='transparent')
titulo_principal.pack(pady=30)

titulo_menu = ctk.CTkLabel(janela_inicial, text='Menu Principal', font=('arial bold', 35), fg_color='transparent', bg_color='transparent')
titulo_menu.pack(pady=10)

def menu_interface():
    pass

botao_cadastro = ctk.CTkButton(janela_inicial, text='Cadastre-se'.upper(), font=('arial', 20), width=250, height=60)
botao_cadastro.pack(pady=20)

botao_logar = ctk.CTkButton(janela_inicial, text='Logar'.upper(), font=('arial', 20), width=250, height=60)
botao_logar.pack(pady=20)

botao_sair = ctk.CTkButton(janela_inicial, text= 'Sair'.upper(), font=('arial', 20), width=250, height=60)
botao_sair.pack(pady=20)

janela_inicial.mainloop()






'''
campo_email = ctk.CTkEntry(janela, placeholder_text='Coloque seu e-mail...', width=250, height=45)
campo_email.pack(pady=10)

campo_senha = ctk.CTkEntry(janela, placeholder_text='Coloque sua senha...', show="*", width=250, height=45)
campo_senha.pack(pady=10)
'''