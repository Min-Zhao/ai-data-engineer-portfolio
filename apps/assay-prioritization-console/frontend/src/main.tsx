import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import { FlaskConical, SlidersHorizontal } from "lucide-react";
import "./styles.css";

type Assay = {
  id: string;
  name: string;
  target: string;
  cost: number;
  turnaround_days: number;
  confidence: number;
  decision_value: number;
  priority_score: number;
  rationale: string;
  risk: string;
};
type Response = { selected: Assay[]; deferred: Assay[]; summary: string; operating_constraints: string[] };

function AssayTable({ title, assays }: { title: string; assays: Assay[] }) {
  return (
    <section>
      <h2>{title}</h2>
      {assays.map((assay) => (
        <article key={assay.id}>
          <div className="row">
            <strong>{assay.name}</strong>
            <span>{Math.round(assay.priority_score * 100)} score</span>
          </div>
          <p>{assay.rationale}</p>
          <small>{assay.id} · {assay.target} · ${assay.cost.toLocaleString()} · {assay.turnaround_days} days</small>
        </article>
      ))}
    </section>
  );
}

function App() {
  const [budget, setBudget] = useState(30000);
  const [days, setDays] = useState(14);
  const [target, setTarget] = useState("EGFR");
  const [data, setData] = useState<Response | null>(null);

  async function run() {
    const response = await fetch("/api/prioritize", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ budget, max_turnaround_days: days, target })
    });
    setData(await response.json());
  }

  return (
    <main>
      <header>
        <FlaskConical />
        <div>
          <p>Decision support for discovery operations</p>
          <h1>Assay Prioritization Console</h1>
        </div>
      </header>
      <aside>
        <label>Target <input value={target} onChange={(event) => setTarget(event.target.value)} /></label>
        <label>Budget <input type="number" value={budget} onChange={(event) => setBudget(Number(event.target.value))} /></label>
        <label>Max days <input type="number" value={days} onChange={(event) => setDays(Number(event.target.value))} /></label>
        <button onClick={run}><SlidersHorizontal size={18} /> Prioritize</button>
      </aside>
      {data ? <p className="summary">{data.summary}</p> : null}
      <div className="grid">
        <AssayTable title="Selected" assays={data?.selected ?? []} />
        <AssayTable title="Deferred" assays={data?.deferred ?? []} />
      </div>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(<App />);

