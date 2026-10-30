
import streamlit as st

# Configurando a página
st.set_page_config(
    page_title="Sistema de Cadastro de Atletas",
    layout="wide"
)

# Criando o menu lateral
st.sidebar.title("Sistema de Atletas")

# Opções disponíveis no menu
pagina = st.sidebar.radio(
    "Navegação",
    [
        "Início",
        "Cadastro de Atletas",
        "Consulta de Atletas",
        "Relatórios"
    ]
)


# Página inicial
if pagina == "Início":

    st.title("Sistema de Cadastro de Atletas")

    st.write(
        "Sistema para cadastro, consulta e gerenciamento "
        "de informações de atletas."
    )

    st.divider()

    st.subheader("Página inicial")

    st.info("Bem-vindo ao sistema!")


# Página de cadastro
elif pagina == "Cadastro de Atletas":

    st.title("Cadastro de Atletas")

    st.write("Preencha os dados abaixo para cadastrar um atleta.")

    st.divider()

    # Formulario com os dados do atleta
    with st.form("formulario_atleta"):

        # Dados pessoais
        st.subheader("Dados pessoais")

        nome = st.text_input("Nome completo")

        data_nascimento = st.date_input(
            "Data de nascimento",
            format="DD/MM/YYYY"
        )

        sexo = st.selectbox(
            "Sexo",
            ["Selecione", "Feminino", "Masculino", "Outro"]
        )

        st.divider()

        # Dados esportivos
        st.subheader("Informações esportivas")

        modalidade = st.selectbox(
            "Modalidade",
            [
                "Selecione",
                "Vôlei",
                "Futebol",
                "Basquete",
                "Handebol",
                "Natação",
                "Atletismo",
                "Outra"
            ]
        )

        equipe = st.text_input("Equipe ou clube")

        posicao = st.text_input("Posição ou função")

        st.divider()

        # Dados para contato
        st.subheader("Contato")

        telefone = st.text_input("Telefone")

        email = st.text_input("E-mail")

        # Botao para enviar os dados
        cadastrar = st.form_submit_button("Cadastrar atleta")

        # Verificando se os campos obrigatorios foram preenchidos
        if cadastrar:

            if not nome.strip():
                st.error("Informe o nome do atleta.")

            elif sexo == "Selecione":
                st.error("Selecione o sexo.")

            elif modalidade == "Selecione":
                st.error("Selecione a modalidade.")

            else:
                st.success("Dados preenchidos com sucesso!")


# Página de consulta
elif pagina == "Consulta de Atletas":

    st.title("Consulta de Atletas")

    st.write("Página para consultar atletas cadastrados.")


# Página de relatórios
elif pagina == "Relatórios":

    st.title("Relatórios")

    st.write("Página para visualizar os dados dos atletas.")
