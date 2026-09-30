        for tentativa in range(3):
            usuario = input("Digite o usuário que deseja deletar: ")
            cursor.execute(
                "SELECT 1 FROM cadastrolibrascode WHERE usuario = %s",
                (usuario,),
            )
            resultado = cursor.fetchone()

            if resultado:
                cursor.execute(
                    "DELETE FROM cadastrolibrascode WHERE usuario = %s",
                    (usuario,),
                )
                conexao.commit()
                print('Usuário deletado com sucesso')
                break

            print(f"Erro {tentativa + 1}/3: usuário não encontrado.")
            if tentativa == 2:
                print("Limite de tentativas atingido. Voltando ao menu principal.")
                