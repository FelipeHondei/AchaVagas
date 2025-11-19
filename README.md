## Job Aggregator

Agregador de vagas com scraping, NLP e envio automático de resumos diários.

### Arquitetura

- **Backend**: FastAPI + SQLAlchemy + Celery/Redis
- **Banco**: PostgreSQL
- **Scraping**: BeautifulSoup, requests e Selenium (quando necessário)
- **NLP/Matching**: spaCy (ou Hugging Face/OpenAI opcional)
- **Frontend**: Dashboard React simples (Vite) com Tailwind CDN
- **Infra**: Docker Compose orquestra API, worker, beat, Redis, PostgreSQL e frontend estático

```
job-aggregator/
├── backend/
│   ├── scrapers/
│   ├── services/
│   ├── models/
│   ├── api/
│   ├── tasks/
│   └── config.py
├── frontend/
├── docker-compose.yml
└── README.md
```

### Fluxo principal

1. Celery agenda scraping periódico (`fetch_latest_jobs`)
2. Scrapers coletam vagas (LinkedIn, Indeed, GitHub Jobs, Gupy) e armazenam em PostgreSQL
3. Serviço de NLP extrai habilidades e pontua cada vaga vs perfil do usuário
4. Matching Service gera ranking e salva aplicações sugeridas
5. Notification Service consolida top matches e envia email diário
6. Frontend consulta API (`/jobs`, `/matches`, `/profile`)

### Desenvolvimento local

```bash
cd job-aggregator
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt
cp backend/.env.example backend/.env
uvicorn backend.api.routes:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

### Variáveis esperadas (`backend/.env`)

```
POSTGRES_USER=jobs
POSTGRES_PASSWORD=jobs
POSTGRES_DB=jobs
DATABASE_URL=postgresql+psycopg2://jobs:jobs@db:5432/jobs
REDIS_URL=redis://redis:6379/0
EMAIL_HOST=smtp.mailgun.org
EMAIL_PORT=587
EMAIL_USER=apikey
EMAIL_PASSWORD=xxxx
EMAIL_FROM=no-reply@example.com
OPENAI_API_KEY=
SPACY_MODEL=pt_core_news_md
```

### Testes

```bash
pytest backend/tests
```

### Próximos passos

- Implementar autenticação JWT para múltiplos perfis
- Adicionar interface avançada com filtros
- Integrar provedores adicionais (Glassdoor, InfoJobs) e modelos LLM para ranking semântico

