from tkinter import Tk, Button,Label,Scrollbar,Listbox,StringVar,DoubleVar,Entry,W,E,N,S,END
from tkinter import ttk
from tkinter import messagebox
from sqlConfig import dbConfig
import pypyodbc as pyo
import pandas as pd
import re
import os.path
from os import path

#cria conexão e cursor para usar o SQL Server
con = pyo.connect(**dbConfig)
cursor = con.cursor()

name_filter =[]
price_filter=[]
description_filter=[]
categories_filter=[]

class productsDB:
    #inicia conexão
    def __init__(self):
        self.con = pyo.connect(**dbConfig)
        self.cursor = con.cursor()
        print("Conexão bem sucedida")
        print(con)
    #encerra no fim do programa
    def __del__(self):
        self.con.close()
    #confere se existe a tabela products no SQL, cria uma caso não tenha
    def create_table_ifnot_exists(self):
        sql = """ IF  NOT EXISTS (SELECT * FROM sys.objects
                WHERE object_id = OBJECT_ID(N'[dbo].products') AND type in (N'U'))

                BEGIN
                CREATE TABLE [dbo].[products](
                    id int PRIMARY KEY IDENTITY(1,1),
                    name VARCHAR(255),
                    price VARCHAR(255),
                    description VARCHAR(255),
                    categories VARCHAR(255)
                )
                END """
        self.cursor.execute(sql)
        self.con.commit()

    #exibe todos os itens
    def view(self):
        self.cursor.execute("SELECT id, name, price, description, categories FROM products")
        rows = self.cursor.fetchall()
        return rows

    #adiciona novas entradas
    def insert(self,name, price, description, categories):
        sql=("INSERT INTO products(name, price, description, categories)VALUES (?,?,?,?)")
        values =[name, price, description, categories]
        self.cursor.execute(sql,values)
        self.con.commit()

    #edita entradas existentes
    def update(self, id, name, price, description, categories):
        tsql = 'UPDATE products SET  name = ?, price = ?, description = ?, categories = ? WHERE id=?'
        self.cursor.execute(tsql, [name, price, description, categories])
        self.con.commit()

    #exclui entradas
    def delete(self,id):
        delquery ='DELETE FROM products WHERE id = ?'
        self.cursor.execute(delquery, [id])
        self.con.commit()

#cria o evento de clicar na linha com o produto
def get_selected_row(event):
    global selected_tuple
    index = list_bx.curselection()[0]
    selected_tuple = list_bx.get(index)
    name_entry.delete(0, 'end')
    name_entry.insert('end', selected_tuple[1])
    price_entry.delete(0, 'end')
    price_entry.insert('end', selected_tuple[2])
    description_entry.delete(0, 'end')
    description_entry.insert('end', selected_tuple[3])
    categories_entry.delete(0, 'end')
    categories_entry.insert('end', selected_tuple[4])

#joga os itens na tela
def view_records():
    list_bx.delete(0, 'end')
    headers = ['Id', 'Nome', 'Preço', 'Descrição', 'Categorias']
    list_bx.insert(0, headers)

    print(name_filter)
    print(price_filter)
    print(description_filter)
    print(categories_filter)

    while("" in name_filter):
        name_filter.remove("")
    while("" in price_filter):
        price_filter.remove("")
    while("" in description_filter):
        description_filter.remove("")
    while("" in categories_filter):
        categories_filter.remove("")

    df = pd.DataFrame(db.view())
    if(len(name_filter) != 0) and (name_filter != ['']):
        df = df[df[1].isin(name_filter)]
    if(len(price_filter) != 0) and (price_filter != ['']):
        df = df[df[2].isin(price_filter)]
    if(len(description_filter) != 0) and (description_filter != ['']):
        df = df[df[3].isin(description_filter)]
    if(len(categories_filter) != 0) and (categories_filter != ['']):
        temp = pd.DataFrame()
        for index, row in df.iterrows():
            categories = row[4]
            categories = categories.split(",")
            print(categories)
            categories2 = set(categories)
            categories_filter2=set(categories_filter)
            if not categories_filter2.issubset(categories2):
                df.drop(index, inplace=True)

    for index, row in df.iterrows():
        list_bx.insert('end',list(row))


#pega os dados inseridos nas caixas de mensagens e insere um produto novo na tabela
def add_product():
    db.insert(name_text.get(),price_text.get(),description_text.get(),categories_text.get())
    list_bx.delete(0, 'end')
    list_bx.insert('end', (name_text.get(),price_text.get(),description_text.get(),categories_text.get()))
    name_entry.delete(0, "end")
    price_entry.delete(0, "end")
    description_entry.delete(0, "end")
    categories_entry.delete(0, "end")
    con.commit()
    messagebox.showinfo(title="Base de produtos",message="Novo produto adicionado.")

#pega os dados inseridos nas caixas de mensagens e insere um filtro novo na tabela
def add_filter():
    name_filter.append(name_text.get())
    price_filter.append(price_text.get())
    description_filter.append(description_text.get())
    categories_filter.append(categories_text.get())
    headers = ['Id', 'Nome', 'Preço', 'Descrição', 'Categorias']
    filter_bx.insert(0, headers)

    filter_bx.insert('end', (name_text.get(),price_text.get(),description_text.get(),categories_text.get()))
    name_entry.delete(0, "end")
    price_entry.delete(0, "end")
    description_entry.delete(0, "end")
    categories_entry.delete(0, "end")
    messagebox.showinfo(title="Base de produtos",message="Novo filtro adicionado.")



#exclui item
def delete_records():
    db.delete(selected_tuple[0])
    con.commit()
    messagebox.showinfo(title="Base de produtos",message="Produto excluido.")

#limpa a tela
def clear_screen():
    list_bx.delete(0,'end')
    name_entry.delete(0,'end')
    price_entry.delete(0,'end')
    description_entry.delete(0,'end')
    categories_entry.delete(0,'end')

#edita item
def update_records():
    db.update(selected_tuple[0], name_text.get(),price_text.get(),description_text.get(),categories_text.get())
    name_entry.delete(0, "end")
    price_text.delete(0, "end")
    description_text.delete(0, "end")
    categories_text.delete(0, "end")
    con.commit()
    messagebox.showinfo(title="Base de produtos",message="Produto atualizado.")

#exclui os filtros
def delete_filters():
    name_filter.clear()
    price_filter.clear()
    description_filter.clear()
    categories_filter.clear()
    filter_bx.delete(0,'end')

#encerra programa
def on_closing():
    dd = db
    if messagebox.askokcancel("Sair", "sair da aplicação?"):
        root.destroy()
        del dd

db = productsDB()
db.create_table_ifnot_exists()

#importa um csv com nome de produto que esteja no mesmo diretório do programa
def import_csv():
    if os.path.isfile('produtos.csv') == True:

        base_csv = pd.read_csv('produtos.csv')
        df = pd.DataFrame(base_csv)
        for index, row in df.iterrows():
            db.insert(row[0], "", "", "")
            con.commit()

    else:
        messagebox.showinfo(title="Arquivo faltando",message="Não foi encontrado o arquivo produtos.csv no diretório do programa")


root = Tk()

#configuraões gerais da GUI
root.title("Painel de Cadastro de Produtos")
root.configure(background="light green")
root.geometry("1200x500")
root.resizable(width=False,height=False)

#cria os heders e as caixas de entrada
name_label =ttk.Label(root,text="Nome",background="light green",font=("TkDefaultFont", 16))
name_label.grid(row=0, column=0, sticky=W)
name_text = StringVar()
name_entry = ttk.Entry(root,width=24,textvariable=name_text)
name_entry.grid(row=0, column=1, sticky=W)

price_label =ttk.Label(root,text="Preço",background="light green",font=("TkDefaultFont", 16))
price_label.grid(row=0, column=2, sticky=W)
price_text = StringVar()
price_entry = ttk.Entry(root,width=24,textvariable=price_text)
price_entry.grid(row=0, column=3, sticky=W)

description_label =ttk.Label(root,text="Descrição",background="light green",font=("TkDefaultFont", 16))
description_label.grid(row=0, column=4, sticky=W)
description_text = StringVar()
description_entry = ttk.Entry(root,width=24,textvariable=description_text)
description_entry.grid(row=0, column=5, sticky=W)

categories_label =ttk.Label(root,text="Categorias",background="light green",font=("TkDefaultFont", 14))
categories_label.grid(row=0, column=6, sticky=W)
categories_text = StringVar()
categories_entry = ttk.Entry(root,width=24,textvariable=categories_text)
categories_entry.grid(row=0, column=7, sticky=W)

list_bx = Listbox(root,height=16,width=40,font="helvetica 13",bg="light blue")
list_bx.grid(row=3,column=1, columnspan=3,sticky=W + E,pady=40,padx=15)
list_bx.bind('<<ListboxSelect>>',get_selected_row)

filter_bx = Listbox(root,height=16,width=40,font="helvetica 13",bg="light blue")
filter_bx.grid(row=3,column=5, columnspan=3,sticky=W + E,pady=40,padx=15)
filter_bx.bind('<<ListboxSelect>>',get_selected_row)

#barrinha de navegação
scroll_bar = Scrollbar(root)
scroll_bar.grid(row=1,column=4, rowspan=5,sticky=W )

list_bx.configure(yscrollcommand=scroll_bar.set)
scroll_bar.configure(command=list_bx.yview)


#cria os botões e os liga com as funções
add_btn = Button(root, text="Adicionar Produto",bg="blue",fg="white",font="helvetica 10 bold",command=add_product)
add_btn.grid(row=0, column=8, sticky=W)

add_filter = Button(root, text="Adicionar Filtro",bg="blue",fg="white",font="helvetica 10 bold",command=add_filter)
add_filter.grid(row=2, column=8, sticky=W)

modify_btn = Button(root, text="Editar",bg="purple",fg="white",font="helvetica 10 bold",command=update_records)
modify_btn.grid(row=15, column=4)

delete_btn = Button(root, text="Deletar",bg="red",fg="white",font="helvetica 10 bold",command=delete_records)
delete_btn.grid(row=15, column=5)

delete_btn = Button(root, text="Limpar Filtros",bg="red",fg="white",font="helvetica 10 bold",command=delete_filters)
delete_btn.grid(row=15, column=6)

view_btn = Button(root, text="Visualizar",bg="black",fg="white",font="helvetica 10 bold",command=view_records)
view_btn.grid(row=15, column=1)

clear_btn = Button(root, text="Limpar Tela",bg="maroon",fg="white",font="helvetica 10 bold",command=clear_screen)
clear_btn.grid(row=15, column=2)

exit_btn = Button(root, text="Sair",bg="blue",fg="white",font="helvetica 10 bold",command=root.destroy)
exit_btn.grid(row=15, column=3)

import_btn = Button(root, text="Importar Arquivo",bg="purple",fg="white",font="helvetica 10 bold",command=import_csv)
import_btn.grid(row=15, column=4)






root.mainloop()
