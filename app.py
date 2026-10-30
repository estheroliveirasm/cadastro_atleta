
import streamlit as st
import pandas as pd

from database.banco import (
    criar_tabela,
    cadastrar_atleta,
    listar_atletas,
    contar_atletas
)


# Configurando a página
st.set_page_config(
    page_title="Sistema de Cadastro de Atletas",
    layout="wide"
)


# Criando a tabela caso ainda nao exista
criar_tabela()


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

    # Mostrando a quantidade de atletas cadastrados
    total = contar_atletas()

    st.metric("Atletas cadastrados", total)

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
            value=None,
            min_value=__import__("datetime").date(1920, 1, 1),
            max_value=__import__("datetime").date.today(),
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

                # Salvando os dados no banco
                cadastrar_atleta(
                    nome,
                    data_nascimento.strftime("%d/%m/%Y") if data_nascimento else None,
                    sexo,
                    modalidade,
                    equipe,
                    posicao,
                    telefone,
                    email
                )

                st.success("Atleta cadastrado com sucesso!")


# Página de consulta
elif pagina == "Consulta de Atletas":

    st.title("Consulta de Atletas")

    st.write("Aqui você pode visualizar os atletas cadastrados.")

    st.divider()

    # Buscando os atletas que estao salvos no banco
    atletas = listar_atletas()

    # Mostrando quantos atletas estao cadastrados
    total = contar_atletas()

    st.metric("Total de atletas", total)

    # Verificando se existe algum cadastro
    if atletas:

        st.subheader("Atletas cadastrados")

        # Criando os nomes das colunas
        colunas = [
            "ID",
            "Nome completo",
            "Data de nascimento",
            "Sexo",
            "Modalidade",
            "Equipe ou clube",
            "Posição",
            "Telefone",
            "E-mail"
        ]

        # Transformando os dados em uma tabela organizada
        tabela = pd.DataFrame(atletas, columns=colunas)

        # Mostrando a tabela na tela
        st.dataframe(
            tabela,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("Ainda não existem atletas cadastrados.")


# Página de relatórios
elif pagina == "Relatórios":

    st.title("Relatórios")

    st.write("Página para visualizar os dados dos atletas.")

    st.divider()

    # Buscando os atletas cadastrados
    atletas = listar_atletas()

    # Mostrando o total de atletas
    total = contar_atletas()

    st.metric("Total de atletas cadastrados", total)

    # Verificando se existem dados para os relatorios
    if atletas:

        # Organizando os dados em uma tabela
        colunas = [
            "ID",
            "Nome completo",
            "Data de nascimento",
            "Sexo",
            "Modalidade",
            "Equipe ou clube",
            "Posição",
            "Telefone",
            "E-mail"
        ]

        tabela = pd.DataFrame(atletas, columns=colunas)

        st.subheader("Atletas por modalidade")

        # Contando quantos atletas existem em cada modalidade
        quantidade = tabela["Modalidade"].value_counts()

        st.bar_chart(quantidade)

        st.subheader("Atletas por sexo")

        # Contando quantos atletas existem em cada categoria
        quantidade_sexo = tabela["Sexo"].value_counts()

        st.bar_chart(quantidade_sexo)

    else:

        st.info("Ainda não existem atletas cadastrados.")
