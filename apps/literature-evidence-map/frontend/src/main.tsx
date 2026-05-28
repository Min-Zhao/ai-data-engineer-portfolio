import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import { BookOpen, GitBranch, Search } from "lucide-react";
import "./styles.css";

type Paper = {
  id: string;
  title: string;
  therapeutic_area: string;
  abstract: string;
  mechanisms: string[];
  biomarkers: string[];
  evidence_level: string;
};

type Cluster = { label: string; paper_ids: string[]; rationale: string };
type Response = { papers: Paper[]; clusters: Cluster[]; gaps: string[] };

function App() {
  const [query, setQuery] = useState("checkpoint resistance interferon biomarker");
  const [data, setData] = useState<Response | null>(null);
  const [loading, setLoading] = useState(false);

  async function run() {
    setLoading(true);
    const response = await fetch("/api/evidence", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query })
    });
    setData(await response.json());
    setLoading(false);
  }

  return (
    <main>
      <header>
        <BookOpen />
        <div>
          <p>Scientific literature intelligence</p>
          <h1>Literature Evidence Map</h1>
        </div>
      </header>
      <section className="searchbar">
        <input value={query} onChange={(event) => setQuery(event.target.value)} />
        <button onClick={run} disabled={loading}>
          <Search size={18} />
          {loading ? "Mapping" : "Map evidence"}
        </button>
      </section>
      <section className="layout">
        <div>
          <h2>Papers</h2>
          {(data?.papers ?? []).map((paper) => (
            <article key={paper.id}>
              <strong>{paper.title}</strong>
              <p>{paper.abstract}</p>
              <span>{paper.id} · {paper.therapeutic_area} · {paper.evidence_level}</span>
            </article>
          ))}
        </div>
        <div>
          <h2><GitBranch size={18} /> Evidence clusters</h2>
          {(data?.clusters ?? []).map((cluster) => (
            <article key={cluster.label}>
              <strong>{cluster.label}</strong>
              <p>{cluster.rationale}</p>
              <span>{cluster.paper_ids.join(", ")}</span>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(<App />);

