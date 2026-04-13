import streamlit as st
import pandas as pd
import time
import random

# Configuração da UI
st.set_page_config(page_title="EcoTrack - Protótipo IA", page_icon="🌱", layout="centered")

@st.cache_data
def carregar_dados():
    # Carregamos apenas as colunas essenciais para evitar lentidão e estouro de memória, visto que o arquivo é gigante (> 500MB)
    colunas = ['product_name', 'brands', 'ingredients_text', 'nutriscore_grade', 'ecoscore_grade', 'packaging', 'categories_tags']
    try:
        # A base do open food facts original é separada por tabulação ('\t')
        df = pd.read_csv('open-food-facts-sample.csv', sep='\t', usecols=colunas, low_memory=False)
        # Limpar os dados primários para melhorar a busca
        df = df.dropna(subset=['product_name'])
        return df
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo CSV: {e}")
        return pd.DataFrame()

# Lógica do "Mock GenAI" - Simulando a resposta generativa de uma IA
def mock_gen_ai_response(produto, perfil):
    time.sleep(2) # Simula o delay de resposta da API do LLM
    
    nome = str(produto['product_name'].values[0])
    nutri = str(produto['nutriscore_grade'].values[0]).upper()
    eco = str(produto['ecoscore_grade'].values[0]).upper()
    packaging = str(produto['packaging'].values[0]).lower()
    ingredientes = str(produto['ingredients_text'].values[0]).lower()
    
    # Textos Base do Relatório
    saudacao = f"✨ **Análise EcoTrack IA gerada para:** `{nome}`\n\n"
    
    # 1. Análise Nutricional Contextualizada
    if nutri in ['A', 'B']:
        insights_nutri = f"✅ **Nutrição Inteligente:** O NutriScore deste produto é excelente ({nutri}). Ele é uma ótima escolha para manter uma dieta balanceada."
    elif nutri in ['C']:
        insights_nutri = f"⚠️ **Atenção Moderada (NutriScore {nutri}):** Um produto mediano. Consuma com moderação."
    elif nutri in ['D', 'E']:
        insights_nutri = f"❌ **Alerta de Saúde (NutriScore {nutri}):** Identificamos alta probabilidade de ultraprocessamento, altos teores de açúcares, sódio ou gorduras saturadas."
    else:
        insights_nutri = "🔍 **Info Nutricional:** Os dados técnicos nutricionais (NutriScore) não foram totalmente fornecidos pelo fabricante, mas os ingredientes devem ser checados."

    # 2. Análise Ambiental Contextualizada (ESG)
    if eco in ['A', 'B']:
        insights_eco = f"🌍 **Impacto Ambiental Sustentável:** O EcoScore {eco} mostra que a pegada de carbono geral do produto é baixa!"
    elif eco in ['D', 'E']:
        insights_eco = f"🔥 **Alto Impacto (EcoScore {eco}):** Este produto tem uma grande pegada de carbono, possivelmente pela cadeia logística ou ingredientes intensivos (ex: Carne, Óleo de Palma)."
    else:
        insights_eco = f"🏭 **Sustentabilidade (EcoScore {eco}):** O impacto está na média ambiental, mas recomendados verificar opções alternativas na sua região."
        
    if "plastic" in packaging or "plastique" in packaging:
        insights_eco += " Atenção especial: Este produto utiliza embalagem **plástica não biodegradável**."

    # 3. Cruzamento com Perfil do Usuário (Internet of Behaviors)
    insights_perfil = ""
    if perfil == "Intolerante a Glúten" and ("blé" in ingredientes or "wheat" in ingredientes or "gluten" in ingredientes):
        insights_perfil = "\n🚨 **ALERTA CRÍTICO PARA SEU PERFIL:** Identificamos potenciais traços e ingredientes com GLÚTEN (como trigo/blé) nesta composição! Não recomendado para consumo."
    elif perfil == "Vegano" and ("lait" in ingredientes or "milk" in ingredientes or "oeuf" in ingredientes or "beurre" in ingredientes or "meat" in ingredientes):
        insights_perfil = "\n🚨 **ALERTA PARA SEU PERFIL (Vegano):** Este produto possui ingredientes de origem animal (ex: Leite, Ovos, etc.)."
    elif perfil == "Redução de Açúcar" and ("sucre" in ingredientes or "sugar" in ingredientes or "syrup" in ingredientes):
        insights_perfil = "\n📉 **DICA DO SEU PERFIL:** Em linha com seu objetivo de reduzir açúcar, evite este produto! Observamos adição direta de açúcares/xaropes na estrutura dos ingredientes."

    # 4. Alternativas Sugeridas (Generative Suggestion Mock)
    sugestoes = [
        "\n\n💡 **Recomendação da IA:** Sugerimos procurar por opções a granel no setor orgânico, pois em média apresentam Ecoscore A.",
        "\n\n💡 **Recomendação da IA:** Considere marcas locais de pequenos produtores para zerar a pegada de transporte logístico detectada no EcoScore atual.",
        "\n\n💡 **Recomendação da IA:** Que tal preparar um produto similar de forma caseira controlando a adição de açúcares e sódio? Substitua o ingrediente refinado."
    ]

    mock_resp = saudacao + insights_nutri + "\n\n" + insights_eco + insights_perfil + random.choice(sugestoes)
    return mock_resp

st.title("🌱 EcoTrack Scanner - Protótipo IA")
st.write("Demonstração da Inteligência Artificial lendo e cruzando os **Dados de Produto x Perfil do Usuário**.")

with st.spinner("Carregando o enorme banco de dados Open Food Facts (Aguente firme, o CSV tem centenas de milhares de linhas!)..."):
    df_produtos = carregar_dados()

if not df_produtos.empty:
    st.sidebar.header("👤 Perfil do Consumidor (IoB)")
    perfil_usuario = st.sidebar.selectbox("Selecione sua Restrição / Objetivo Alimentar:", 
                         ["Geral/Nenhum", "Intolerante a Glúten", "Vegano", "Redução de Açúcar"])
    
    st.sidebar.markdown("---")
    st.sidebar.write("**Dados Técnicos Carregados:**")
    st.sidebar.info(f"O Sistema detectou **{len(df_produtos):,} produtos** catalogados com sucesso.")

    st.subheader("🔍 Simule o Escaneamento do Produto")
    termo_busca = st.text_input("Digite o nome ou marca do produto (Ex: Pepsi, Pastille Vichy, Quiche, Donuts, 7Up):", placeholder="Exemplo: Pepsi")

    if st.button("Escanear Produto e Rodar Inteligência IA", use_container_width=True):
        if termo_busca:
            # Filtro Simples por nome (case insensitive)
            resultado = df_produtos[df_produtos['product_name'].str.contains(termo_busca, case=False, na=False)].head(1)
            
            if not resultado.empty:
                st.success(f"PRODUTO IDENTIFICADO: {resultado['product_name'].values[0]} | ({resultado['brands'].values[0]})")
                
                # Container para destacar resultado da IA
                st.markdown("### Processando Contexto e Extraindo Relatório...")
                
                with st.spinner("Conectando com o LLM (Mock) e enviando os dados JSON estruturados..."):
                    resposta_ia = mock_gen_ai_response(resultado, perfil_usuario)
                    
                st.info(resposta_ia)
                
                with st.expander("Ver JSON Bruto enviado para a IA (Para Fins Técnicos)"):
                    st.json({
                        "usuario": {
                            "perfil": perfil_usuario
                        },
                        "produto": {
                            "name": str(resultado['product_name'].values[0]),
                            "nutriscore": str(resultado['nutriscore_grade'].values[0]),
                            "ecoscore": str(resultado['ecoscore_grade'].values[0]),
                            "packaging": str(resultado['packaging'].values[0]),
                            "ingredients": str(resultado['ingredients_text'].values[0])
                        }
                    })
                    
            else:
                st.warning("Produto não encontrado na base de dados. Tente usar nomes reais como '7Up', 'Pepsi', 'Pastille Vichy'.")
        else:
            st.error("Por favor, digite o nome de um produto para escanear.")
else:
    st.error("Falha ao preparar a memória da base de dados. Verifique a existência do arquivo 'open-food-facts-sample.csv'.")
