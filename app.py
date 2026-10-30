import streamlit as st
import pandas as pd

from datetime import date, datetime

from database.banco import (
    criar_tabela,
    cadastrar_atleta,
    listar_atletas,
    contar_atletas,
    editar_atleta,
    excluir_atleta
)

st.set_page_config(
    page_title="Gestão de Atletas",
    layout="wide"
)

st.markdown("""
    <style>
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"] {
            background-color: #F1F5F9 !important;
        }

        [data-testid="stAppViewContainer"] h1,
        [data-testid="stAppViewContainer"] h2,
        [data-testid="stAppViewContainer"] h3,
        [data-testid="stAppViewContainer"] h4 {
            color: #142B4A !important;
        }

        [data-testid="stAppViewContainer"] p,
        [data-testid="stAppViewContainer"] label {
            color: #334155;
        }

        [data-testid="stSidebar"] {
            background-color: #142B4A !important;
        }

        [data-testid="stSidebar"] * {
            color: #FFFFFF !important;
        }

        .cabecalho {
            background-color: #142B4A !important;
            padding: 28px;
            border-radius: 14px;
            margin-bottom: 20px;
        }

        .cabecalho h1 {
            color: #FFFFFF !important;
            margin-bottom: 5px;
        }

        .cabecalho p {
            color: #DCE8F5 !important;
            margin-bottom: 0;
        }

        .boas-vindas {
            background-color: #FFFFFF !important;
            padding: 24px;
            border-radius: 12px;
            border-left: 5px solid #42A5A0;
            margin-bottom: 25px;
        }

        .boas-vindas h3 {
            color: #142B4A !important;
            margin-top: 0;
        }

        .boas-vindas p {
            color: #64748B !important;
            margin-bottom: 0;
        }

        [data-testid="stMetric"] {
            background-color: #FFFFFF !important;
            padding: 20px;
            border-radius: 12px;
            border-left: 5px solid #42A5A0;
            box-shadow: 0 2px 8px rgba(20, 43, 74, 0.08);
        }

        [data-testid="stMetricLabel"] {
            color: #64748B !important;
        }

        [data-testid="stMetricValue"] {
            color: #142B4A !important;
        }

        [data-testid="stForm"] {
            background-color: #FFFFFF !important;
            padding: 25px;
            border-radius: 12px;
            border: 1px solid #E2E8F0;
        }

        .stButton > button,
        .stFormSubmitButton > button {
            background-color: #245B8F !important;
            color: #FFFFFF !important;
            border: none;
            border-radius: 8px;
            padding: 10px 18px;
            font-weight: 600;
        }

        .stButton > button:hover,
        .stFormSubmitButton > button:hover {
            background-color: #42A5A0 !important;
            color: #FFFFFF !important;
        }

        [data-testid="stDataFrame"] {
            border-radius: 10px;
            overflow: hidden;
        }

        hr {
            border-color: #CBD5E1;
        }

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }
    </style>
""", unsafe_allow_html=True)

criar_tabela()

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

def calcular_idade(data_nascimento):

    try:

        nascimento = datetime.strptime(
            data_nascimento,
            "%d/%m/%Y"
        ).date()

        hoje = date.today()

        idade = hoje.year - nascimento.year

        if (hoje.month, hoje.day) < (
            nascimento.month,
            nascimento.day
        ):
            idade -= 1

        return idade

    except (ValueError, TypeError):

        return None

def mostrar_mensagem(chave):

    if chave in st.session_state:

        st.success(st.session_state[chave])

        del st.session_state[chave]

def mostrar_cabecalho(titulo, descricao):

    st.markdown(f"""
        <div class="cabecalho">
            <h1>{titulo}</h1>
            <p>{descricao}</p>
        </div>
    """, unsafe_allow_html=True)

def navegar(pagina_destino):

    st.session_state["pagina_menu"] = pagina_destino

st.sidebar.markdown("""
    <div style="padding: 10px 0;">
        <h2 style="color: white !important; font-size: 23px;">
            GESTÃO DE ATLETAS
        </h2>
        <p style="color: #CBD5E1 !important; font-size: 13px;">
            Sistema de gerenciamento esportivo
        </p>
    </div>
""", unsafe_allow_html=True)

st.sidebar.divider()

if "pagina_menu" not in st.session_state:
    st.session_state["pagina_menu"] = "Início"

pagina = st.sidebar.radio(
    "MENU PRINCIPAL",
    [
        "Início",
        "Cadastro de Atletas",
        "Consulta de Atletas",
        "Editar Atleta",
        "Relatórios"
    ],
    key="pagina_menu"
)

st.sidebar.divider()

st.sidebar.caption("Sistema de Gestão Esportiva")

if pagina == "Início":

    mostrar_cabecalho(
        "Gestão de Atletas",
        "Gerencie cadastros e acompanhe informações esportivas em um só lugar."
    )

    st.markdown("""
        <div class="boas-vindas">
            <h3>Bem-vindo ao Gestão de Atletas!</h3>
            <p>
                Este sistema foi desenvolvido para facilitar o cadastro,
                a organização e o acompanhamento de atletas.
                Consulte informações, gerencie equipes e acompanhe
                indicadores esportivos em um só lugar.
            </p>
        </div>
    """, unsafe_allow_html=True)

    atletas = listar_atletas()

    tabela = criar_dataframe(atletas)

    total = contar_atletas()

    modalidades_cadastradas = (
        tabela["Modalidade"].nunique()
        if not tabela.empty else 0
    )

    equipes_cadastradas = (
        tabela["Equipe ou clube"].replace("", pd.NA).dropna().nunique()
        if not tabela.empty else 0
    )

    st.subheader("Visão geral")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total de atletas", total)

    with col2:
        st.metric("Modalidades", modalidades_cadastradas)

    with col3:
        st.metric("Equipes e clubes", equipes_cadastradas)

    st.divider()

    col1, col2 = st.columns([1.4, 1])

    with col1:

        st.subheader("Atletas por modalidade")

        if atletas:

            quantidade_modalidade = tabela["Modalidade"].value_counts()

            st.bar_chart(
                quantidade_modalidade,
                color="#245B8F"
            )

        else:

            st.info("Os gráficos serão exibidos após os primeiros cadastros.")

    with col2:

        st.subheader("Acesso rápido")

        st.write("Acesse as principais funcionalidades.")

        st.button(
            "Cadastrar atleta",
            use_container_width=True,
            on_click=navegar,
            args=("Cadastro de Atletas",)
        )

        st.button(
            "Consultar atletas",
            use_container_width=True,
            on_click=navegar,
            args=("Consulta de Atletas",)
        )

    st.divider()

    st.subheader("Atletas cadastrados recentemente")

    if atletas:

        tabela_recente = tabela.sort_values(
            by="ID",
            ascending=False
        ).head(5)

        st.dataframe(
            tabela_recente[
                ["ID", "Nome completo", "Modalidade", "Equipe ou clube"]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("Ainda não existem atletas cadastrados.")


elif pagina == "Cadastro de Atletas":

    mostrar_cabecalho(
        "Cadastro de Atletas",
        "Adicione novos atletas e registre suas informações."
    )

    with st.form("formulario_atleta"):

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

        st.subheader("Informações esportivas")

        modalidade = st.selectbox(
            "Modalidade esportiva",
            ["Selecione"] + modalidades
        )

        equipe = st.text_input("Equipe ou clube")

        posicao = st.text_input("Posição ou função")

        st.divider()

        st.subheader("Informações de contato")

        telefone = st.text_input("Telefone")

        email = st.text_input("E-mail")

        cadastrar = st.form_submit_button(
            "Cadastrar atleta",
            use_container_width=True
        )

        if cadastrar:

            if not nome.strip():

                st.error("Informe o nome do atleta.")

            elif data_nascimento is None:

                st.error("Informe a data de nascimento.")

            elif sexo == "Selecione":

                st.error("Selecione o sexo.")

            elif modalidade == "Selecione":

                st.error("Selecione a modalidade.")

            elif email.strip() and (
                "@" not in email or "." not in email.split("@")[-1]
            ):

                st.error("Informe um e-mail válido.")

            else:

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

                st.session_state["feedback_cadastro"] = (
                    "Atleta cadastrado com sucesso!"
                )

                st.rerun()

    # A mensagem aparece abaixo do formulario
    mostrar_mensagem("feedback_cadastro")


elif pagina == "Consulta de Atletas":

    mostrar_cabecalho(
        "Consulta de Atletas",
        "Pesquise, filtre e visualize os atletas cadastrados."
    )

    atletas = listar_atletas()

    st.metric("Total de atletas cadastrados", len(atletas))

    if atletas:

        tabela = criar_dataframe(atletas)

        st.subheader("Filtros de pesquisa")

        pesquisa = st.text_input(
            "Pesquisar pelo nome",
            placeholder="Digite o nome do atleta..."
        )

        col1, col2 = st.columns(2)

        modalidades_disponiveis = [
            "Todas"
        ] + sorted(tabela["Modalidade"].dropna().unique().tolist())

        sexos_disponiveis = [
            "Todos"
        ] + sorted(tabela["Sexo"].dropna().unique().tolist())

        with col1:

            filtro_modalidade = st.selectbox(
                "Modalidade",
                modalidades_disponiveis
            )

        with col2:

            filtro_sexo = st.selectbox(
                "Sexo",
                sexos_disponiveis
            )

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

        st.subheader("Resultados da pesquisa")

        st.dataframe(
            tabela_filtrada,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            f"Resultados encontrados: {len(tabela_filtrada)}"
        )

        if tabela_filtrada.empty:

            st.warning("Nenhum atleta encontrado com esses filtros.")

    else:

        st.info("Ainda não existem atletas cadastrados.")


elif pagina == "Editar Atleta":

    mostrar_cabecalho(
        "Gerenciar Atletas",
        "Altere informações ou remova cadastros existentes."
    )

    mostrar_mensagem("feedback_edicao")
    mostrar_mensagem("feedback_exclusao")

    atletas = listar_atletas()

    if atletas:

        atleta_selecionado = st.selectbox(
            "Selecione o atleta",
            atletas,
            format_func=lambda atleta: (
                f"{atleta[1]} - ID: {atleta[0]}"
            )
        )

        id_atleta = atleta_selecionado[0]

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

        st.divider()

        st.subheader("Alterar informações")

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

            if salvar:

                if not nome.strip():

                    st.error("O nome do atleta é obrigatório.")

                elif email.strip() and (
                    "@" not in email or "." not in email.split("@")[-1]
                ):

                    st.error("Informe um e-mail válido.")

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

                    st.session_state["feedback_edicao"] = (
                        "Dados do atleta atualizados com sucesso!"
                    )

                    st.rerun()

        st.divider()

        st.subheader("Excluir atleta")

        st.warning(
            f"Cadastro selecionado: {nome_atual}"
        )

        confirmar = st.checkbox(
            "Confirmo que desejo excluir este atleta.",
            key=f"confirmar_exclusao_{id_atleta}"
        )

        if st.button(
            "Excluir atleta",
            disabled=not confirmar,
            type="secondary",
            use_container_width=True
        ):

            excluir_atleta(id_atleta)

            st.session_state["feedback_exclusao"] = (
                "Atleta excluído com sucesso!"
            )

            st.rerun()

    else:

        st.info("Não existem atletas cadastrados para editar ou excluir.")


elif pagina == "Relatórios":

    mostrar_cabecalho(
        "Relatórios",
        "Acompanhe indicadores e analise o perfil dos atletas cadastrados."
    )

    atletas = listar_atletas()

    if atletas:

        tabela = criar_dataframe(atletas)

        tabela["Idade"] = tabela["Data de nascimento"].apply(
            calcular_idade
        )

        tabela["Equipe ou clube"] = (
            tabela["Equipe ou clube"]
            .replace("", "Não informada")
            .fillna("Não informada")
        )

        st.subheader("Indicadores gerais")

        col1, col2, col3, col4 = st.columns(4)

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

            total_equipes = (
                tabela["Equipe ou clube"]
                .replace("Não informada", pd.NA)
                .dropna()
                .nunique()
            )

            st.metric(
                "Equipes e clubes",
                total_equipes
            )

        with col4:

            idades_validas = tabela["Idade"].dropna()

            idade_media = (
                round(idades_validas.mean(), 1)
                if not idades_validas.empty else 0
            )

            st.metric(
                "Idade média",
                f"{idade_media} anos"
            )

        st.divider()

        st.subheader("Distribuição dos atletas")

        col1, col2 = st.columns(2)

        with col1:

            st.write("**Atletas por modalidade**")

            quantidade_modalidade = tabela["Modalidade"].value_counts()

            st.bar_chart(
                quantidade_modalidade,
                color="#245B8F"
            )

        with col2:

            st.write("**Atletas por sexo**")

            quantidade_sexo = tabela["Sexo"].value_counts()

            st.bar_chart(
                quantidade_sexo,
                color="#42A5A0"
            )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            st.write("**Atletas por equipe ou clube**")

            quantidade_equipes = tabela["Equipe ou clube"].value_counts()

            st.bar_chart(
                quantidade_equipes,
                color="#245B8F"
            )

        with col2:

            st.write("**Distribuição por faixa etária**")

            idades_validas = tabela["Idade"].dropna()

            if not idades_validas.empty:

                faixas = pd.cut(
                    idades_validas,
                    bins=[0, 12, 17, 23, 30, 100],
                    labels=[
                        "Até 12 anos",
                        "13 a 17 anos",
                        "18 a 23 anos",
                        "24 a 30 anos",
                        "Acima de 30 anos"
                    ]
                )

                quantidade_faixas = (
                    faixas.value_counts()
                    .sort_index()
                )

                st.bar_chart(
                    quantidade_faixas,
                    color="#42A5A0"
                )

            else:

                st.info(
                    "Não existem datas de nascimento válidas para calcular as idades."
                )

        st.divider()

        st.subheader("Dados dos atletas")

        st.dataframe(
            tabela,
            use_container_width=True,
            hide_index=True
        )

        arquivo_csv = tabela.to_csv(
            index=False,
            sep=";",
            encoding="utf-8-sig"
        ).encode("utf-8-sig")

        st.download_button(
            label="Exportar relatório em CSV",
            data=arquivo_csv,
            file_name="relatorio_atletas.csv",
            mime="text/csv",
            use_container_width=True
        )

    else:

        st.info(
            "Ainda não existem atletas cadastrados para gerar relatórios."
        )