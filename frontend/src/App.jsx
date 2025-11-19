import { useEffect, useMemo, useState } from "react";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export default function App() {
  const [jobs, setJobs] = useState([]);
  const [query, setQuery] = useState("Python");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchJobs();
  }, []);

  async function fetchJobs() {
    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/jobs`);
      const data = await response.json();
      setJobs(data);
    } catch (error) {
      console.error("Erro ao buscar vagas", error);
    } finally {
      setLoading(false);
    }
  }

  const filtered = useMemo(() => {
    const term = query.toLowerCase();
    return jobs.filter((job) => job.title.toLowerCase().includes(term));
  }, [jobs, query]);

  return (
    <main className="min-h-screen bg-slate-100 p-6">
      <header className="max-w-6xl mx-auto mb-8 flex flex-col gap-4">
        <h1 className="text-3xl font-bold text-slate-900">Agregador de Vagas</h1>
        <p className="text-slate-600">
          Automação de scraping, NLP e matching inteligente. Digite uma skill para filtrar.
        </p>
        <div className="flex gap-3">
          <input
            className="flex-1 rounded-md border border-slate-200 px-4 py-2"
            placeholder="Filtrar por skill..."
            value={query}
            onChange={(event) => setQuery(event.target.value)}
          />
          <button
            onClick={fetchJobs}
            className="rounded-md bg-primary px-4 py-2 font-semibold text-white"
          >
            Atualizar
          </button>
        </div>
      </header>

      <section className="max-w-6xl mx-auto grid gap-4 md:grid-cols-2">
        {loading ? (
          <div className="text-slate-500">Carregando vagas...</div>
        ) : (
          filtered.map((job) => <JobCard key={`${job.source}-${job.id}`} job={job} />)
        )}
      </section>
    </main>
  );
}

function JobCard({ job }) {
  return (
    <article className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex items-center justify-between text-sm text-slate-500">
        <span className="uppercase tracking-wide">{job.source}</span>
        {job.match_score && <span>Match {(job.match_score * 100).toFixed(0)}%</span>}
      </div>
      <h2 className="mt-2 text-xl font-semibold text-slate-900">{job.title}</h2>
      <p className="text-slate-600">{job.company}</p>
      <p className="text-sm text-slate-500">{job.location}</p>
      <p className="mt-4 line-clamp-3 text-sm text-slate-600">{job.description}</p>
      <a
        className="mt-4 inline-flex items-center text-primary"
        href={job.url}
        target="_blank"
        rel="noreferrer"
      >
        Ver vaga →
      </a>
    </article>
  );
}

