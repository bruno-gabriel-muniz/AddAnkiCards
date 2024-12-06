# AddAnkiCards

## Visão Geral / Overview
AddAnkiCards é uma ferramenta em desenvolvimento que facilita a criação e adição de cartões de estudo em inglês e matemática no Anki, ajudando estudantes a manter contato constante com o conteúdo de forma gratuita e personalizada.
<p>/<p>
AddAnkiCards is a tool under development that simplifies creating and adding study cards for English and math in Anki, helping students maintain consistent contact with content in a free and personalized way.
---

## Índice / Table of Contents
1. [Interfaces](#interfaces)
2. [Como Funciona](#como-funciona)
3. [Como Usar](#como-usar)
4. [Bibliotecas Usadas](#bibliotecas-usadas)

---

## Interfaces

### Main / Main
Interface principal do AddAnkiCards, onde o usuário pode acessar as funcionalidades principais do programa.
<p>/<p>
The main interface of AddAnkiCards, where users can access the program's primary functions.

<img src="https://i.ibb.co/MBbC1Yp/Add-Anki-Cards-Main.png" alt="AddAnkiCards-Main" border="0">

### English: Make / English: Make
Permite ao usuário criar cartões em inglês com frases e significados para revisões.
<p>/<p>
Allows users to create English cards with phrases and meanings for review.

<img src="https://i.ibb.co/9gKn8r9/Add-Anki-Cards-Make-Cards-English.png" alt="AddAnkiCards-MakeCardsEnglish" border="0">

### English: Add / English: Add
Adiciona os cartões de inglês criados diretamente ao Anki.
<p>/<p>
Adds the English cards created directly to Anki.

<img src="https://i.ibb.co/CQ7L1rJ/Add-Anki-Cards-Add-English-Cards.png" alt="AddAnkiCards-AddEnglishCards" border="0">

### Math: Make / Math: Make
Permite ao usuário criar cartões de operações matemáticas para treino.
<p>/<p>
Allows users to create math cards for practice.

<img src="https://i.ibb.co/fNNzV8R/Captura-de-tela-de-2024-08-13-15-33-54.png" alt="Captura-de-tela-de-2024-08-13-15-33-54" border="0">

### Math: Add / Math: Add
Adiciona os cartões de matemática criados diretamente ao Anki.
<p>/<p>
Adds the math cards created directly to Anki.

<img src="https://i.ibb.co/m8kKH71/Captura-de-tela-de-2024-08-13-15-34-17.png" alt="Captura-de-tela-de-2024-08-13-15-34-17" border="0">

---

## Como Funciona? / How Does It Work?

### English / English
A proposta do programa é facilitar o contato diário com a língua inglesa. Após uma leitura de textos em inglês, o programa ajuda a criar revisões diárias, que aumentam a retenção e fluência.
<p>/<p>
The program's aim is to make daily contact with the English language easier. After reading English texts, the program helps create daily reviews that enhance retention and fluency.

### Math / Math
A prática de operações matemáticas repetitivas ajuda o cérebro a se adaptar, tornando cálculos mentais mais rápidos e automáticos. O programa utiliza a revisão espaçada do Anki para ajudar na memorização dessas operações, apresentando-as de forma aleatória e personalizada.
<p>/<p>
The practice of repetitive mathematical operations helps the brain adapt, making mental calculations faster and more automatic. The program uses spaced repetition from Anki to help memorize these operations, presenting them in a random and personalized way.

---

## Como Usar? / How to Use?

### English / English
1. **Preparar o Anki**:
   - Instalar o Anki.
   - Instalar a extensão AnkiConnect (2055492159).
   - Instalar a extensão AwesomeTTS (1436550454).
   - Ativar nas configurações do baralho a opção de ocultar (primeira e segunda opções). [Vídeo de Referência](https://youtu.be/8fJfF5ezEUU?si=Mdo9wrct9rxVhvqw)

2. **Criar Cartões**:
   - Ler textos em inglês, com a menor ajuda possível de tradutores. Para garantir o aprendizado e o dominio do texto, antes das revisões. Pois, isso garante que as revisões sejam mais eficientes.
   - Inserir o prompt adequado no ChatGPT para criação das frases: ```Hello, I'm working on a language-related project, but I need your help to complete it. I will send you English texts followed by a numbers (indicating the number of sentences), and I would like you to create English sentences inspired by the text and translate them into Portuguese (according to the level and context of the text). The result should be displayed in the output and saved to a .txt file, separating the English sentences from their Portuguese equivalents with a semicolon (both on the same line) and using the '|' symbol to separate the sentences, which should all be on one line. Can you do this?```. E, logo em seguida, colocar os textos que você deseja praticar o seu inglês no ChatGPT seguido com o número de frases que você deseja criar.
   - Copiar a saída e adicionar no programa através da interface "Make Cards" de inglês.

3. **Adicionar Cartões ao Anki**:
   - Usar a aba "Add Cards" para enviar os cartões ao Anki (deixe o Anki aberto ao adicionar).
<p>/<p>

1. **Prepare Anki**:
   - Install Anki.
   - Install AnkiConnect (2055492159).
   - Install AwesomeTTS (1436550454).
   - Activate the first option in the deck settings to hide (first and second options). [Reference Video](https://youtu.be/8fJfF5ezEUU?si=Mdo9wrct9rxVhvqw)

2. **Create Cards**:
   - Read English texts, with the least possible help from translators. To ensure learning and mastery of the text, before reviews. Because this ensures that the reviews are more efficient.
   - Insert the appropriate prompt in ChatGPT to create phrases: ```Hello, I'm working on a language-related project, but I need your help to complete it. I will send you English texts followed by a numbers (indicating the number of sentences), and I would like you to create English sentences inspired by the text and translate them into Portuguese (according to the level and context of the text). The result should be displayed in the output and saved to a .txt file, separating the English sentences from their Portuguese equivalents with a semicolon (both on the same line) and using the '|' symbol to separate the sentences, which should all be on one line. Can you do this?```. And then, put the texts you want to practice your English after that with the number of phrases you want to create.
   - Copy the output and add it to the program through the "Make Cards" tab of English.

3. **Add Cards to Anki**:
   - Use the "Add Cards" tab to send cards to Anki (leave Anki open when adding).

### Math / Math
1. **Preparar o Anki**:
   - Instalar o Anki.
   - Instalar a extensão AnkiConnect (2055492159).
   - Instalar a extensão Cloze (Hide All) (1709973686).
   - Ativar a primeira opção de ocultação nas configurações do baralho. [Vídeo de Referência](https://youtu.be/8fJfF5ezEUU?si=Mdo9wrct9rxVhvqw)

2. **Criar Cartões de Matemática**:
   - Usar a interface "Make Cards" para definir intervalos, operações, e grupos de notas.

3. **Adicionar Cartões ao Anki**:
   - Acessar a aba "Add Cards" para adicionar as operações no Anki.
<p>/<p>

1. **Prepare Anki**:
   - Install Anki.
   - Install AnkiConnect (2055492159).
   - Install Cloze (Hide All) (1709973686).
   - Activate the first option in the deck settings to hide. [Reference Video](https://youtu.be/8fJfF5ezEUU?si=Mdo9wrct9rxVhvqw)

2. **Create Math Cards**:
   - Use the "Make Cards" interface to define intervals, operations, and note groups.

3. **Add Cards to Anki**:
   - Access the "Add Cards" tab to add operations to Anki.

---

## Bibliotecas Usadas / Used Libraries

1. **Requests** - Para comunicação com a API do AnkiConnect.
2. **gTTS** - Utilizada para gerar áudios nos cartões.
3. **CTkTable** - Exibe dados de cartões (MIT License, autor: Akascape).
4. **CustomTkinter** - Usada para a interface gráfica (MIT License, autor: Tom Schimansky).
5. **Cloze (Hide All)** - Extensão do Anki para ocultação de conteúdo em revisões.
<p>/<p>

1. **Requests** - For communication with the AnkiConnect API.
2. **gTTS** - Used to generate audio in the cards.
3. **CTkTable** - Displays card data (MIT License, author: Akascape).
4. **CustomTkinter** - Used for the graphical interface (MIT License, author: Tom Schimansky).
5. **Cloze (Hide All)** - Anki extension for hiding content in reviews.
