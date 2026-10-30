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

if pagina == "Início":

    st.title("Sistema de Cadastro de Atletas")

    st.write(
        "Sistema para cadastro, consulta e gerenciamento "
        "de informações de atletas."
    )

    st.divider()

    st.subheader("Página inicial")

    st.info("Bem-vindo ao sistema!")


elif pagina == "Cadastro de Atletas":

    st.title("Cadastro de Atletas")

    st.write("Página para cadastrar novos atletas.")


elif pagina == "Consulta de Atletas":

    st.title("Consulta de Atletas")

    st.write("Página para consultar atletas cadastrados.")


elif pagina == "Relatórios":

    st.title("Relatórios")

    st.write("Página para visualizar os dados dos atletas.")