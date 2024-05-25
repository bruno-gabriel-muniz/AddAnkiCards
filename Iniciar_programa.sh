# Entrando na pasta do projeto
cd '/home/bruno/Área de Trabalho/AddCardsAnkiProject/Treino-Ingles'
# entrando no ambiente virtual do projeto
source VenvAddAnkiCards/bin/activate
# evitando um bug da biblioteca xerox
xhost +local:$USER
# rodando o programa principal
python3 "Interface/InterfaceMain.py"