# Hero Management API

API REST para gerenciamento de heróis, ameaças e missões, desenvolvida com Python e Flask como parte do desafio **100 Dias de Código**.

O projeto tem como objetivo aplicar conceitos de desenvolvimento backend através de regras de negócio, relacionamentos entre entidades, gerenciamento de estados e consultas utilizando SQLAlchemy.

> 🚧 Projeto em desenvolvimento.
>
> A camada de services de missão está sendo finalizada. As rotas da API serão implementadas nas próximas etapas do projeto.

---

## 📌 Sobre o projeto

A Hero Management API simula um sistema responsável por gerenciar heróis, ameaças e as missões criadas para atendê-las.

Uma missão conecta um herói a uma ameaça e possui regras próprias para controlar quando ela pode ser criada, finalizada ou cancelada.

O projeto está sendo desenvolvido com foco no entendimento das regras de negócio e da relação entre os dados antes da exposição dessas funcionalidades através das rotas HTTP.

---

## 🛠️ Tecnologias utilizadas

- Python
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- Flask-JWT-Extended
- Flask-Migrate
- python-dotenv
- SQLite durante o desenvolvimento

---

## 🏗️ Estrutura atual

O sistema possui quatro entidades principais:

### Usuário

Responsável pela estrutura de usuários da aplicação.

Campos atuais:

- `id`
- `nome`
- `email`
- `senha_hash`
- `criado_em`

### Herói

Representa os heróis disponíveis para receber missões.

Campos atuais:

- `id`
- `nome`
- `codinome`
- `rank`
- `status`
- `latitude`
- `longitude`
- `criado_em`

Cada herói pode possuir várias missões.

### Ameaça

Representa uma ocorrência que poderá receber um herói.

Campos atuais:

- `id`
- `titulo`
- `descricao`
- `nivel`
- `status`
- `latitude`
- `longitude`
- `criado_em`

Cada ameaça pode estar relacionada a diferentes registros de missão ao longo do sistema.

### Missão

Responsável por relacionar um herói a uma ameaça.

Campos atuais:

- `id`
- `heroi_id`
- `ameaca_id`
- `status`
- `iniciada_em`
- `finalizada_em`

A entidade possui relacionamento com `Heroi` e `Ameaca`.

---

## 🔄 Estados da aplicação

### Rank dos heróis

- `C`
- `B`
- `A`
- `S`

### Status dos heróis

- `DISPONIVEL`
- `EM_MISSAO`
- `INATIVO`

### Nível das ameaças

- `C`
- `B`
- `A`
- `S`

### Status das ameaças

- `REGISTRADA`
- `EM_ATENDIMENTO`
- `RESOLVIDA`
- `CANCELADA`

### Status das missões

- `EM_ANDAMENTO`
- `CONCLUIDA`
- `CANCELADA`

---

## ⚙️ Regras de negócio implementadas

### Criação de missão

Antes da criação de uma missão, o sistema verifica:

- se o herói existe;
- se a ameaça existe;
- se o herói está disponível;
- se a ameaça está registrada;
- se o herói já possui uma missão em andamento;
- se a ameaça já está vinculada a outra missão em andamento;
- se o rank do herói é suficiente para enfrentar o nível da ameaça.

A hierarquia utilizada atualmente é:

```text
C = 1
B = 2
A = 3
S = 4