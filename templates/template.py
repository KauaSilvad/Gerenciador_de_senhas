import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.curdir))

from model.password import Password
from views.password_views import FernetHasher

# Função principal da interface do Streamlit
def main():
    st.title("Gerenciador de Senhas")
    
    # Pergunta pro usuário o que ele quer fazer
    action = st.radio("Escolha uma ação:", ["Salvar uma nova senha", "Ver uma senha"])
    
    if action == "Salvar uma nova senha":
        # Se for a primeira vez, gera uma chave única e exibe para o usuário
        if len(Password.get()) == 0:
            key, path = FernetHasher.create_key(archive=True)
            st.warning('Sua chave foi criada! Salve-a com cuidado, porque se perder, não dá pra recuperar as senhas.')
            st.text(f'Chave: {key.decode("utf-8")}')
            
            # Mostra um aviso extra pra reforçar a importância de guardar a chave
            st.info('Atenção: Esta é sua chave única. Salve-a em um lugar seguro. Sem ela, não tem como recuperar suas senhas.')

            if path:
                st.info('Chave salva em um arquivo. Lembre de mover o arquivo para um lugar seguro e depois apagar aqui.')
                st.text(f'Caminho: {path}')
        else:
            # Se já tiver uma chave, pede pro usuário informar
            key = st.text_input("Digite sua chave usada para criptografia (use sempre a mesma chave):", type="password")
        
        # Pede o domínio e a senha
        domain = st.text_input("Domínio:")
        password = st.text_input("Digite a senha:", type="password")
        
        # Salva a senha quando o usuário clicar no botão
        if st.button("Salvar Senha"):
            if key and domain and password:
                fernet = FernetHasher(key)
                encrypted_password = fernet.encrypt(password).decode('utf-8')
                p1 = Password(domain=domain, password=encrypted_password)
                p1.save()
                st.success("Senha salva com sucesso!")
            else:
                st.error("Preencha todos os campos.")

    elif action == "Ver uma senha":
        # Pede o domínio e a chave pra mostrar a senha
        domain = st.text_input("Domínio:")
        key = st.text_input("Chave:", type="password")
        
        if st.button("Visualizar Senha"):
            if key and domain:
                fernet = FernetHasher(key)
                data = Password.get()
                password = ''
                for entry in data:
                    if domain in entry['domain']:
                        password = fernet.decrypt(entry['password'])
                if password:
                    st.success(f"Sua senha: {password}")
                else:
                    st.error("Nenhuma senha encontrada para esse domínio.")
            else:
                st.error("Preencha todos os campos.")

# Executa a interface
if __name__ == '__main__':
    main()
