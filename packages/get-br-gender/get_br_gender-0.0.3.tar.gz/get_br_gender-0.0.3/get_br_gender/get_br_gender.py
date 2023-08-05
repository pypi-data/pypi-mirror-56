import pandas as pd
from unidecode import unidecode


class GetBrGender:
    def __init__(self):
        NomeGenero = pd.read_excel('get_br_gender/nome_genero.xlsx', sheet_name='Sheet1')
        self.dictNomeGenero = dict(zip(NomeGenero.Nome, NomeGenero.Genero))

    def getGenero(self, string):
        foundName = 0
        notFoundName = 0
        string2 = ""
        string2 = unidecode(string[0:string.find(' ')]).upper()
        if (string2 in self.dictNomeGenero):
            return self.dictNomeGenero[string2]
            foundName = foundName+1
        else:
            notFoundName = notFoundName+1
            if (string2[len(string2)-1:len(string2)] == 'A' or string2[len(string2)-1:len(string2)] == 'I' or string2[len(string2)-1:len(string2)] == 'Y' or string2[len(string2)-1:len(string2)] == 'E'):
                return 'F'
            else:
                return 'M'
