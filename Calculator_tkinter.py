# -*- coding: utf-8 -*-

from tkinter import *
from math import *
import tkinter.font


class Fenetre(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("TP calculatrice")

        # Placer la fenêtre
        ecran_x = self.winfo_screenwidth()
        ecran_y = self.winfo_screenheight()
        fenetre_x = 420
        fenetre_y = 640
        pos_x = ecran_x // 2 - fenetre_x // 2
        pos_y = ecran_y // 2 - fenetre_y // 2
        geometrie = f"{fenetre_x}x{fenetre_y}+{pos_x}+{pos_y}"
        self.geometry(geometrie)

        # Variables
        self.cur_list = []                # Chaque touche tapée est stockée comme un élément de cette liste
        self.formula_str = ''             # transfert la liste à un str
        self.formula_str_2 = ''           # changer formula_str en une forme arithmétique
        self.result_float = 0             # Contient le résultat
        self.result_str = ''              # transfert le résultat
        self.did_tap_equal = False

        # Variables pour les résultats
        self.result_affiche_str = ''
        self.result_affiche = StringVar()
        self.result_affiche.set('0')

        # Variables pour les historiques
        self.historiques = []
        self.nb_his = 0
        self.pointer = 0

        # Variables pour afficher deg/rad
        self.rd = StringVar()
        self.rd.set('deg')

        # Afficher les labels et buttons pour la fenêtre
        self.labels()
        self.buttons()

    def set_rd(self):
        """
        Régler et afficher le système d'angle et de radian
        :return: None
        """
        # Afficher le degré ou radia dans la calculatrice
        if self.rd.get() == 'deg':
            self.rd.set('rad')
        else:
            self.rd.set('deg')

    def list_to_formula(self):
        """
        Convertit une liste de valeurs d'entrée enregistrées en un type de données affichables.
        :return: None
        """
        # Initialisation de 'formula_str'
        self.formula_str = ''
        # transfert des variables
        for elem in self.cur_list:
            self.formula_str += elem

        self.result_affiche_str = self.formula_str
        self.result_affiche.set(self.result_affiche_str)

    def press_num_operator(self, button: str):
        """
        Saisir des chiffres et des opérateurs
        :param button: [str], Différents chiffres et opérateurs
        :return: None
        """
        self.did_tap_equal = False
        # Sauvegarder la valeur saisie dans la liste
        self.cur_list.append(button)
        print(self.cur_list)
        self.list_to_formula()
        # Réinitialiser le pointer à la dernière histoire
        self.pointer = self.nb_his + 1

    def press_c_ac(self, button: str):
        """
        Effacer la formule ou le résultat affiché
        :param button: [str], 'C'=Effacer un, 'AC'=effacer tous
        :return: None
        """
        # Si le résultat est affiché à l'écran, que C ait la même fonction que AC
        if self.did_tap_equal:
            button = 'AC'
        if button == 'C':
            # Sauter à cette fonction lorsqu'il n'y a pas d'élément dans 'cur_list'
            if not self.cur_list:
                return
            # Changer la formule et réafficher la formule modifiée
            self.cur_list.pop(-1)
            self.list_to_formula()
        if button == 'AC':
            # Réinitialiser tous les formula et résultat
            self.cur_list = []
            self.list_to_formula()
            self.result_str = ''
            self.result_affiche.set('0')
        # Réinitialiser le pointer à la dernière histoire
        self.pointer = self.nb_his + 1

    def press_equal(self):
        """
        Calculer et afficher le résultat
        :return : None
        """
        global j
        global nb_parenthese
        # Sauter à cette fonction lorsqu'il n'y a pas de formule de calcul
        if not self.cur_list:
            return
        # Calcul pour le cas rad/deg
        # cas rad
        if self.rd.get() == 'rad':
            self.formula_str_2 = self.formula_str

        try:
            # cas deg
            if self.rd.get() == 'deg':
                length_list = list(range(len(self.cur_list)))
                # Itérer sur chaque élément de la liste
                for i in length_list:
                    print(i)
                    nb_parenthese = 0  # Enregistrez le nombre de parenthèses
                    # Test d'existence des fonctions trigonométriques
                    if self.cur_list[i] in ['sin(', 'cos(', 'tan(']:
                        #
                        length_list.append(length_list[-1] + 1)
                        length_list.append(length_list[-1] + 1)
                        # après des fonctions trigonométriques, on ajoute un élément pour le transfert à une formule deg
                        self.cur_list.insert(i + 1, 'pi/180*(')
                        j = i + 2
                        # Trouver la position de l'insertion de parenthèse arrière
                        while nb_parenthese != -1:
                            if self.cur_list[j] in ['(', 'sin(', 'cos(', 'tan(']:
                                nb_parenthese += 1
                            if self.cur_list[j] == ')':
                                nb_parenthese -= 1
                            j += 1
                        self.cur_list.insert(j, ')')
                        nb_parenthese = 0
                # transfert la nouvelle formule à formula_str_2
                for elem in self.cur_list:
                    self.formula_str_2 += elem
                print(self.formula_str_2)

            # calcul et affichage de résultat
            self.result_float = eval(self.formula_str_2)
            self.result_str = str(format(self.result_float, '0.5f'))
        # Afficher "Formule incorrecte" si la formule est incorrecte
        except:
            self.result_str = 'Formule Incorrecte'
            self.result_affiche_str = self.formula_str + '=' + self.result_str
            self.result_affiche.set(self.result_affiche_str)
        # Si la formule est correcte, le résultat correct est affiché
        else:
            self.result_affiche_str = self.formula_str + '=' + self.result_str
            self.result_affiche.set(self.result_affiche_str)
        finally:
            # Générer l'histoire
            self.historiques.append(self.result_affiche_str)
            print(self.historiques)
            self.nb_his = len(self.historiques)
            self.pointer = self.nb_his - 1
            # reset parameters
            self.cur_list = []
            self.formula_str_2 = ''
            self.did_tap_equal = True

    def histoire(self, button):
        """
        Afficher l'historique
        :param button: [str], Correspond à "<--" et "-->" dans l'histoire.
        :return: None
        """
        # set pointer
        if button == 'go back':
            self.pointer -= 1
        if button == 'go on':
            self.pointer += 1
        if self.pointer > self.nb_his - 1:
            self.pointer = self.nb_his - 1
        if self.pointer < 0:
            self.pointer = 0
        # Sauter à cette fonction lorsqu'il n'y a pas d'historique
        if not self.historiques:
            return
        #  Affichage des résultats historiques
        self.result_affiche_str = self.historiques[self.pointer]
        self.result_affiche.set(self.result_affiche_str)

    def labels(self):
        """
        Afficher les labels
        :return: None
        """
        # Label de titre : 'calculatrice'
        self.__calculatrice = Label(text="calculatrice", font=('Calibri', 14), width=30, height=3)
        self.__calculatrice.pack()

        # Label de résultat
        self.__res = Label(textvariable=self.result_affiche, font=('Calibri', 16), anchor=SE, relief='sunken', bd=20)
        self.__res.place(x=20, y=70, width=380, height=70)

        # Label de rad/deg
        self.__rd = Label(textvariable=self.rd, font=('Calibri', 12), anchor=SE, relief='ridge', bd=3)
        self.__rd.place(x=350, y=40, width=35, height=30)

    def buttons(self):
        """
        Afficher les buttons
        :return: None
        """
        # Definition de couleur et taille de button
        num_bt, op_bt, egl_bt, cl_bt = "yellow", "cyan", "red", "green"
        bt_w, bt_h = 60, 60
        bt_font = tkinter.font.Font(family='Calibri', size=14)

        # La première ligne
        self.__bt_precedent = Button(self, text='←', font=bt_font, bg=op_bt, relief='raised', bd=16, command=lambda: self.histoire('go back'))
        self.__bt_precedent.place(x=20, y=160, width=bt_w, height=bt_h)
        self.__bt_suivant = Button(self, text='→', font=bt_font, bg=op_bt, relief='raised', bd=15, command=lambda: self.histoire('go on'))
        self.__bt_suivant.place(x=100, y=160, width=bt_w, height=bt_h)
        self.__bt_sin = Button(self, text='sin', font=bt_font, bg=op_bt, relief='raised', bd=15, command=lambda: self.press_num_operator('sin('))
        self.__bt_sin.place(x=180, y=160, width=bt_w, height=bt_h)
        self.__bt_cos = Button(self, text='cos', font=bt_font, bg=op_bt, relief='raised', bd=15, command=lambda: self.press_num_operator('cos('))
        self.__bt_cos.place(x=260, y=160, width=bt_w, height=bt_h)
        self.__bt_tan = Button(self, text='tan', font=bt_font, bg=op_bt, relief='raised', bd=15, command=lambda: self.press_num_operator('tan('))
        self.__bt_tan.place(x=340, y=160, width=bt_w, height=bt_h)

        # La deuxième ligne
        self.__bt_c = Button(self, text='C', font=bt_font, bg=cl_bt, relief='raised', bd=16, command=lambda: self.press_c_ac('C'))
        self.__bt_c.place(x=20, y=240, width=bt_w, height=bt_h)
        self.__bt_ac = Button(self, text='AC', font=bt_font, bg=cl_bt, relief='raised', bd=16, command=lambda: self.press_c_ac('AC'))
        self.__bt_ac.place(x=100, y=240, width=bt_w, height=bt_h)
        self.__bt_RD = Button(self, text='R/D', font=bt_font, bg=op_bt, relief='raised', bd=16, command=lambda: self.set_rd())
        self.__bt_RD.place(x=180, y=240, width=bt_w, height=bt_h)
        self.__bt_xcarre = Button(self, text='x²', font=bt_font, bg=op_bt, relief='raised', bd=16, command=lambda: self.press_num_operator('**2'))
        self.__bt_xcarre.place(x=260, y=240, width=bt_w, height=bt_h)
        self.__bt_racinex = Button(self, text='√x', font=bt_font, bg=op_bt, relief='raised', bd=16, command=lambda: self.press_num_operator('sqrt('))
        self.__bt_racinex.place(x=340, y=240, width=bt_w, height=bt_h)

        # La troisième ligne
        self.__bt_7 = Button(self, text='7', font=bt_font, bg=num_bt, relief='raised', bd=16, command=lambda: self.press_num_operator('7'))
        self.__bt_7.place(x=20, y=320, width=bt_w, height=bt_h)
        self.__bt_8 = Button(self, text='8', font=bt_font, bg=num_bt, relief='raised', bd=16, command=lambda: self.press_num_operator('8'))
        self.__bt_8.place(x=100, y=320, width=bt_w, height=bt_h)
        self.__bt_9 = Button(self, text='9', font=bt_font, bg=num_bt, relief='raised', bd=16, command=lambda: self.press_num_operator('9'))
        self.__bt_9.place(x=180, y=320, width=bt_w, height=bt_h)
        self.__bt_multi = Button(self, text='*', font=bt_font, bg=op_bt, relief='raised', bd=16, command=lambda: self.press_num_operator('*'))
        self.__bt_multi.place(x=260, y=320, width=bt_w, height=bt_h)
        self.__bt_dev = Button(self, text='/', font=bt_font, bg=op_bt, relief='raised', bd=16, command=lambda: self.press_num_operator('/'))
        self.__bt_dev.place(x=340, y=320, width=bt_w, height=bt_h)

        # La quatrième ligne
        self.__bt_4 = Button(self, text='4', font=bt_font, bg=num_bt, relief='raised', bd=16, command=lambda: self.press_num_operator('4'))
        self.__bt_4.place(x=20, y=400, width=bt_w, height=bt_h)
        self.__bt_5 = Button(self, text='5', font=bt_font, bg=num_bt, relief='raised', bd=16, command=lambda: self.press_num_operator('5'))
        self.__bt_5.place(x=100, y=400, width=bt_w, height=bt_h)
        self.__bt_6 = Button(self, text='6', font=bt_font, bg=num_bt, relief='raised', bd=16, command=lambda: self.press_num_operator('6'))
        self.__bt_6.place(x=180, y=400, width=bt_w, height=bt_h)
        self.__bt_plus = Button(self, text='+', font=bt_font, bg=op_bt, relief='raised', bd=16, command=lambda: self.press_num_operator('+'))
        self.__bt_plus.place(x=260, y=400, width=bt_w, height=bt_h)
        self.__bt_moins = Button(self, text='-', font=bt_font, bg=op_bt, relief='raised', bd=16, command=lambda: self.press_num_operator('-'))
        self.__bt_moins.place(x=340, y=400, width=bt_w, height=bt_h)

        # La cinquième ligne
        self.__bt_1 = Button(self, text='1', font=bt_font, bg=num_bt, relief='raised', bd=16, command=lambda: self.press_num_operator('1'))
        self.__bt_1.place(x=20, y=480, width=bt_w, height=bt_h)
        self.__bt_2 = Button(self, text='2', font=bt_font, bg=num_bt, relief='raised', bd=16, command=lambda: self.press_num_operator('2'))
        self.__bt_2.place(x=100, y=480, width=bt_w, height=bt_h)
        self.__bt_3 = Button(self, text='3', font=bt_font, bg=num_bt, relief='raised', bd=16, command=lambda: self.press_num_operator('3'))
        self.__bt_3.place(x=180, y=480, width=bt_w, height=bt_h)
        self.__bt_g_parenthese = Button(self, text='(', font=bt_font, bg=op_bt, relief='raised', bd=16, command=lambda: self.press_num_operator('('))
        self.__bt_g_parenthese.place(x=260, y=480, width=bt_w, height=bt_h)
        self.__bt_d_parenthese = Button(self, text=')', font=bt_font, bg=op_bt, relief='raised', bd=16, command=lambda: self.press_num_operator(')'))
        self.__bt_d_parenthese.place(x=340, y=480, width=bt_w, height=bt_h)

        # La sixième ligne
        self.__bt_0 = Button(self, text='0', font=bt_font, bg=num_bt, relief='raised', bd=16, command=lambda: self.press_num_operator('0'))
        self.__bt_0.place(x=20, y=560, width=bt_w, height=bt_h)
        self.__bt_point = Button(self, text='.', font=bt_font, bg=num_bt, relief='raised', bd=16, command=lambda: self.press_num_operator('.'))
        self.__bt_point.place(x=100, y=560, width=bt_w, height=bt_h)
        self.__bt_pi = Button(self, text='π', font=bt_font, bg=num_bt, relief='raised', bd=16, command=lambda: self.press_num_operator('pi'))
        self.__bt_pi.place(x=180, y=560, width=bt_w, height=bt_h)
        self.__bt_In = Button(self, text='In', font=bt_font, bg=op_bt, relief='raised', bd=16, command=lambda: self.press_num_operator('log('))
        self.__bt_In.place(x=260, y=560, width=bt_w, height=bt_h)
        self.__bt_eg = Button(self, text='=', font=bt_font, bg=egl_bt, relief='raised', bd=16, command=lambda: self.press_equal())
        self.__bt_eg.place(x=340, y=560, width=bt_w, height=bt_h)


if __name__ == '__main__':
    fenetre = Fenetre()
    fenetre.mainloop()


