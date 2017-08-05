# Programa - Lista Telefônica
# Versão - 0.1
# usuário digita uma palavra e clica ok ou da enter
# vai fazer a busca no banco para uma palavra(s) parecida(s)
# exibe no frame de baixo a lista por ordem de relevancia
#
# Exibira um label com o nome da área e outro com o ramal
# logo abaixo, se existir, exibirá os sublocais e seus ramais internos

import sqlite3
import kivy
kivy.require("1.10.0")


from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.properties import ListProperty

# Cria ou inicia conexao com o banco
con = sqlite3.connect('ListaTelDB.sqlite')
# Cria um handle para o banco de dados
cur = con.cursor()

# cur.execute('SELECT ramal FROM Area WHERE nome == ?', (string,))

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
        existeSubArea = True
        cur.execute('SELECT Area.nome, Area.ramal, SubArea.nome, SubArea.ramal '
                    'FROM Area join SubArea '
                    'WHERE Area.id == SubArea.area_id and Area.nome == ?', (string,))
        result = cur.fetchall()
        if result == []:
            cur.execute('SELECT Area.nome, Area.ramal FROM Area WHERE Area.nome == ?', (string,))
            result = cur.fetchall()
            existeSubArea = False
        if result != []:
            stringArea = str(result[0][0]) + "    " + "--------    " + str(result[0][1]) + "\n"
            # print(stringArea)
            if existeSubArea:
                stringSubArea = str()
                for i in result:
                    stringSubArea += "    " + i[2] + "    " + "--------    " + str(i[3]) + "\n"
                # print(stringSubArea)
                lb = Label(text=stringArea + stringSubArea)
            else:
                lb = Label(text=stringArea)
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