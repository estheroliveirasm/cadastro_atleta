
# Importando as bibliotecas
import streamlit as st
import pandas as pd

from datetime import date, datetime

# Importando as funcoes do banco de dados
from database.banco import (
    criar_tabela,
    cadastrar_atleta,
    listar_atletas,
    contar_atletas,
    editar_atleta,
    excluir_atleta
)


# Configurando a pagina
st.set_page_config(
    page_title="Sistema de Cadastro de Atletas",
    layout="wide"
)


# Criando a tabela caso ainda nao exista
criar_tabela()


# Definindo as opcoes do sistema
modalidades = [
    "Vôlei",
    "Futebol",
    "Basquete",
    "Handebol",
    "Natação",
    "Atletismo",
    "Outra"
]

sexos = [
    "Feminino",
    "Masculino",
    "Outro",
    "Prefiro não informar"
]


# Organizando os dados em uma tabela
def criar_dataframe(atletas):

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

    return pd.DataFrame(atletas, columns=colunas)


# Criando o menu lateral
st.sidebar.title("Sistema de Atletas")

pagina = st.sidebar.radio(
    "Navegação",
    [
        "Início",
        "Cadastro de Atletas",
        "Consulta de Atletas",
        "Editar Atleta",
        "Relatórios"
    ]
)


# Mostrando mensagens de sucesso depois das alteracoes
if "mensagem" in st.session_state:

    st.success(st.session_state["mensagem"])

    del st.session_state["mensagem"]


# Página inicial
if pagina == "Início":

    st.title("Sistema de Cadastro de Atletas")

    st.write(
        "Sistema para cadastro, consulta e gerenciamento "
        "de informações de atletas."
    )

    st.divider()

    # Buscando a quantidade de atletas cadastrados
    total = contar_atletas()

    atletas = listar_atletas()

    # Mostrando os principais indicadores
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total de atletas", total)

    with col2:
        modalidades_cadastradas = len(
            set(atleta[4] for atleta in atletas)
        )

        st.metric("Modalidades cadastradas", modalidades_cadastradas)

    st.divider()

    st.subheader("Página inicial")

    st.info("Bem-vindo ao sistema de gerenciamento de atletas!")

    st.write(
        "Utilize o menu lateral para cadastrar, consultar, "
        "editar e visualizar os dados dos atletas."
    )


# Página de cadastro
elif pagina == "Cadastro de Atletas":

    st.title("Cadastro de Atletas")

    st.write("Preencha os dados abaixo para cadastrar um atleta.")

    st.divider()

    # Criando o formulario de cadastro
    with st.form("formulario_atleta"):

        # Dados pessoais
        st.subheader("Dados pessoais")

        nome = st.text_input("Nome completo")

        data_nascimento = st.date_input(
            "Data de nascimento",
            value=None,
            min_value=date(1920, 1, 1),
            max_value=date.today(),
            format="DD/MM/YYYY"
        )

        sexo = st.selectbox(
            "Sexo",
            ["Selecione"] + sexos
        )

        st.divider()

        # Dados esportivos
        st.subheader("Informações esportivas")

        modalidade = st.selectbox(
            "Modalidade esportiva",
            ["Selecione"] + modalidades
        )

        equipe = st.text_input("Equipe ou clube")

        posicao = st.text_input("Posição ou função")

        st.divider()

        # Dados de contato
        st.subheader("Contato")

        telefone = st.text_input("Telefone")

        email = st.text_input("E-mail")

        # Botao para cadastrar
        cadastrar = st.form_submit_button(
            "Cadastrar atleta",
            use_container_width=True
        )

        # Verificando os campos obrigatorios
        if cadastrar:

            if not nome.strip():
                st.error("Informe o nome do atleta.")

            elif data_nascimento is None:
                st.error("Informe a data de nascimento.")

            elif sexo == "Selecione":
                st.error("Selecione o sexo.")

            elif modalidade == "Selecione":
                st.error("Selecione a modalidade.")

            else:

                # Salvando os dados no banco
                cadastrar_atleta(
                    nome.strip(),
                    data_nascimento.strftime("%d/%m/%Y"),
                    sexo,
                    modalidade,
                    equipe.strip(),
                    posicao.strip(),
                    telefone.strip(),
                    email.strip()
                )

                st.session_state["mensagem"] = (
                    "Atleta cadastrado com sucesso!"
                )

                st.rerun()


# Página de consulta
elif pagina == "Consulta de Atletas":

    st.title("Consulta de Atletas")

    st.write("Pesquise e visualize os atletas cadastrados.")

    st.divider()

    # Buscando os atletas no banco
    atletas = listar_atletas()

    st.metric("Total de atletas cadastrados", len(atletas))

    if atletas:

        tabela = criar_dataframe(atletas)

        st.subheader("Pesquisar atletas")

        # Campo para pesquisar pelo nome
        pesquisa = st.text_input(
            "Digite o nome do atleta"
        )

        # Criando os filtros
        col1, col2 = st.columns(2)

        modalidades_disponiveis = [
            "Todas"
        ] + sorted(tabela["Modalidade"].dropna().unique().tolist())

        sexos_disponiveis = [
            "Todos"
        ] + sorted(tabela["Sexo"].dropna().unique().tolist())

        with col1:

            filtro_modalidade = st.selectbox(
                "Filtrar por modalidade",
                modalidades_disponiveis
            )

        with col2:

            filtro_sexo = st.selectbox(
                "Filtrar por sexo",
                sexos_disponiveis
            )

        # Aplicando os filtros na tabela
        tabela_filtrada = tabela.copy()

        if pesquisa.strip():

            tabela_filtrada = tabela_filtrada[
                tabela_filtrada["Nome completo"].str.contains(
                    pesquisa,
                    case=False,
                    na=False
                )
            ]

        if filtro_modalidade != "Todas":

            tabela_filtrada = tabela_filtrada[
                tabela_filtrada["Modalidade"] == filtro_modalidade
            ]

        if filtro_sexo != "Todos":

            tabela_filtrada = tabela_filtrada[
                tabela_filtrada["Sexo"] == filtro_sexo
            ]

        st.divider()

        st.subheader("Atletas encontrados")

        # Mostrando os resultados
        st.dataframe(
            tabela_filtrada,
            use_container_width=True,
            hide_index=True
        )

        st.write(
            f"Resultados encontrados: {len(tabela_filtrada)}"
        )

        if tabela_filtrada.empty:

            st.warning("Nenhum atleta encontrado com esses filtros.")

    else:

        st.info("Ainda não existem atletas cadastrados.")


# Página de edição
elif pagina == "Editar Atleta":

    st.title("Editar ou excluir atleta")

    st.write("Selecione um atleta para alterar ou excluir seus dados.")

    st.divider()

    atletas = listar_atletas()

    if atletas:

        # Escolhendo qual atleta sera alterado
        atleta_selecionado = st.selectbox(
            "Selecione o atleta",
            atletas,
            format_func=lambda atleta: (
                f"{atleta[1]} - ID: {atleta[0]}"
            )
        )

        id_atleta = atleta_selecionado[0]

        # Recuperando os dados atuais
        nome_atual = atleta_selecionado[1]

        try:
            data_atual = datetime.strptime(
                atleta_selecionado[2],
                "%d/%m/%Y"
            ).date()
        except (ValueError, TypeError):
            data_atual = date.today()

        sexo_atual = atleta_selecionado[3]

        modalidade_atual = atleta_selecionado[4]

        equipe_atual = atleta_selecionado[5] or ""

        posicao_atual = atleta_selecionado[6] or ""

        telefone_atual = atleta_selecionado[7] or ""

        email_atual = atleta_selecionado[8] or ""

        st.subheader("Alterar informações")

        # Criando o formulario de edicao
        with st.form("formulario_edicao"):

            nome = st.text_input(
                "Nome completo",
                value=nome_atual
            )

            data_nascimento = st.date_input(
                "Data de nascimento",
                value=data_atual,
                min_value=date(1920, 1, 1),
                max_value=date.today(),
                format="DD/MM/YYYY"
            )

            opcoes_sexo = sexos.copy()

            if sexo_atual not in opcoes_sexo:
                opcoes_sexo.append(sexo_atual)

            sexo = st.selectbox(
                "Sexo",
                opcoes_sexo,
                index=opcoes_sexo.index(sexo_atual)
            )

            opcoes_modalidade = modalidades.copy()

            if modalidade_atual not in opcoes_modalidade:
                opcoes_modalidade.append(modalidade_atual)

            modalidade = st.selectbox(
                "Modalidade",
                opcoes_modalidade,
                index=opcoes_modalidade.index(modalidade_atual)
            )

            equipe = st.text_input(
                "Equipe ou clube",
                value=equipe_atual
            )

            posicao = st.text_input(
                "Posição ou função",
                value=posicao_atual
            )

            telefone = st.text_input(
                "Telefone",
                value=telefone_atual
            )

            email = st.text_input(
                "E-mail",
                value=email_atual
            )

            salvar = st.form_submit_button(
                "Salvar alterações",
                use_container_width=True
            )

            # Salvando as alteracoes
            if salvar:

                if not nome.strip():

                    st.error("O nome do atleta é obrigatório.")

                else:

                    editar_atleta(
                        id_atleta,
                        nome.strip(),
                        data_nascimento.strftime("%d/%m/%Y"),
                        sexo,
                        modalidade,
                        equipe.strip(),
                        posicao.strip(),
                        telefone.strip(),
                        email.strip()
                    )

                    st.session_state["mensagem"] = (
                        "Dados do atleta atualizados com sucesso!"
                    )

                    st.rerun()

        st.divider()

        st.subheader("Excluir atleta")

        st.warning(
            f"Você está selecionando o cadastro de {nome_atual}."
        )

        # Pedindo confirmacao antes de excluir
        confirmar = st.checkbox(
            "Confirmo que desejo excluir este atleta.",
            key="confirmar_exclusao"
        )

        if st.button(
            "Excluir atleta",
            disabled=not confirmar,
            type="secondary"
        ):

            excluir_atleta(id_atleta)

            st.session_state["mensagem"] = (
                "Atleta excluído com sucesso!"
            )

            st.rerun()

    else:

        st.info("Não existem atletas cadastrados para editar ou excluir.")


# Página de relatórios
elif pagina == "Relatórios":

    st.title("Relatórios")

    st.write("Visualize informações e estatísticas dos atletas.")

    st.divider()

    atletas = listar_atletas()

    if atletas:

        tabela = criar_dataframe(atletas)

        # Mostrando os indicadores
        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Total de atletas",
                len(tabela)
            )

        with col2:

            st.metric(
                "Modalidades",
                tabela["Modalidade"].nunique()
            )

        with col3:

            st.metric(
                "Equipes",
                tabela["Equipe ou clube"].replace("", pd.NA).nunique()
            )

        st.divider()

        # Grafico de atletas por modalidade
        st.subheader("Atletas por modalidade")

        quantidade_modalidade = (
            tabela["Modalidade"]
            .value_counts()
        )

        st.bar_chart(quantidade_modalidade)

        # Grafico de atletas por sexo
        st.subheader("Atletas por sexo")

        quantidade_sexo = tabela["Sexo"].value_counts()

        st.bar_chart(quantidade_sexo)

        # Mostrando os dados completos
        st.subheader("Resumo dos cadastros")

        st.dataframe(
            tabela,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("Ainda não existem atletas cadastrados para gerar relatórios.")
