import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
# Options complémentaires
from st_aggrid.grid_options_builder import GridOptionsBuilder
# Saisies en JavaScript : condition sur cellule
from st_aggrid.shared import JsCode
import plotly.express as px

def func_df(df):
    # Traitements opérés en matière de DS sur les balances chargées
    
    #region Créances clients
          
    # Récupération des comptes 41 par millésime
    fb_41 = df.loc[df['Compte'].astype('str').str.contains('^41')]
    fb_41 = fb_41.groupby('Millesime')['Solde créditeur'].sum().reset_index()
    fb_41['Solde créditeur'] = - fb_41['Solde créditeur']
    
    # Insertion d'une colonne récupérant les valeurs de N-1
    fb_41.insert(loc=2, column='N-1', value=fb_41['Solde créditeur'].shift(1))
    
    # Ajout des colonnes 'POSTE 1', 'POSTE 2' et 'VAR'
    fb_41.insert(loc=0, column='POSTE 1', value='BILAN')
    fb_41.insert(loc=1, column='POSTE 2', value='CREANCES')
    fb_41.insert(loc=fb_41.shape[1], column='VAR', 
                value=(fb_41['Solde créditeur']-fb_41['N-1'])/abs(fb_41['N-1']))
    
    # Remplacement des valeurs NaN dans la colonne 'N-1' par 0
    fb_41.fillna(0, inplace=True)
    
    #endregion Créances clients
    
    #region Dettes fournisseurs
    
    # Récupération des comptes 40 par millésime
    fb_40 = df.loc[df['Compte'].astype('str').str.contains('^40')]
    fb_40 = fb_40.groupby('Millesime')['Solde créditeur'].sum().reset_index()
    
    # Insertion d'une colonne récupérant les valeurs de N-1
    fb_40.insert(loc=2, column='N-1', value=fb_40['Solde créditeur'].shift(1))
    
    # Ajout des colonnes 'POSTE 1', 'POSTE 2' et 'VAR'
    fb_40.insert(loc=0, column='POSTE 1', value='BILAN')
    fb_40.insert(loc=1, column='POSTE 2', value='DETTES')
    fb_40.insert(loc=fb_40.shape[1], column='VAR', 
                value=(fb_40['Solde créditeur']-fb_40['N-1'])/abs(fb_40['N-1']))
    
    # Remplacement des valeurs NaN dans la colonne 'N-1' par 0
    fb_40.fillna(0, inplace=True)
    
    #endregion Dettes fournisseurs
    
    #region Chiffre d'affaires
    
    # Récupération des comptes 70 par millésime
    fb_70 = df.loc[df['Compte'].astype('str').str.contains('^70')]
    fb_70 = fb_70.groupby('Millesime')['Solde créditeur'].sum().reset_index()
    
    # Insertion d'une colonne récupérant les valeurs de N-1
    fb_70.insert(loc=2, column='N-1', value=fb_70['Solde créditeur'].shift(1))
    
    # Ajout des colonnes 'POSTE 1', 'POSTE 2' et 'VAR'
    fb_70.insert(loc=0, column='POSTE 1', value='PRODUITS')
    fb_70.insert(loc=1, column='POSTE 2', value='CAHT')
    fb_70.insert(loc=fb_70.shape[1], column='VAR', 
                value=(fb_70['Solde créditeur']-fb_70['N-1'])/fb_70['N-1'])
    
    # Remplacement des valeurs NaN dans la colonne 'N-1' par 0
    fb_70.fillna(0, inplace=True)
    
    #endregion Chiffre d'affaires
    
    #region Achats
    
    # Récupération des comptes 60 par millésime
    fb_60 = df.loc[df['Compte'].astype('str').str.contains('^60')]
    fb_60 = fb_60.groupby('Millesime')['Solde créditeur'].sum().reset_index()
    fb_60['Solde créditeur'] = - fb_60['Solde créditeur']
    
    # Insertion d'une colonne récupérant les valeurs de N-1
    fb_60.insert(loc=2, column='N-1', value=fb_60['Solde créditeur'].shift(1))
    
    # Ajout des colonnes 'POSTE 1', 'POSTE 2' et 'VAR'
    fb_60.insert(loc=0, column='POSTE 1', value='CHARGES')
    fb_60.insert(loc=1, column='POSTE 2', value='60 - ACHATS')
    fb_60.insert(loc=fb_60.shape[1], column='VAR', 
                value=(fb_60['Solde créditeur']-fb_60['N-1'])/abs(fb_60['N-1']))
    
    # Remplacement des valeurs NaN dans la colonne 'N-1' par 0
    fb_60.fillna(0, inplace=True)
    
    #endregion Achats
    
    #region Services extérieurs
    
    # Récupération des comptes 61/62 par millésime
    fb_61 = df.loc[(~df['Compte'].astype('str').str.contains('^621|^627')) &
                (df['Compte'].astype('str').str.contains('^61|^62'))]
    fb_61 = fb_61.groupby('Millesime')['Solde créditeur'].sum().reset_index()
    fb_61['Solde créditeur'] = - fb_61['Solde créditeur']
    
    # Insertion d'une colonne récupérant les valeurs de N-1
    fb_61.insert(loc=2, column='N-1', value=fb_61['Solde créditeur'].shift(1))
    
    # Ajout des colonnes 'POSTE 1', 'POSTE 2' et 'VAR'
    fb_61.insert(loc=0, column='POSTE 1', value='CHARGES')
    fb_61.insert(loc=1, column='POSTE 2', value='61/62 - SERV. EXTERIEURS')
    fb_61.insert(loc=fb_61.shape[1], column='VAR', 
                value=(fb_61['Solde créditeur']-fb_61['N-1'])/abs(fb_61['N-1']))
    
    # Remplacement des valeurs NaN dans la colonne 'N-1' par 0
    fb_61.fillna(0, inplace=True)

    #endregion Services extérieurs
        
    #region Impôts et taxes
    
    # Récupération des comptes 63 et 695 + suiv. par millésime
    fb_63 = df.loc[
        df['Compte'].astype('str').str.contains('^63|^695|^696|^697|^698|^699')]
    fb_63 = fb_63.groupby('Millesime')['Solde créditeur'].sum().reset_index()
    fb_63['Solde créditeur'] = - fb_63['Solde créditeur']
    
    # Insertion d'une colonne récupérant les valeurs de N-1
    fb_63.insert(loc=2, column='N-1', value=fb_63['Solde créditeur'].shift(1))
    
    # Ajout des colonnes 'POSTE 1', 'POSTE 2' et 'VAR'
    fb_63.insert(loc=0, column='POSTE 1', value='CHARGES')
    fb_63.insert(loc=1, column='POSTE 2', value='63 - IMPOTS & TAXES')
    fb_63.insert(loc=fb_63.shape[1], column='VAR', 
                value=(fb_63['Solde créditeur']-fb_63['N-1'])/abs(fb_63['N-1']))
    
    # Remplacement des valeurs NaN dans la colonne 'N-1' par 0
    fb_63.fillna(0, inplace=True)
    
    #endregion Impôts et taxes
    
    #region Personnel
    
    # Récupération des comptes 621, 64 et 691 par millésime
    fb_64 = df.loc[
        df['Compte'].astype('str').str.contains('^621|^64|^691')]
    fb_64 = fb_64.groupby('Millesime')['Solde créditeur'].sum().reset_index()
    fb_64['Solde créditeur'] = - fb_64['Solde créditeur']
    
    # Insertion d'une colonne récupérant les valeurs de N-1
    fb_64.insert(loc=2, column='N-1', value=fb_64['Solde créditeur'].shift(1))
    
    # Ajout des colonnes 'POSTE 1', 'POSTE 2' et 'VAR'
    fb_64.insert(loc=0, column='POSTE 1', value='CHARGES')
    fb_64.insert(loc=1, column='POSTE 2', value='64 - PERSONNEL')
    fb_64.insert(loc=fb_64.shape[1], column='VAR', 
                value=(fb_64['Solde créditeur']-fb_64['N-1'])/abs(fb_64['N-1']))
    
    # Remplacement des valeurs NaN dans la colonne 'N-1' par 0
    fb_64.fillna(0, inplace=True)
    
    #endregion Personnel
    
    #region Charges financières
    
    # Récupération des comptes 627, 66 par millésime
    fb_66 = df.loc[
        df['Compte'].astype('str').str.contains('^627|^66')]
    fb_66 = fb_66.groupby('Millesime')['Solde créditeur'].sum().reset_index()
    fb_66['Solde créditeur'] = - fb_66['Solde créditeur']
    
    # Insertion d'une colonne récupérant les valeurs de N-1
    fb_66.insert(loc=2, column='N-1', value=fb_66['Solde créditeur'].shift(1))
    
    # Ajout des colonnes 'POSTE 1', 'POSTE 2' et 'VAR'
    fb_66.insert(loc=0, column='POSTE 1', value='CHARGES')
    fb_66.insert(loc=1, column='POSTE 2', value='66 - FINANCIER')
    fb_66.insert(loc=fb_66.shape[1], column='VAR', 
                value=(fb_66['Solde créditeur']-fb_66['N-1'])/abs(fb_66['N-1']))
    
    # Remplacement des valeurs NaN dans la colonne 'N-1' par 0
    fb_66.fillna(0, inplace=True)
    
    #endregion Charges financières
    
    #region Charges exceptionnelles
    
    # Récupération des comptes 67 par millésime
    fb_67 = df.loc[df['Compte'].astype('str').str.contains('^67')]
    fb_67 = fb_67.groupby('Millesime')['Solde créditeur'].sum().reset_index()
    fb_67['Solde créditeur'] = - fb_67['Solde créditeur']
    
    # Insertion d'une colonne récupérant les valeurs de N-1
    fb_67.insert(loc=2, column='N-1', value=fb_67['Solde créditeur'].shift(1))
    
    # Ajout des colonnes 'POSTE 1', 'POSTE 2' et 'VAR'
    fb_67.insert(loc=0, column='POSTE 1', value='CHARGES')
    fb_67.insert(loc=1, column='POSTE 2', value='67 - EXCEPTIONNEL')
    fb_67.insert(loc=fb_67.shape[1], column='VAR', 
                value=(fb_67['Solde créditeur']-fb_67['N-1'])/abs(fb_67['N-1']))
    
    # Remplacement des valeurs NaN dans la colonne 'N-1' par 0
    fb_67.fillna(0, inplace=True)
    
    #endregion Charges exceptionnelles
    
    #region Résultat d'exploitation
    
    # Récupération des comptes 70 à 75 et 60 à 65... par millésime
    fb_op_result = df.loc[
        df['Compte'].astype('str').str.contains(
        '^70|^71|^72|^73|^74|^75|^781|^791|^60|^61|^62|^63|^64|^65|^681')]
    fb_op_result = (fb_op_result.groupby('Millesime')['Solde créditeur']
                    .sum().reset_index())
    
    # Insertion d'une colonne récupérant les valeurs de N-1
    fb_op_result.insert(
        loc=2, column='N-1', value=fb_op_result['Solde créditeur'].shift(1))
    
    # Ajout des colonnes 'POSTE 1', 'POSTE 2' et 'VAR'
    fb_op_result.insert(loc=0, column='POSTE 1', value='ANALYSE FIN')
    fb_op_result.insert(loc=1, column='POSTE 2', value='RESULTAT EXPLOITATION')
    fb_op_result.insert(loc=fb_op_result.shape[1], column='VAR', 
                value=((fb_op_result['Solde créditeur']-fb_op_result['N-1'])
                /abs(fb_op_result['N-1'])))
    
    # Remplacement des valeurs NaN dans la colonne 'N-1' par 0
    fb_op_result.fillna(0, inplace=True)
    
    #endregion Résultat d'exploitation
    
    #region Résultat comptable
    
    # Récupération des comptes 6 et 7
    fb_result = df.loc[
        df['Compte'].astype('str').str.contains('^7|^6')]
    fb_result = (fb_result.groupby('Millesime')['Solde créditeur']
                    .sum().reset_index())
    
    # Insertion d'une colonne récupérant les valeurs de N-1
    fb_result.insert(
        loc=2, column='N-1', value=fb_result['Solde créditeur'].shift(1))
    
    # Ajout des colonnes 'POSTE 1', 'POSTE 2' et 'VAR'
    fb_result.insert(loc=0, column='POSTE 1', value='ANALYSE FIN')
    fb_result.insert(loc=1, column='POSTE 2', value='RESULTAT')
    fb_result.insert(loc=fb_result.shape[1], column='VAR', 
                value=((fb_result['Solde créditeur']-fb_result['N-1'])
                /abs(fb_result['N-1'])))
    
    # Remplacement des valeurs NaN dans la colonne 'N-1' par 0
    fb_result.fillna(0, inplace=True)
    
    #endregion Résultat comptable
    
    #region Fonds de roulement
    
    # Récupération des comptes
    fb_work_capital = df.loc[
        df['Compte'].astype('str').str.contains('^1|^2|^39|^49|^59')]
    fb_work_capital = (fb_work_capital.groupby('Millesime')
                    ['Solde créditeur'].sum().reset_index())
    
    # Insertion d'une colonne récupérant les valeurs de N-1
    fb_work_capital.insert(
        loc=2, column='N-1', value=fb_work_capital['Solde créditeur'].shift(1))
    
    # Ajout des colonnes 'POSTE 1', 'POSTE 2' et 'VAR'
    fb_work_capital.insert(loc=0, column='POSTE 1', value='ANALYSE FIN')
    fb_work_capital.insert(loc=1, column='POSTE 2', value='FR')
    fb_work_capital.insert(loc=fb_work_capital.shape[1], column='VAR', 
                value=((fb_work_capital['Solde créditeur']
                        -fb_work_capital['N-1'])
                        /abs(fb_work_capital['N-1'])))
    
    # Remplacement des valeurs NaN dans la colonne 'N-1' par 0
    fb_work_capital.fillna(0, inplace=True)
    
    #endregion Fonds de roulement
    
    #region Besoin en fonds de roulement
    
    # Récupération des comptes
    fb_requirements = df.loc[
        (~df['Compte'].astype('str').str.contains('^39|^49')) &
        (df['Compte'].astype('str').str.contains('^3|^4'))]
    fb_requirements = (fb_requirements.groupby('Millesime')
                    ['Solde créditeur'].sum().reset_index())
    fb_requirements['Solde créditeur'] = - fb_requirements['Solde créditeur']
    
    # Insertion d'une colonne récupérant les valeurs de N-1
    fb_requirements.insert(
        loc=2, column='N-1', value=fb_requirements['Solde créditeur'].shift(1))
    
    # Ajout des colonnes 'POSTE 1', 'POSTE 2' et 'VAR'
    fb_requirements.insert(loc=0, column='POSTE 1', value='ANALYSE FIN')
    fb_requirements.insert(loc=1, column='POSTE 2', value='BFR')
    fb_requirements.insert(loc=fb_requirements.shape[1], column='VAR', 
                value=((fb_requirements['Solde créditeur']
                        -fb_requirements['N-1'])
                        /abs(fb_requirements['N-1'])))
    
    # Remplacement des valeurs NaN dans la colonne 'N-1' par 0
    fb_requirements.fillna(0, inplace=True)
    
    #endregion Besoin en fonds de roulement
    
    #region Trésorerie
    
    # Récupération des comptes
    fb_cash = df.loc[
        (~df['Compte'].astype('str').str.contains('^59')) &
        (df['Compte'].astype('str').str.contains('^5'))]
    fb_cash = (fb_cash.groupby('Millesime')['Solde créditeur']
                .sum().reset_index())
    fb_cash['Solde créditeur'] = - fb_cash['Solde créditeur']
    
    # Insertion d'une colonne récupérant les valeurs de N-1
    fb_cash.insert(
        loc=2, column='N-1', value=fb_cash['Solde créditeur'].shift(1))
    
    # Ajout des colonnes 'POSTE 1', 'POSTE 2' et 'VAR'
    fb_cash.insert(loc=0, column='POSTE 1', value='ANALYSE FIN')
    fb_cash.insert(loc=1, column='POSTE 2', value='TRESORERIE')
    fb_cash.insert(loc=fb_cash.shape[1], column='VAR', 
                value=((fb_cash['Solde créditeur']
                        -fb_cash['N-1'])/abs(fb_cash['N-1'])))
    
    # Remplacement des valeurs NaN dans la colonne 'N-1' par 0
    fb_cash.fillna(0, inplace=True)
    
    #endregion Trésorerie
    
    #region Valeur ajoutée
    
    # Récupération des comptes
    fb_added_value = df.loc[
        df['Compte'].astype('str').str.contains('^70|^71|^72|^60|^61|^62')]
    fb_added_value = (fb_added_value.groupby('Millesime')['Solde créditeur']
                    .sum().reset_index())
    
    # Insertion d'une colonne récupérant les valeurs de N-1
    fb_added_value.insert(
        loc=2, column='N-1', value=fb_added_value['Solde créditeur'].shift(1))
    
    # Ajout des colonnes 'POSTE 1', 'POSTE 2' et 'VAR'
    fb_added_value.insert(loc=0, column='POSTE 1', value='ANALYSE FIN')
    fb_added_value.insert(loc=1, column='POSTE 2', value='VA')
    fb_added_value.insert(loc=fb_added_value.shape[1], column='VAR', 
                value=((fb_added_value['Solde créditeur']-fb_added_value['N-1'])
                        /abs(fb_added_value['N-1'])))
    
    # Remplacement des valeurs NaN dans la colonne 'N-1' par 0
    fb_added_value.fillna(0, inplace=True)
    
    #endregion Valeur ajoutée
    
    #region EBITDA
    
    # Récupération des comptes
    fb_ebitda = df.loc[
        df['Compte'].astype('str').str.contains(
        '^70|^713|^75|^7817|^791|^60|^61|^62|^63|^64|^65|^6817|^691')]
    fb_ebitda = (fb_ebitda.groupby('Millesime')['Solde créditeur']
                    .sum().reset_index())
    
    # Insertion d'une colonne récupérant les valeurs de N-1
    fb_ebitda.insert(
        loc=2, column='N-1', value=fb_ebitda['Solde créditeur'].shift(1))
    
    # Ajout des colonnes 'POSTE 1', 'POSTE 2' et 'VAR'
    fb_ebitda.insert(loc=0, column='POSTE 1', value='ANALYSE FIN')
    fb_ebitda.insert(loc=1, column='POSTE 2', value='EBITDA')
    fb_ebitda.insert(loc=fb_ebitda.shape[1], column='VAR', 
                value=((fb_ebitda['Solde créditeur']-fb_ebitda['N-1'])
                        /abs(fb_ebitda['N-1'])))
    
    # Remplacement des valeurs NaN dans la colonne 'N-1' par 0
    fb_ebitda.fillna(0, inplace=True)
    
    #endregion EBITDA
    
    #region CAF
    
    # Récupération des comptes
    
    fb_self_financing = df.loc[
        (~df['Compte'].astype('str').str.contains('^675|^775|^777|^68|^78'))
        & (df['Compte'].astype('str').str.contains('^6|^7'))]
    fb_self_financing = (fb_self_financing.groupby('Millesime')
                            ['Solde créditeur'].sum().reset_index())
    
    # Insertion d'une colonne récupérant les valeurs de N-1
    fb_self_financing.insert(
        loc=2, column='N-1', 
        value=fb_self_financing['Solde créditeur'].shift(1))
    
    # Ajout des colonnes 'POSTE 1', 'POSTE 2' et 'VAR'
    fb_self_financing.insert(loc=0, column='POSTE 1', value='ANALYSE FIN')
    fb_self_financing.insert(loc=1, column='POSTE 2', value='CAF')
    fb_self_financing.insert(loc=fb_self_financing.shape[1], column='VAR', 
                value=((fb_self_financing['Solde créditeur']
                        -fb_self_financing['N-1'])
                        /abs(fb_self_financing['N-1'])))
    
    # Remplacement des valeurs NaN dans la colonne 'N-1' par 0
    fb_self_financing.fillna(0, inplace=True)
    
    #endregion CAF
    
    #region Concaténation de toutes les opérations sélectionnées
    
    # Concaténation
    balance_df = pd.concat([
        fb_41, fb_40, fb_70, fb_60, fb_61, fb_63,
        fb_64, fb_66, fb_67, fb_op_result, fb_result,
        fb_work_capital, fb_requirements, fb_cash,
        fb_added_value, fb_ebitda, fb_self_financing], axis=0)
    
    # Renommage de la colonne 'Solde créditeur'
    balance_df.rename(columns={"Solde créditeur":"N"}, inplace=True)
    
    # Conversion du champ 'Millesime' en datetime
    balance_df['Millesime'] = pd.to_datetime(
        balance_df['Millesime'], format='%Y%m%d') 
    
    return balance_df

    #endregion Concaténation de toutes les opérations sélectionnées

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
    # Configuration de la page web
    
    #region Configuration de la page principale
    
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
        "<h3 style='text-align: center; color: #41a0cc;'>ANALYSE FINANCIÈRE</h3>", 
        unsafe_allow_html=True # HTML par défaut
        )
    
    #endregion Configuration de la page principale

    #region Balances à charger et périodes visées
    
    # Insertion des colonnes pour les balances à charger et les périodes visées
    col1, col2, col3 = st.columns([0.7, 3.8, 0.5])

    # Menu déroulant du nombre de balances à charger
    data_numbers = col1.selectbox("Nombre de balances à charger", (2, 3, 4, 5))
    
    # Attribution d'une variable pour màj lors du chargement du fichier :
    # présence d'un menu déroulant
    selected_period = col3.empty()
    
    #endregion Balances à charger et périodes visées

    #region Chargement des balances
    
    # Insertion des colonnes au regard du nombre de fichiers chargés
    col1, col2, col3, col4, col5 = st.columns([3, 3, 3, 3, 3])

    # Assignation d'une DF vide
    my_df = pd.DataFrame()
    
    # Si le nombre de fichier à charger est de 2
    if data_numbers == 2:
        
        # Chargement du 1er fichier Excel
        file1_uploader = col1.file_uploader('Balance n° 1 à charger', type='xlsx')
        # Si la fichier Excel est chargé
        if file1_uploader:
            # Conversion du fichier Excel en DF
            full1 = pd.read_excel(file1_uploader, sheet_name=3)
        
        # Chargement du 2ème fichier Excel
        file2_uploader = col2.file_uploader('Balance n° 2 à charger', type='xlsx')
        # Si la fichier Excel est chargé
        if file2_uploader:
            # Conversion du fichier Excel en DF
            full2 = pd.read_excel(file2_uploader, sheet_name=3)
        
        # Si tous les fichiers ont été chargés
        if file1_uploader and file2_uploader:
            # Concaténation des DF
            fb = pd.concat([full1, full2], axis=0)
            # Appel de la fonction func_df()
            my_df = func_df(fb)
    
    # Si le nombre de fichier à charger est de 3
    elif data_numbers == 3:
        
        # Chargement du 1er fichier Excel
        file1_uploader = col1.file_uploader('Balance n° 1 à charger', type='xlsx')
        # Si la fichier Excel est chargé
        if file1_uploader:
            # Conversion du fichier Excel en DF
            full1 = pd.read_excel(file1_uploader, sheet_name=3)
        
        # Chargement du 2ème fichier Excel
        file2_uploader = col2.file_uploader('Balance n° 2 à charger', type='xlsx')
        # Si la fichier Excel est chargé
        if file2_uploader:
            # Conversion du fichier Excel en DF
            full2 = pd.read_excel(file2_uploader, sheet_name=3)
        
        # Chargement du 3ème fichier Excel
        file3_uploader = col3.file_uploader('Balance n° 3 à charger', type='xlsx')
         # Si la fichier Excel est chargé
        if file3_uploader:
            # Conversion du fichier Excel en DF
            full3 = pd.read_excel(file3_uploader, sheet_name=3)
        
        # Si tous les fichiers ont été chargés
        if (file1_uploader and file2_uploader and file3_uploader):
            # Concaténation des DF
            fb = pd.concat([full1, full2, full3], axis=0)
            # Appel de la fonction func_df()
            my_df = func_df(fb)
    
    # Si le nombre de fichier à charger est de 4
    elif data_numbers == 4:
        
        # Chargement du 1er fichier Excel
        file1_uploader = col1.file_uploader('Balance n° 1 à charger', type='xlsx')
        # Si la fichier Excel est chargé
        if file1_uploader:
            # Conversion du fichier Excel en DF
            full1 = pd.read_excel(file1_uploader, sheet_name=3)
        
        # Chargement du 2ème fichier Excel
        file2_uploader = col2.file_uploader('Balance n° 2 à charger', type='xlsx')
        # Si la fichier Excel est chargé
        if file2_uploader:
            # Conversion du fichier Excel en DF
            full2 = pd.read_excel(file2_uploader, sheet_name=3)
        
        # Chargement du 3ème fichier Excel
        file3_uploader = col3.file_uploader('Balance n° 3 à charger', type='xlsx')
        # Si la fichier Excel est chargé
        if file3_uploader:
            # Conversion du fichier Excel en DF
            full3 = pd.read_excel(file3_uploader, sheet_name=3)
        
        # Chargement du 4ème fichier Excel
        file4_uploader = col4.file_uploader('Balance n° 4 à charger', type='xlsx')
        # Si la fichier Excel est chargé
        if file4_uploader:
            # Conversion du fichier Excel en DF
            full4 = pd.read_excel(file4_uploader, sheet_name=3)
        
        # Si tous les fichiers ont été chargés
        if (file1_uploader and file2_uploader and file3_uploader and
            file4_uploader):
            # Concaténation des DF
            fb = pd.concat([full1, full2, full3, full4], axis=0)
            # Appel de la fonction func_df()
            my_df = func_df(fb)
    
    # Si le nombre de fichier à charger est de 5
    elif data_numbers == 5:
        
        # Chargement du 1er fichier Excel
        file1_uploader = col1.file_uploader('Balance n° 1 à charger', type='xlsx')
        # Si la fichier Excel est chargé
        if file1_uploader:
            # Conversion du fichier Excel en DF
            full1 = pd.read_excel(file1_uploader, sheet_name=3)
        
        # Chargement du 2ème fichier Excel
        file2_uploader = col2.file_uploader('Balance n° 2 à charger', type='xlsx')
        # Si la fichier Excel est chargé
        if file2_uploader:
            # Conversion du fichier Excel en DF
            full2 = pd.read_excel(file2_uploader, sheet_name=3)
        
        # Chargement du 3ème fichier Excel
        file3_uploader = col3.file_uploader('Balance n° 3 à charger', type='xlsx')
        # Si la fichier Excel est chargé
        if file3_uploader:
            # Conversion du fichier Excel en DF
            full3 = pd.read_excel(file3_uploader, sheet_name=3)
        
        # Chargement du 4ème fichier Excel
        file4_uploader = col4.file_uploader('Balance n° 4 à charger', type='xlsx')
        # Si la fichier Excel est chargé
        if file4_uploader:
            # Conversion du fichier Excel en DF
            full4 = pd.read_excel(file4_uploader, sheet_name=3)
        
        # Chargement du 5ème fichier Excel
        file5_uploader = col5.file_uploader('Balance n° 5 à charger', type='xlsx')
        # Si la fichier Excel est chargé
        if file5_uploader:
            # Conversion du fichier Excel en DF
            full5 = pd.read_excel(file5_uploader, sheet_name=3)
        
        # Si tous les fichiers ont été chargés
        if (file1_uploader and file2_uploader and file3_uploader and
            file4_uploader and file5_uploader):
            # Concaténation des DF
            fb = pd.concat([full1, full2, full3, full4, full5], axis=0)
            # Appel de la fonction func_df()
            my_df = func_df(fb)
    
    # Si les DF ont été correctement établies        
    if not my_df.empty :
        
        # Récupération des périodes
        period_list = []
        for i in my_df['Millesime'].unique():
            period_list.append(str(i)[:4]) # Récupération de l'année
        
        # Mise à jour du menu déroulant
        selected_year = selected_period.selectbox("Période", tuple(period_list))
        
    #endregion Chargement des balances
    
    #region Tableaux financiers
        
    # Insertion de deux colonnes pour les tableaux
    col1, col2 = st.columns([3, 3])
    
    try:
    
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
        col1.plotly_chart(fig1)

        #endregion 1ère graphique sur l'évolution des postes de charges

        #region 2ème graphique sur les marges SIG
        
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
        col2.plotly_chart(fig2)

        #endregion 2ème graphique sur les marges SIG
        
        #region 3ème graphique sur l'évoluation du CAHT
        
        col4, col5, col6 = st.columns([1, 3, 1])

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

        col5.plotly_chart(fig3)

        #endregion 3ème graphique sur l'évoluation du CAHT
        
    #endregion Graphiques financiers
    
    except UnboundLocalError:
        # Dans le cas où les fichiers n'ont pas été correctement chargés
        
        col1, col2, col3, col4, col5 = st.columns([0.7, 1.5, 3, 0.5, 1])
        col3.subheader("Merci de mettre à jour les fichiers à charger 😎")
    
if __name__ == '__main__':
    
    application()
