# AddAnkiCards
Um projeto, em construção, que adiciona cartões de matemática e inglês no Anki, com o intuito de auxiliar estudantes a dominar essas habilidades de forma gratuita e que melhore a qualidade do estudo dos mesmos.

# Interfaces:
## Main:
<img src="https://i.ibb.co/MBbC1Yp/Add-Anki-Cards-Main.png" alt="AddAnkiCards-Main" border="0">

## English:
### Make:
<img src="https://i.ibb.co/9gKn8r9/Add-Anki-Cards-Make-Cards-English.png" alt="AddAnkiCards-MakeCardsEnglish" border="0">

### Add:
<img src="https://i.ibb.co/CQ7L1rJ/Add-Anki-Cards-Add-English-Cards.png" alt="AddAnkiCards-AddEnglishCards" border="0">

## Math:
### Make:
<img src="https://i.ibb.co/fNNzV8R/Captura-de-tela-de-2024-08-13-15-33-54.png" alt="Captura-de-tela-de-2024-08-13-15-33-54" border="0">

### Add:
<img src="https://i.ibb.co/m8kKH71/Captura-de-tela-de-2024-08-13-15-34-17.png" alt="Captura-de-tela-de-2024-08-13-15-34-17" border="0">

## Modelo do Cartão de Matemática:
<img src="https://i.ibb.co/vqqHtyn/Captura-de-tela-de-2024-08-13-16-16-11.png" alt="Captura-de-tela-de-2024-08-13-16-16-11" border="0">

## Modelo do Cartão de Inglês:
### Frente:
<a href="https://ibb.co/qsxpgQP"><img src="https://i.ibb.co/R07c6wV/image.png" alt="image" border="0"></a>

### Verso:
<a href="https://ibb.co/hHGrbDQ"><img src="https://i.ibb.co/82yGq6v/image.png" alt="image" border="0"></a><br>

### Bibliotecas Usadas:
1. O programa adiciona os cartões através do <a href=https://git.foosoft.net/alex/anki-connect>Anki-Connect</a>;
2. Fazendo isso através da biblioteca <a href=https://docs.python-requests.org/en/latest/index.html>Requests</a>;
3. Além disso, utiliza a extensão cloze (Hide all) para formatar os cartões;
4. Usa a biblioteca <a href=https://pypi.org/project/gTTS>gTTS</a> para colocar os audios nos cartões;
5. O programa usa a biblioteca <a href=https://github.com/Akascape/CTkTable/tree/main>CTkTable</a> para mostrar certos tipos de dados dos cartões (licença MIT, autor: Akascape); e
6. A biblioteca <a href=https://github.com/TomSchimansky/CustomTkinter>Custom Tikinter</a>, para fazer a interface gráfica (licença MIT, autor: Tom Schimansky).