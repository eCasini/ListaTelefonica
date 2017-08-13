# Programa - Lista Telefônica
# Versão - 1.0
# Usuário digita uma palavra e pressiona Enter
# vai fazer a busca no banco com a(s) palavra(s) parecida(s)
# exibe abaixo a lista de resultados por ordem de relevancia
#
# Exibira uma linha com o nome da área e seu ramal
# logo abaixo, se existir, exibirá os sublocais e seus ramais internos

import sqlite3
import kivy
kivy.require("1.10.0")

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.clock import Clock

# Cria ou inicia conexao com o banco
con = sqlite3.connect('ListaTelDB.sqlite')
# Cria um handle para o banco de dados
cur = con.cursor()

class ListaT(BoxLayout):
    input_wid = ObjectProperty()

    def refocus(self, *args):
        self.input_wid.text = ""
        self.input_wid.focus = True

    def busca(self, string):
        # Limpa os widgets caso haja um pesquisa anterior já exibida na tela
        for child in [child for child in self.children]:
            if (str(type(child)) != "<class 'kivy.uix.textinput.TextInput'>"):
                ListaT.remove_widget(self, child)

        # Faz a busca pela palavra digitada e popula os resultados nos Labels
        string = "%" + string + "%"
        cur.execute('SELECT Area.nome, Area.ramal FROM Area WHERE Area.nome like ?', (string,))
        result = cur.fetchall()
        if len(result) >= 1:
            for local in result:
                cur.execute('SELECT Area.nome, Area.ramal, SubArea.nome, SubArea.ramal '
                            'FROM Area join SubArea '
                            'WHERE Area.nome like ? and Area.id == SubArea.area_id', (str(local[0]),))
                subresult = cur.fetchall()
                if subresult == []:
                    stringArea = str(local[0]) + "    " + "--------    " + str(local[1]) + "\n"
                    lb = Label(text=stringArea)
                    self.add_widget(lb)
                else:
                    stringArea = str(local[0]) + "    " + "--------    " + str(local[1]) + "\n"
                    stringSubArea = str()
                    for i in subresult:
                        stringSubArea += "    " + i[2] + "    " + "--------    " + str(i[3]) + "\n"
                    lb = Label(text=stringArea + stringSubArea)
                    self.add_widget(lb)
            Clock.schedule_once(self.refocus)
        else:
            lb = Label(text="NÃO ENCONTREI NADA!")
            self.add_widget(lb)
            Clock.schedule_once(self.refocus)


class ListaTelApp(App):
    def build(self):
        return ListaT()

ltApp = ListaTelApp()
ltApp.run()