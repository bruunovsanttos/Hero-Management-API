# Hero Management API

API REST para gerenciamento de heróis, ameaças e missões, desenvolvida com Python e Flask.

O projeto tem como objetivo aplicar conceitos de desenvolvimento backend através de regras de negócio, relacionamentos entre entidades, gerenciamento de estados e consultas utilizando SQLAlchemy.

> A V1 possui autenticação JWT, gerenciamento de missões e execução com Docker e Gunicorn. A API está publicada no Render, com PostgreSQL em produção.

API pública: [https://hero-management-api.onrender.com](https://hero-management-api.onrender.com).

---

## 📌 Sobre o projeto

A Hero Management API simula um sistema responsável por gerenciar heróis, ameaças e as missões criadas para atendê-las.

Uma missão conecta um herói a uma ameaça e possui regras próprias para controlar quando ela pode ser criada, finalizada ou cancelada.

O projeto está sendo desenvolvido com foco no entendimento das regras de negócio e da relação entre os dados, com essas funcionalidades expostas através de rotas HTTP organizadas em Blueprints.

---

## 🛠️ Tecnologias utilizadas

- Python
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- Flask-JWT-Extended
- Flask-Migrate / Alembic
- python-dotenv
- SQLite no desenvolvimento local e no Docker Compose
- PostgreSQL em produção, com Psycopg 3 (psycopg[binary])
- Docker / Docker Compose
- Gunicorn
- Render

---

## 🏗️ Estrutura atual

O sistema possui quatro entidades principais:

### Usuário

Responsável pelos usuários da aplicação, com cadastro, login e identificação através de JWT. As senhas são armazenadas como hash e não são retornadas pela API.

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
```

O rank do herói deve ser maior ou igual ao nível da ameaça.

Ao criar uma missão:

- a missão recebe o status `EM_ANDAMENTO`;
- o herói passa para `EM_MISSAO`;
- a ameaça passa para `EM_ATENDIMENTO`.

### Finalização de missão

Somente uma missão em andamento pode ser finalizada.

- A missão passa para `CONCLUIDA`.
- O herói volta a ficar `DISPONIVEL`.
- A ameaça passa para `RESOLVIDA`.
- A data de finalização é registrada em `finalizada_em`.

### Cancelamento de missão

Somente uma missão em andamento pode ser cancelada.

- A missão passa para `CANCELADA`.
- O herói volta a ficar `DISPONIVEL`.
- A ameaça volta para `REGISTRADA`, permitindo um novo atendimento.
- A data de encerramento é registrada em `finalizada_em`.

As alterações de cada operação são persistidas pelo serviço no banco de dados. Tentativas de finalizar ou cancelar uma missão já encerrada retornam conflito.

---

## 🗂️ Organização do projeto

A aplicação está organizada em três camadas principais:

### Models

Definem os campos, estados e relacionamentos das entidades no banco de dados.

### Services

Concentram as regras de negócio, as consultas e a persistência dos dados. Atualmente, existem serviços de autenticação e de missões.

### Routes / Blueprints

Recebem as requisições HTTP, chamam os serviços e retornam as respostas com os códigos correspondentes. As rotas de autenticação e de missões possuem seus próprios Blueprints.

```text
app/
├── models/
├── services/
├── routes/
├── extensions.py
└── __init__.py
migrations/
.env.example
.dockerignore
Dockerfile
compose.yaml
config.py
requirements.txt
run.py
```

---

## 🔐 Autenticação de usuários

### Cadastro — `POST /auth/cadastro` (público)

```json
{"nome":"Pessoa Exemplo","email":"pessoa@example.com","senha":"uma-senha-de-exemplo"}
```

Resposta `201`:

```json
{"id":1,"nome":"Pessoa Exemplo","email":"pessoa@example.com"}
```

Exige objeto JSON não vazio e campos textuais. Nome e email têm espaços externos removidos; email é convertido para minúsculas. Nome: até 120 caracteres; email: até 255, exatamente um `@`, partes não vazias e nenhum espaço. Campos vazios são rejeitados; a senha não pode conter apenas espaços. Não há tamanho mínimo de senha implementado. Senhas são armazenadas como hash pelo Werkzeug e nunca retornadas. Dados inválidos: `400`; email já cadastrado: `409` com `{"erro":"Email já cadastrado"}`.

### Login — `POST /auth/login` (público)

```json
{"email":"pessoa@example.com","senha":"uma-senha-de-exemplo"}
```

Resposta `200`: `{"access_token":"<JWT>"}`. Email tem espaços externos removidos e é convertido para minúsculas. Entrada inválida retorna `400`; credenciais incorretas retornam `401` com `{"erro":"Email ou senha inválidos"}`.

Envie o token nas rotas privadas:

```http
Authorization: Bearer <JWT>
```

O token identifica o usuário pelo `id` convertido em string. Sem sobrescrita na aplicação, o access token usa a validade padrão da extensão (15 minutos). Não há endpoints de refresh ou logout/revogação implementados.

### Usuário atual — `GET /auth/me` (JWT)

Retorna `200` com `{"id":1,"nome":"Pessoa Exemplo","email":"pessoa@example.com"}`. Consulta o usuário identificado pelo token no banco; usuário inexistente retorna `404` com `{"erro":"Usuário não encontrado"}`.

---

## 🌐 Rotas implementadas

| Método | Endpoint | Acesso | Sucesso |
|---|---|---|---|
| GET | /health | Público | 200 objeto de saúde |
| POST | /auth/cadastro | Público | 201 usuário |
| POST | /auth/login | Público | 200 access_token |
| GET | /auth/me | JWT | 200 usuário |
| GET | /missoes | Público | 200 lista |
| POST | /missoes | JWT | 201 missão |
| GET | /missoes/<id> | JWT | 200 missão |
| GET | /missoes/status/<status> | JWT | 200 lista |
| GET | /missoes/heroi/<id> | JWT | 200 lista |
| GET | /missoes/ameaca/<id> | JWT | 200 lista |
| PATCH | /missoes/<id>/finalizar | JWT | 200 missão |
| PATCH | /missoes/<id>/cancelar | JWT | 200 missão |

`GET /missoes` é público por decisão da V1, inclusive os IDs presentes na resposta. Consultas específicas e operações exigem JWT. Não há autorização por perfil nem verificação de propriedade da missão. As rotas de missões validam o JWT, mas não consultam a existência atual do usuário como `/auth/me` faz.

Não existem CRUDs `/herois` e `/ameacas`. Heróis e ameaças precisam existir no banco para criar missões; podem ser preparados via modelos no Flask shell. As funções de serviço `listar_missoes_heroi_por_status` e `listar_missoes_ameaca_por_status` não têm rotas registradas.

---

## 📋 Requisições e respostas de missões

Todos os IDs de caminho usam o conversor inteiro do Flask. Use `Content-Type: application/json` nos POSTs. A representação de missão retornada pelas rotas contém exatamente:

```json
{"id":1,"heroi_id":1,"ameaca_id":1,"status":"EM_ANDAMENTO"}
```

As listas retornam arrays dessa representação, ou `[]`. Datas não são expostas nas respostas atuais.

### Criar

`POST /missoes`, com JWT e corpo:

```json
{"heroi_id":1,"ameaca_id":1}
```

Retorna `201` com missão em andamento. Corpo vazio/não objeto: `400` com `{"erro":"Dados da missão não informados"}`. Campo ausente ou valor falso: `400` com `{"erro":"heroi_id e ameaca_id são obrigatórios"}`. Use IDs inteiros existentes; ainda não há validação explícita de tipo dos valores desses campos. Herói/ameaça inexistente: `404`. Conflito de negócio: `409`.

### Consultar

- `GET /missoes/<id>`: missão ou `404`, `{"erro":"Missão não encontrada"}`.
- `GET /missoes/status/<status>`: aceita exatamente `EM_ANDAMENTO`, `CONCLUIDA` ou `CANCELADA`; inválido retorna `400`, `{"erro":"Status de missão inválido"}`.
- `GET /missoes/heroi/<id>` e `/missoes/ameaca/<id>`: listas do recurso, `[]` quando existe sem missões, `404` quando o herói/ameaça não existe.

### Finalizar e cancelar

`PATCH /missoes/<id>/finalizar` ou `PATCH /missoes/<id>/cancelar`, com JWT, sem corpo obrigatório. Retornam `200` com missão `CONCLUIDA` ou `CANCELADA`. ID inexistente: `404`; missão já encerrada: `409`, `{"erro":"Missão não está em andamento"}`.

---

## 📄 Paginação

Apenas `GET /missoes` usa `page` e `per_page`: `GET /missoes?page=1&per_page=10`. Padrões da rota: 1 e 10. Retorno é somente um array, sem total, páginas ou links. Não há ordenação explícita. Os filtros não são paginados.

Texto não conversível para inteiro volta ao padrão da rota. Com `error_out=False`, página menor que 1 é normalizada para 1; `per_page` menor que 1 é normalizado para 20 pela biblioteca. Página além dos resultados retorna `200` e `[]`. A aplicação não define um limite próprio de `per_page`; não se deve assumir um teto de 100 nesta chamada a `Query.paginate`.

---

## 📡 Códigos HTTP

| Código | Uso |
|---|---|
| 200 | consultas, login, finalização e cancelamento |
| 201 | cadastro e criação de missão |
| 400 | entrada inválida ou status de missão inválido |
| 401 | JWT ausente/expirado ou credenciais incorretas |
| 404 | recurso inexistente |
| 409 | duplicidade de email ou conflito de negócio |
| 422 | JWT malformado ou assinatura inválida |

Erros dos serviços usam `{"erro":"..."}`. Erros padrão JWT usam `msg`: token ausente `{"msg":"Missing Authorization Header"}`; malformado testado `{"msg":"Not enough segments"}`; assinatura inválida `{"msg":"Signature verification failed"}`; expirado `{"msg":"Token has expired"}`.

Erros gerados pelo Flask podem vir em HTML: por exemplo, JSON sintaticamente inválido na criação de missão (`400`), tipo de conteúdo não JSON (`415`), URL não registrada (`404`) ou método não permitido (`405`). Não existe tratamento global que padronize todos os erros em JSON.

---

## 🚀 Como executar o projeto

### Variáveis de ambiente

O arquivo `.env.example` contém o modelo de configuração. No PowerShell, copie-o apenas se ainda não tiver um `.env`:

```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

Preencha o `.env` com os valores do seu ambiente antes de iniciar a aplicação:

| Variável | Uso |
|---|---|
| `SECRET_KEY` | Chave da aplicação Flask. Obrigatória; a aplicação não inicia se estiver ausente ou vazia. |
| `JWT_SECRET_KEY` | Chave usada para assinar os tokens JWT. Obrigatória; a aplicação não inicia se estiver ausente ou vazia. Use uma chave aleatória de pelo menos 32 bytes. |
| `DATABASE_URL` | URI de conexão com o banco. Na ausência da variável, usa `sqlite:///hero_management.db`. Em produção, configure a conexão PostgreSQL do ambiente. |

O `python-dotenv` carrega o `.env`. O arquivo local é ignorado pelo Git; `.env.example` é o modelo versionável. Mantenha nele apenas exemplos, sem chaves reais ou credenciais. No Render, configure os valores nas variáveis de ambiente do serviço.

O `config.py` converte URIs iniciadas por `postgresql://` para `postgresql+psycopg://`, selecionando Psycopg 3. URIs já iniciadas por `postgresql+psycopg://` são mantidas. O prefixo `postgres://` não é convertido pela configuração atual.

### Execução local

No PowerShell, na pasta do projeto, com Python instalado:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Após configurar o `.env`, use `DATABASE_URL=sqlite:///hero_management.db` para SQLite local e aplique as migrations:

```powershell
python -m flask --app run db upgrade
python run.py
```

Servidor de desenvolvimento: `http://127.0.0.1:5000`. `run.py` habilita debug; essa execução é destinada ao desenvolvimento. A URI SQLite relativa aponta para a pasta `instance/`.

### Execução com Docker Compose

Com Docker e Docker Compose disponíveis e o `.env` configurado:

```powershell
docker compose build
docker compose run --rm api python -m flask --app run db upgrade
docker compose up -d
```

A API fica disponível em `http://127.0.0.1:5001`. O `Dockerfile` usa Python 3.12 e inicia `gunicorn --bind 0.0.0.0:5000 run:app`. O Compose publica a porta 5000 do contêiner na porta 5001, acessível apenas pela interface local.

O serviço `api` carrega as chaves do `.env`, mas sobrescreve `DATABASE_URL` com `sqlite:////app/instance/hero_management.db`. O volume nomeado `dados_api` persiste o banco em `/app/instance`. O Compose atual não define um serviço PostgreSQL.

Para acompanhar a aplicação e encerrá-la:

```powershell
docker compose logs -f api
docker compose down
```

O comando `down` preserva o volume; a opção `-v` remove o volume e seus dados. O `.dockerignore` exclui arquivos de ambiente, bancos locais e o ambiente virtual da imagem.

### Migrations

Flask-Migrate integra o Alembic à aplicação. As revisões existentes em `migrations/` definem as tabelas de heróis, ameaças, missões e usuários. Aplique-as no banco selecionado por `DATABASE_URL`:

```powershell
python -m flask --app run db upgrade
python -m flask --app run db current
```

No Compose, com a API em execução:

```powershell
docker compose exec api python -m flask --app run db upgrade
docker compose exec api python -m flask --app run db current
```

Ao alterar modelos durante o desenvolvimento, gere uma revisão, confira o arquivo gerado e aplique-a:

```powershell
python -m flask --app run db migrate -m "descreve a alteracao do esquema"
python -m flask --app run db upgrade
```

O diretório de migrations já existe; não é necessário executar `db init`. A inicialização da aplicação e o comando padrão do Docker não executam migrations automaticamente.

### Produção no Render

A API está publicada em [https://hero-management-api.onrender.com](https://hero-management-api.onrender.com), usando PostgreSQL com Psycopg 3 em produção.

A configuração de produção usa `SECRET_KEY`, `JWT_SECRET_KEY` e `DATABASE_URL` nas variáveis de ambiente do serviço. O Gunicorn carrega a aplicação por `run:app`; a imagem Docker escuta em `0.0.0.0:5000`. Configure `/health` como caminho de verificação de saúde do serviço.

As migrations devem ser aplicadas ao banco de produção com `python -m flask --app run db upgrade`, em um ambiente com acesso ao banco e às variáveis do serviço. O repositório não contém `render.yaml` nem uma etapa automática de migrations no `Dockerfile`; os ajustes do serviço no painel do Render não são definidos por esses arquivos.

---

## 🧪 Verificação da aplicação

O endpoint público `GET /health` retorna `200` com:

```json
{"message":"Hero Management API funcionando","status":"online"}
```

No PowerShell:

```powershell
# Execução local
Invoke-RestMethod http://127.0.0.1:5000/health

# Docker Compose
Invoke-RestMethod http://127.0.0.1:5001/health

# Produção
Invoke-RestMethod https://hero-management-api.onrender.com/health
```

Essa rota confirma que a aplicação responde, mas não consulta o banco de dados. A cópia atual do projeto não contém uma suíte em `tests/` nem relatórios em `docs/`.

---

## 📌 Limitações atuais

- As rotas protegidas exigem JWT, sem autorização por perfil ou propriedade da missão.
- A paginação não define limite próprio, ordenação explícita ou metadados; os filtros não são paginados.
- Os IDs recebidos no corpo de criação de missão não possuem validação explícita de tipo, e os erros HTTP não são todos padronizados em JSON.
- Não há refresh ou revogação de tokens. As rotas de missões não verificam se o usuário do token ainda existe; `/auth/me` faz essa consulta.
