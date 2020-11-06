# Instalação
Para utilizar o programa é necessário instalado na máquina:
  -Python
  -SQL Server (2019)
  
Para o Python, são utilizados os seguintes pacotes:
  -pandas
  -virtualenv
  -pypyodbc

Para instalar os pacotes pandas e virtualenv basta utilizar o comando pip install (nome do pacote)

em seguida, no diretorio onde se encontra o projeto, digite o comando "virtualenv sqlserverenv" para criar um novo ambiente virtual

mude o diretorio para o da pasta sqlserverenv e utilize o comando scripts\activate

por fim, no diretorio sqlserverenv instale o pypyodbc com pip install pypyodbc

O arquivo sqlConfig.py contem as informações para conexão do SQL, é necessário abrir com um editor de texto e indicar o nome do Driver e o do Servidor.

Esse passo pode variar dependendo de suas configurações.

# Utilização
antes de iniciar o programa, certifique-se que a tabela a ser importada está no mesmo diretório do projeto, e que está com o nome 'produtos.csv'

Para iniciar o projeto, abra o prompt e, estando no diretorio do projeto, digite python cadastro.py

Para melhor navegação clique em "Visualizar" após cada alteração.

Os produtos cadastrados apareceram no bloco esquerdo, os filtros aplicados no bloco direito.

Para importar o arquivo CSV, clique no botão importar arquivo.

Para adicionar um produto, escreva nas caixas de texto as informações necessarias, e clique no botão de adicionar produto.

Para adicioanr um produto com mais de uma categoria, escreva as categorias deparadas por vírgulas e sem espaços.

para filtrar escreva o filtro nas mesmas caixas de texto e clique em adicionar um filtro, e depois clique em visualizar.

Os filtros são cumulativos, sendo possivel adicionar quantos quiser.

Para editar um deletar um produto, clique sobre ele e clique no botão respectivo.

