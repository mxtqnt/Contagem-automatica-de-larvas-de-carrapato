import pandas as pd

def criar_planilha(larvas, frames):
    planilha_vazia = pd.DataFrame(index=range(larvas), columns=range(frames))
    return planilha_vazia

def inserir_dado(planilha, linha, coluna, dado):
    planilha.at[linha, coluna] = dado
    return planilha