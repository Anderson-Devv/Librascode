# 📚 LIBRASCODE


O **LibrasCode** é uma plataforma gamificada voltada à aprendizagem de LIBRAS (Língua Brasileira de Sinais), com o intuito de ensinar as pessoas que querem aprender sobre
a linguagem de sinais brasileira, e assim, podermos promover uma inclusão eficaz de pessoas deficientes-auditivas na educação e sociedade num contexto geral.

---
<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/f96ba174-d097-47da-94ac-8465634e1908" />

## 🚀 Release 1.0

| Funcionalidade                     | Descrição                                                                                                                                |
| ---------------------------------- | -----------------------------------------------------------------------------------------------------------------------------------------|
| Cadastro de usuários               | Permite que novos usuários criem uma conta no sistema.                                                                                   |
| Login                              | Permite que o usuário entre no sistema utilizando seus dados cadastrados.                                                                |
| Atualizar informações              | Permite usuário alterar suas informações                                                                                                 |
| Deleção de conta                   | Permite usuário deletar sua conta                                                                                                        |
| Lições de Libras                   | Dispõe questões para o usuário responder e entender palavras em libras.                                                                  |
| Interface Gráfica                  | Interface interativa com opções de cadastro e login                                                                                      |
| Menu                               | Sistema que apresenta ao usuário as funcionalidades disponíveis para ele usufruir                                                        |


## 📚 Bibliotecas utilizadas no projeto

| Biblioteca                         | Para que é utilizada                                                                                                                     |
| ---------------------------------- | -----------------------------------------------------------------------------------------------------------------------------------------|
| mysql.connector                    | Conectar o Python ao banco de dados MySQL, executar consultas e tratar erros de conexão.                                                 |
| customtkinter                      | Criar a interface gráfica do sistema, incluindo janelas, botões, campos de texto, caixas de diálogo e entre outros.                      |         
| Pillow (PIL)                       | Carregar, redimensionar e manipular imagens utilizadas na interface e nas lições.                                                        |
| requests                           | Fazer requisições HTTP para a API do LibrasCode, permitindo que a interface solicite dados e envie respostas.                            |

FRAMEWORK: Flask
O Flask foi utilizado para desenvolver a API responsável pela comunicação entre a interface gráfica e o banco de dados. Ele permite consultar módulos e lições, registrar respostas, calcular pontuações, consultar o ranking e disponibilizar as mídias utilizadas nas atividades, retornando os dados para a interface em formato JSON
