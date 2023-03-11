import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
# Options complémentaires
from st_aggrid.grid_options_builder import GridOptionsBuilder
# Saisies en JavaScript : condition sur cellule
from st_aggrid.shared import JsCode
import plotly.express as px

def func_tab1(df, year):
    # Données à alimenter pour la DF sur les postes de bilan
    
    # FR
    account1 = int(df.loc[
                (df['POSTE 2'].astype('str').str.contains('^FR$')) & 
                (df['Millesime'].astype('str').str.contains(year)),
                ['N']].squeeze())
    var1 = (df.loc[
                (df['POSTE 2'].astype('str').str.contains('^FR$')) & 
                (df['Millesime'].astype('str').str.contains(year)),
                ['VAR']].squeeze())*100
    
    # BFR
    account2 = int(df.loc[
                (df['POSTE 2'].astype('str').str.contains('^BFR$')) & 
                (df['Millesime'].astype('str').str.contains(year)),
                ['N']].squeeze())
    var2 = (df.loc[
                (df['POSTE 2'].astype('str').str.contains('^BFR$')) & 
                (df['Millesime'].astype('str').str.contains(year)),
                ['VAR']].squeeze())*100
    
    # CREANCES
    account3 = int(df.loc[
                (df['POSTE 2'].astype('str').str.contains('^CREANCES$')) & 
                (df['Millesime'].astype('str').str.contains(year)),
                ['N']].squeeze())
    var3 = (df.loc[
                (df['POSTE 2'].astype('str').str.contains('^CREANCES$')) & 
                (df['Millesime'].astype('str').str.contains(year)),
                ['VAR']].squeeze())*100
    
    # DETTES
    account4 = int(df.loc[
                (df['POSTE 2'].astype('str').str.contains('^DETTES$')) & 
                (df['Millesime'].astype('str').str.contains(year)),
                ['N']].squeeze())
    var4 = (df.loc[
                (df['POSTE 2'].astype('str').str.contains('^DETTES$')) & 
                (df['Millesime'].astype('str').str.contains(year)),
                ['VAR']].squeeze())*100
    
    # TRESORERIE
    account5 = int(df.loc[
                (df['POSTE 2'].astype('str').str.contains('^TRESORERIE$')) & 
                (df['Millesime'].astype('str').str.contains(year)),
                ['N']].squeeze())
    var5 = (df.loc[
                (df['POSTE 2'].astype('str').str.contains('^TRESORERIE$')) & 
                (df['Millesime'].astype('str').str.contains(year)),
                ['VAR']].squeeze())*100
    
    # Chargement de la DF
    tab1 = pd.DataFrame({
        'BILAN':[
            'FONDS DE ROULEMENT', 'BESOIN EN FONDS DE ROULEMENT',
            'CRÉANCES CLIENTS', 'DETTES FOURNISSEURS', 'TRÉSORERIE'],
        'MONTANT':[f'{account1:,}', f'{account2:,}', 
                    f'{account3:,}', f'{account4:,}', f'{account5:,}'],
        'VAR N-1 / N':[f'{round(var1, 2)} %', f'{round(var2, 2)} %',
                       f'{round(var3, 2)} %', f'{round(var4, 2)} %',
                       f'{round(var5, 2)} %']})
    
    return tab1

def func_tab2(df, year):
    # Données à alimenter pour la DF sur les postes du compte de résultat
    
    # VA
    account1 = int(df.loc[
                (df['POSTE 2'].astype('str').str.contains('^VA$')) & 
                (df['Millesime'].astype('str').str.contains(year)),
                ['N']].squeeze())
    var1 = (df.loc[
                (df['POSTE 2'].astype('str').str.contains('^VA$')) & 
                (df['Millesime'].astype('str').str.contains(year)),
                ['VAR']].squeeze())*100
    
    # EBITDA
    account2 = int(df.loc[
                (df['POSTE 2'].astype('str').str.contains('^EBITDA$')) & 
                (df['Millesime'].astype('str').str.contains(year)),
                ['N']].squeeze())
    var2 = (df.loc[
                (df['POSTE 2'].astype('str').str.contains('^EBITDA$')) & 
                (df['Millesime'].astype('str').str.contains(year)),
                ['VAR']].squeeze())*100
    
    # RESULTAT EXPLOITATION
    account3 = int(df.loc[
                (df['POSTE 2'].astype('str').str.contains('^RESULTAT EXPLOITATION$')) & 
                (df['Millesime'].astype('str').str.contains(year)),
                ['N']].squeeze())
    var3 = (df.loc[
                (df['POSTE 2'].astype('str').str.contains('^RESULTAT EXPLOITATION$')) & 
                (df['Millesime'].astype('str').str.contains(year)),
                ['VAR']].squeeze())*100
    
    # RESULTAT
    account4 = int(df.loc[
                (df['POSTE 2'].astype('str').str.contains('^RESULTAT$')) & 
                (df['Millesime'].astype('str').str.contains(year)),
                ['N']].squeeze())
    var4 = (df.loc[
                (df['POSTE 2'].astype('str').str.contains('^RESULTAT$')) & 
                (df['Millesime'].astype('str').str.contains(year)),
                ['VAR']].squeeze())*100
    
    # CAF
    account5 = int(df.loc[
                (df['POSTE 2'].astype('str').str.contains('^CAF$')) & 
                (df['Millesime'].astype('str').str.contains(year)),
                ['N']].squeeze())
    var5 = (df.loc[
                (df['POSTE 2'].astype('str').str.contains('^CAF$')) & 
                (df['Millesime'].astype('str').str.contains(year)),
                ['VAR']].squeeze())*100
    
    # Chargement de la DF
    tab2 = pd.DataFrame({
        'COMPTE DE RÉSULTAT':[
            'VALEUR AJOUTÉE', 'EBITDA',"RÉSULTAT D'EXPLOITATION", 
            'RÉSULTAT COMPTABLE', 'CAF'],
        'MONTANT':[f'{account1:,}', f'{account2:,}', 
                    f'{account3:,}', f'{account4:,}', f'{account5:,}'],
        'VAR N-1 / N':[f'{round(var1, 2)} %', f'{round(var2, 2)} %',
                       f'{round(var3, 2)} %', f'{round(var4, 2)} %',
                       f'{round(var5, 2)} %']})
    
    return tab2

def func_graph1(df, year):
    # Graphique sur l'évolution des postes de charges
    
    # 60 - ACHATS
    try:
        account1 = int(df.loc[
                    (df['POSTE 2'].astype('str').str.contains('^60 - ACHATS$')) & 
                    (df['Millesime'].astype('str').str.contains(year)),
                    ['N']].squeeze())
    except TypeError:
        account1 = 0
    try:
        previous1 = int(df.loc[
                    (df['POSTE 2'].astype('str').str.contains('^60 - ACHATS$')) & 
                    (df['Millesime'].astype('str').str.contains(year)),
                    ['N-1']].squeeze())
    except TypeError:
        previous1 = 0
    
    
    # 61/62 - SERV. EXTERIEURS
    try:
        account2 = int(df.loc[
                    (df['POSTE 2'].astype('str').str.contains(
                        '^61/62 - SERV. EXTERIEURS$')) & 
                    (df['Millesime'].astype('str').str.contains(year)),
                    ['N']].squeeze())
    except TypeError:
        account2 = 0
    try:
        previous2 = int(df.loc[
                    (df['POSTE 2'].astype('str').str.contains(
                        '^61/62 - SERV. EXTERIEURS$')) & 
                    (df['Millesime'].astype('str').str.contains(year)),
                    ['N-1']].squeeze())
    except TypeError:
        previous2 = 0
    
    # 63 - IMPOTS & TAXES
    try:
        account3 = int(df.loc[
                    (df['POSTE 2'].astype('str').str.contains(
                        '^63 - IMPOTS & TAXES$')) & 
                    (df['Millesime'].astype('str').str.contains(year)),
                    ['N']].squeeze())
    except TypeError:
        account3 = 0
    try:
        previous3 = int(df.loc[
                    (df['POSTE 2'].astype('str').str.contains(
                        '^63 - IMPOTS & TAXES$')) & 
                    (df['Millesime'].astype('str').str.contains(year)),
                    ['N-1']].squeeze())
    except TypeError:
        previous3 = 0
    
    # 64 - PERSONNEL
    try:
        account4 = int(df.loc[
                    (df['POSTE 2'].astype('str').str.contains(
                        '^64 - PERSONNEL$')) & 
                    (df['Millesime'].astype('str').str.contains(year)),
                    ['N']].squeeze())
    except TypeError:
        account4 = 0
    try:
        previous4 = int(df.loc[
                    (df['POSTE 2'].astype('str').str.contains(
                        '^64 - PERSONNEL$')) & 
                    (df['Millesime'].astype('str').str.contains(year)),
                    ['N-1']].squeeze())
    except TypeError:
        previous4 = 0
    
    # 66 - FINANCIER
    try:
        account5 = int(df.loc[
                    (df['POSTE 2'].astype('str').str.contains(
                        '^66 - FINANCIER$')) & 
                    (df['Millesime'].astype('str').str.contains(year)),
                    ['N']].squeeze())
    except TypeError:
        account5 = 0
    try:
        previous5 = int(df.loc[
                    (df['POSTE 2'].astype('str').str.contains(
                        '^66 - FINANCIER$')) & 
                    (df['Millesime'].astype('str').str.contains(year)),
                    ['N-1']].squeeze())
    except TypeError:
        previous5 = 0
    
    # 67 - EXCEPTIONNEL
    try:
        account6 = int(df.loc[
                    (df['POSTE 2'].astype('str').str.contains(
                        '^67 - EXCEPTIONNEL$')) & 
                    (df['Millesime'].astype('str').str.contains(year)),
                    ['N']].squeeze())
    except TypeError:
        account6 = 0
    try:
        previous6 = int(df.loc[
                    (df['POSTE 2'].astype('str').str.contains(
                        '^67 - EXCEPTIONNEL$')) & 
                    (df['Millesime'].astype('str').str.contains(year)),
                    ['N-1']].squeeze())
    except TypeError:
        previous6 = 0
    
    # DF sur les postes de charges
    expenses_df = pd.DataFrame({
        'POSTE':['60 - ACHATS', '61/62 - SERV. EXTÉRIEURS',
                    '63 - IMPÔTS & TAXES', '64 - PERSONNEL',
                    '66 - FINANCIER', '67 - EXCEPTIONNEL'],
        'N-1':[previous1, previous2, previous3, previous4, previous5, previous6],
        'N':[account1, account2, account3, account4, account5, account6]
    })
    
    return expenses_df

def func_graph2(df, year):
    # Graphique sur l'évolution des marges SIG
    
    # 60 - ACHATS
    try:
        var1 = (df.loc[
                    (df['POSTE 2'].astype('str').str.contains('^60 - ACHATS$')) & 
                    (df['Millesime'].astype('str').str.contains(year)),
                    ['VAR']].squeeze())*100
    except TypeError:
        var1 = 0
    
    # 61/62 - SERV. EXTERIEURS
    try:
        var2 = (df.loc[
                    (df['POSTE 2'].astype('str').str.contains(
                        '^61/62 - SERV. EXTERIEURS$')) & 
                    (df['Millesime'].astype('str').str.contains(year)),
                    ['VAR']].squeeze())*100
    except TypeError:
        var2 = 0
    
    # 63 - IMPOTS & TAXES
    try:
        var3 = (df.loc[
                    (df['POSTE 2'].astype('str').str.contains(
                        '^63 - IMPOTS & TAXES$')) & 
                    (df['Millesime'].astype('str').str.contains(year)),
                    ['VAR']].squeeze())*100
    except TypeError:
        var3 = 0
    
    # 64 - PERSONNEL
    try:
        var4 = (df.loc[
                    (df['POSTE 2'].astype('str').str.contains(
                        '^64 - PERSONNEL$')) & 
                    (df['Millesime'].astype('str').str.contains(year)),
                    ['VAR']].squeeze())*100
    except TypeError:
        var4 = 0
    
    # 66 - FINANCIER
    try:
        var5 = (df.loc[
                    (df['POSTE 2'].astype('str').str.contains(
                        '^66 - FINANCIER$')) & 
                    (df['Millesime'].astype('str').str.contains(year)),
                    ['VAR']].squeeze())*100
    except TypeError:
        var5 = 0
    
    # 67 - EXCEPTIONNEL
    try:
        var6 = (df.loc[
                    (df['POSTE 2'].astype('str').str.contains(
                        '^67 - EXCEPTIONNEL$')) & 
                    (df['Millesime'].astype('str').str.contains(year)),
                    ['VAR']].squeeze())*100
    except TypeError:
        var6 = 0
        
    # CHIFFRE D'AFFAIRES
    try:
        var7 = (df.loc[
                    (df['POSTE 2'].astype('str').str.contains('^CAHT$')) & 
                    (df['Millesime'].astype('str').str.contains(year)),
                    ['VAR']].squeeze())*100
    except TypeError:
        var7 = 0
    
    # DF sur les postes de SIG
    analysis_df = pd.DataFrame({
        'POSTE':['60 - ACHATS', '61/62 - SERV. EXTÉRIEURS',
                    '63 - IMPÔTS & TAXES', '64 - PERSONNEL',
                    '66 - FINANCIER', '67 - EXCEPTIONNEL', "CHIFFRE D'AFFAIRES"],
        'VAR':[f'{round(var1, 2)} %', f'{round(var2, 2)} %', 
               f'{round(var3, 2)} %', f'{round(var4, 2)} %',
               f'{round(var5, 2)} %', f'{round(var6, 2)} %',
               f'{round(var7, 2)} %']})
    
    return analysis_df

def application():
    
    #region Config fenêtre principale et composants chargement fichier
      
    # Affichage par défaut plein écran
    st.set_page_config(page_title="Analyse financière", layout="wide")
    
    # Espacements avec la fenêtre
    st.markdown("""
    <style>
            .block-container {
                padding-top: 1rem;
                padding-bottom: 0rem;
                padding-left: 5rem;
                padding-right: 5rem;
            }
    </style>
    """, unsafe_allow_html=True)
    
    # Titre de la page : centré, couleur 'bleu', format titre
    st.markdown(
        "<h3 style='text-align: center; color: #fcfcfc;'>ANALYSE FINANCIÈRE</h3>", 
        unsafe_allow_html=True # HTML par défaut
        )
    
    col1, col2, col3 = st.columns([1.5, 3, 0.5])
    with col1:
        # Composant pour charger le fichier
        files_uploader = st.file_uploader(
                'Fichier AnalyseFinPluri.xlsx à charger', 
                type='xlsx')
        
    with col3:
        # Attribution d'une variable pour màj lors du chargement du fichier :
        # présence d'un menu déroulant
        selected_period = st.empty()
    
    #endregion Config fenêtre principale et composants chargement fichier
    
    #region Chargement du fichier Excel et périodes récupérées
    
    if files_uploader is not None:
        
        # Chargement du fichier
        my_df = pd.read_excel(files_uploader)
        
        #region Périodes visées
        
        # Récupération des périodes
        period_list = []
        for i in my_df['Millesime'].unique():
            period_list.append(str(i)[:4]) # Récupération de l'année
        
        # Mise à jour du menu déroulant
        selected_year = selected_period.selectbox("Période", tuple(period_list))
        
        #endregion Périodes visées

        #region Tableaux financiers
        
        # Insertion de deux colonnes pour les tableaux
        col1, col2 = st.columns([3, 3])
        
            #region 1ère DF sur les données du bilan
        
        with col1:
            
            # Récupération des données de la fonction
            tab1 = func_tab1(my_df, selected_year)

            # Options complémentaires : modification des données
            
            gd = GridOptionsBuilder.from_dataframe(tab1) # configuration avec la DF
            
            gd.configure_default_column(editable=True, # Modification des données
                                        groupable=True # TCD, export
                                        )  
            
            # Conditions sur les cellules (script JavaScript)
            cellstyle_jscode = JsCode(
                """
                function(params) {
                    if (params.value < '0') {
                        return {
                            'color':'red',
                        }
                    }
                    else {
                        return {
                            'color':'blue',
                        }
                    }          
                };
                """ 
            )
            # Activation du script de JS
            gd.configure_column("VAR N-1 / N", cellStyle=cellstyle_jscode)
            
            # Mise en place des options complémentaires
            gridoptions=gd.build()  
            
            # Affichage de la DF
            AgGrid(tab1,
                    gridOptions=gridoptions, # options complémentaires
                    fit_columns_on_grid_load=True, # ajust automatique des colonnes
                    enable_enterprise_modules=True, # Script JS
                    allow_unsafe_jscode=True, # Script JS
                    )
        
            #endregion 1ère DF sur les données du bilan
        
            #region 2ème DF sur les données du compte de résultat
        
        with col2:
        
            # Récupération des données de la fonction
            tab2 = func_tab2(my_df, selected_year)
            
            # Options complémentaires : modification des données
            
            gd = GridOptionsBuilder.from_dataframe(tab2) # configuration avec la DF
            
            gd.configure_default_column(editable=True, # Modification des données
                                        groupable=True # TCD, export
                                        )  
            
            # Conditions sur les cellules (script JavaScript)
            cellstyle_jscode = JsCode(
                """
                function(params) {
                    if (params.value < '0') {
                        return {
                            'color':'red',
                        }
                    }
                    else {
                        return {
                            'color':'blue',
                        }
                    }          
                };
                """ 
            )
            # Activation du script de JS
            gd.configure_column("VAR N-1 / N", cellStyle=cellstyle_jscode)
            
            # Mise en place des options complémentaires
            gridoptions=gd.build()  
            
            # Affichage de la DF
            AgGrid(tab2,
                    gridOptions=gridoptions, # options complémentaires
                    fit_columns_on_grid_load=True, # ajust automatique des colonnes
                    enable_enterprise_modules=True, # Script JS
                    allow_unsafe_jscode=True, # Script JS
                    )
        
            #endregion 2ème DF sur les données du compte de résultat
        
        #endregion Tableaux financiers
        
        #region Graphiques financiers
        
        # Insertion de deux colonnes pour les graphiques
        col1, col2 = st.columns([3, 3])
        
            #region 1ère graphique sur l'évolution des postes de charges
        
        with col1:
            
            # Récupération des données de la fonction
            costs_df = func_graph1(my_df, selected_year)

            # Configuration du graphique
            fig1 = px.histogram(costs_df, 
                            x=['N', 'N-1'],
                            y='POSTE',
                            title='Évolution des postes de charges',
                            barmode='group', # Séparation barres N-1 et N
                            orientation='h')
            fig1.update_layout(yaxis_title=None, xaxis_title=None,
                                margin=dict(l=20, r=20, t=50, b=50))
            st.plotly_chart(fig1)

            #endregion 1ère graphique sur l'évolution des postes de charges

            #region 2ème graphique sur les marges SIG

        with col2:
        
            # Récupération des données de la fonction
            analysis_df = func_graph2(my_df, selected_year)
                
            # Configuration du graphique
            fig2 = px.bar(analysis_df,
                          x='POSTE',
                          y='VAR',
                          title='Évolution des marges SIG (en %)',
                          text='VAR')
            fig2.update_traces(textposition='inside')
            fig2.update_layout(yaxis_title=None, xaxis_title=None,
                               xaxis={'categoryorder':'total descending' # décroissant
                                      })
            st.plotly_chart(fig2)

            #endregion 2ème graphique sur les marges SIG
        
            #region 3ème graphique sur l'évoluation du CAHT
        
        col4, col5, col6 = st.columns([1, 3, 1])
        
        with col5:
            
            # Récupération des années visées
            revenues_period = (my_df.loc[
                my_df['POSTE 2'].astype('str').str.contains('CAHT'), ['Millesime']])
            revenues_period['Millesime'] = (
                revenues_period['Millesime'].dt.strftime('%Y-%m-%d'))
            revenues_period['Millesime'] = (
                revenues_period['Millesime'].str.slice(start=0, stop=4))
            period_list = revenues_period['Millesime'].values.tolist()
            
            # Récupération des CAHT
            revenus_accounts = (my_df.loc[
                my_df['POSTE 2'].astype('str').str.contains('CAHT'), ['N']])
            revenues_list = revenus_accounts['N'].values.tolist()

            # DF sur le CAHT par période
            revenues_df = pd.DataFrame({
                'Période':period_list,
                'MONTANT':revenues_list})

            # Configuration du graphique
            fig3 = px.bar(revenues_df, title='Évolution du CAHT', color='Période',
                            height=300)
            fig3.update_xaxes(visible=False)
            fig3.update_layout(yaxis_title=None, 
                                margin=dict(l=20, r=20, t=50, b=50))

            st.plotly_chart(fig3)
        
            #endregion 3ème graphique sur l'évoluation du CAHT
        
        #endregion Graphiques financiers
        
    #endregion Chargement du fichier Excel     

if __name__ == '__main__':
    
    application()
