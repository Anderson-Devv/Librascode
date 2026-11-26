# 📚 LibrasCode 🤚🏽

O **LibrasCode** é uma plataforma gamificada voltada à aprendizagem de LIBRAS (Língua Brasileira de Sinais), com o intuito de facilitar o entendimento das pessoas que querem aprender sobre
a linguagem de sinais brasileira, e assim, podermos promover uma inclusão eficaz de pessoas deficientes-auditivas.

---
<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/f96ba174-d097-47da-94ac-8465634e1908" />

## 🎯 Público-Alvo
Inicialmente, o LibrasCode está voltado para o público universitário da Universidade Federal Rural de Pernambuco (UFRPE), mas, futuramente, pode se estender para abranger o estado, ou até mesmo o país.

## 🚀 Release 1.0
| Funcionalidade                     | Descrição                                                                                                                                |
| ---------------------------------- | -----------------------------------------------------------------------------------------------------------------------------------------|
| Cadastro de usuários               | Permite que novos usuários criem uma conta no sistema                                                                                    |
| Login                              | Permite que o usuário entre no sistema utilizando seus dados que já foram cadastrados                                                    |
| Atualizar informações              | Permite que o usuário altere suas informações                                                                                            |
| Deleção de conta                   | Permite que o usuário delete sua conta                                                                                                   |
| Lições de Libras                   | Dispõe questões para o usuário responder e entender palavras em libras                                                                   |
| Interface Gráfica                  | Interface interativa com opções de cadastro e login                                                                                      |
| Menu                               | Sistema que apresenta ao usuário as funcionalidades disponíveis para ele usufruir                                                        |

## 🚀 Release 2.0
| Funcionalidade                     | Descrição                                                                                                                                                       |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Ranking Global                     | Permite que os usuários vejam suas pontuações e quantidade de acertos, quem possui mais pontos no ranking e os 10 usuários com mais pontos aparecem em destaque |   
| Recompensas (Medalhas)             | Bônus simbólicos concedidos aos usuários que concluem uma certa quantia de módulos                                                                              |
| Pesquisar Sinais                   | Permite explorar os sinais disponíveis e ver um preview dos gifs                                                                                                |
| Favoritar Sinais                   | Permite selecionar um sinal e deixá-lo destacado no menu de pesquisa                                                                                            |
| Certificado                        | Certificado concedido ao usuário que concluir todos os módulos de questões pelo menos uma vez                                                                   |
| Material de Apoio - Guia Inicial   | PDF que contém instruções sobre a didática da plataforma e outras informações importantes                                                                       |

## 🚀 Release 2.1 - EXTRA! 👌🏽
| Funcionalidade / Enhacement        | Descrição                                                                                                                                                       |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Sugerir Sinais                     | Permite que um usuário faça upload de algum arquivo sugerindo um novo sinal para ser inserido na plataforma, no qual somente moderadores conseguem aprovar      |   



## 📚 Tecnologias & Bibliotecas Utilizadas
| Tecnologia / Biblioteca            | Utilização                                                                                                                               |
| ---------------------------------- | -----------------------------------------------------------------------------------------------------------------------------------------|
| Python                             | Linguagem de progromação utilizada para desenvolvimento do projeto                                                                       |
| mysql.connector                    | Conectar o Python ao banco de dados MySQL, executar consultas e tratar erros de conexão.                                                 |
| customtkinter                      | Criar a interface gráfica do sistema, incluindo janelas, botões, campos de texto, caixas de diálogo e entre outros.                      |         
| Pillow (PIL)                       | Carregar, redimensionar e manipular imagens utilizadas na interface e nas lições.                                                        |
| requests                           | Fazer requisições HTTP para a API do LibrasCode, permitindo que a interface solicite dados e envie respostas.                            |
| Framework - Flask                  | Desenvolver a API responsável pela comunicação entre a interface gráfica e o banco de dados (retorna dados para a interface em JSON      |
| ReportLab                          | Gerar arquivos PDF diretamente pelo código, também desenha as bordas, linhas e textos do certificado                                     |

## 💻 Como Executar o Código:
1. Clone este repositório:
```bash
git clone https://github.com/Anderson-Devv/Librascode.git
```

2. Acesse a pasta do projeto:
```bash
cd Librascode
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute o código:
```bash
python main.py
```

## 🧬 Fluxogramas:
```bash
https://drive.google.com/file/d/1ddffPOG2tuZTm98RcU_hfTJZ1_W9wj93/view?usp=sharing
```

## 📄 Artigo:
```bash
https://www.overleaf.com/project/6ae1ed27c58909a3ec188a08
```

## 🚹 Devs:
| Nome do Desenvolvedor              | Função                      |
| ---------------------------------- | ----------------------------|
| Álvaro                             | Desenvolvimento do projeto  |
| Anderson                           | Desenvolvimento do projeto  |     
| Seann                              | Desenvolvimento do projeto  |       
