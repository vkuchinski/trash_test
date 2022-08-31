# -*- coding: utf-8 -*-
"""
Converte grid de chuva para formato tripa do MGB e arquivos de cadastro

@author: Mino Sorribas
"""

import json
import pandas as pd


rainfall_csv = 'grid.csv'



# le dados
df = pd.read_csv(rainfall_csv)

# inclui coordenadas
df_coords = df.apply(lambda x:json.loads(x['.geo'])['coordinates'], axis = 1, result_type='expand')
df_coords.columns = ['lon','lat']

# organiza os dados
df = pd.concat([df,df_coords],axis = 1)
df = df.iloc[:,1:].drop('.geo',axis=1)


# datas em formato pt-br
datas = pd.to_datetime( df.columns[:-2] )
datas_ptbr = datas.strftime('    %d    %m  %Y')


# abre arquivos para cadastro no mgb
fil_nomes = open('_Nomes_Chuva.txt','w')
fil_estacoes = open('_Estacoes1_Chuva.txt','w')
fil_lats = open('_Latitudes1_Chuva.txt','w')
fil_lons = open('_Longitudes1_Chuva.txt','w')


# itera pontos do grid e salva arquivos
conta = 0
fmt = {'datas':"{:>18}".format,
       'chuva':"{:>15,.6f}".format}
for i,row in df.iterrows():

    conta = conta+1

    #ajusta dados em formato tripa
    dfp = row[:-2].to_frame()
    dfp.columns = ['chuva']
    dfp['datas'] = datas_ptbr
    dfp = dfp.set_index('datas')
    dfp = dfp.reset_index()

    # salva serie temporal
    code =  f'raingrid_{row.lon:.3f}_{row.lat:.3f}.txt'
    code = '9' + str(conta).zfill(7) + '.txt'
    code = '099' + str(conta).zfill(5) + '.txt'
    with open(code,'w') as f:
        f.write(dfp.to_string(index = False, header = False, formatters = fmt))

    # atualiza arquivos de cadastro
    #fil_nomes.write('GRID_9' + str(conta).zfill(7) + '\n')
    #fil_estacoes.write('9' + str(conta).zfill(7) + '\n')  #

    fil_nomes.write('099' + str(conta).zfill(5) + '\n')
    fil_estacoes.write('099' + str(conta).zfill(5) + '\n')

    fil_lats.write(f'{row.lat:.3f}' + '\n')
    fil_lons.write(f'{row.lon:.3f}' + '\n')


fil_nomes.close()
fil_estacoes.close()
fil_lats.close()
fil_lons.close()


