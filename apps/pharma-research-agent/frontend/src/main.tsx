import React, { useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import { Activity, Bot, FlaskConical, Network, Search, ShieldCheck } from "lucide-react";
import "./styles.css";

type SearchHit = {
  id: string;
  title: string;
  section: string;
  text: string;
  tags: string[];
  score: number;
  source: string;
};

type AgentStep = {
  name: string;
  role: string;
  output: string;
  citations: string[];
};

type ChatResponse = {
  answer: string;
  confidence: string;
  evidence: SearchHit[];
  agent_trace: AgentStep[];
  follow_up_questions: string[];
};

const starterQuestions = [
  "How should we triage EGFR resistance evidence for a new kinase series?",
  "Design a RAG workflow for ADME and assay notes.",
  "What risks should a hypothesis agent flag before proposing next experiments?"
];

async function postJson<T>(path: string, body: unknown): Promise<T> {
  const response = await fetch(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

function App() {
  const [question, setQuestion] = useState(starterQuestions[0]);
  const [context, setContext] = useState("Medicinal chemistry team comparing potency, selectivity, and ADME tradeoffs.");
  const [response, setResponse] = useState<ChatResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const citedIds = useMemo(
    () => new Set(response?.agent_trace.flatMap((step) => step.citations) ?? []),
    [response]
  );

  const runAgent = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await postJson<ChatResponse>("/api/chat", {
        question,
        project_context: context,
        top_k: 5
      });
      setResponse(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unexpected API error");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main>
      <section className="topbar">
        <div>
          <p className="eyebrow">Portfolio build for AI Data Engineer - LLMs / Agentic Systems</p>
          <h1>Pharma Research Agent Studio</h1>
        </div>
        <div className="status-pill">
          <Activity size={16} />
          RAG + agent workflow
        </div>
      </section>

      <section className="workspace">
        <aside className="query-panel">
          <div className="panel-title">
            <FlaskConical size={18} />
            Research prompt
          </div>
          <label>
            Scientist question
            <textarea value={question} onChange={(event) => setQuestion(event.target.value)} />
          </label>
          <label>
            Project context
            <textarea value={context} onChange={(event) => setContext(event.target.value)} />
          </label>
          <div className="prompt-list">
            {starterQuestions.map((item) => (
              <button key={item} type="button" onClick={() => setQuestion(item)}>
                {item}
              </button>
            ))}
          </div>
          <button className="primary-action" type="button" onClick={runAgent} disabled={isLoading}>
            <Search size={17} />
            {isLoading ? "Running..." : "Run agent"}
          </button>
          {error ? <p className="error">{error}</p> : null}
        </aside>

        <section className="results">
          <div className="answer-band">
            <div className="panel-title">
              <Bot size={18} />
              Grounded response
            </div>
            <p>{response?.answer ?? "Run the agent to retrieve evidence, synthesize guidance, and review research risks."}</p>
            {response ? <span className="confidence">Confidence: {response.confidence}</span> : null}
          </div>

          <div className="grid">
            <section className="trace">
              <div className="panel-title">
                <Network size={18} />
                Agent trace
              </div>
              {(response?.agent_trace ?? []).map((step) => (
                <article key={step.name} className="step">
                  <div>
                    <strong>{step.role}</strong>
                    <span>{step.name}</span>
                  </div>
                  <p>{step.output}</p>
                </article>
              ))}
            </section>

            <section className="evidence">
              <div className="panel-title">
                <ShieldCheck size={18} />
                Evidence
              </div>
              {(response?.evidence ?? []).map((hit) => (
                <article key={hit.id} className={citedIds.has(hit.id) ? "hit cited" : "hit"}>
                  <div className="hit-header">
                    <strong>{hit.title}</strong>
                    <span>{Math.round(hit.score * 100)}%</span>
                  </div>
                  <p>{hit.text}</p>
                  <div className="tags">
                    <span>{hit.id}</span>
                    <span>{hit.section}</span>
                    {hit.tags.slice(0, 3).map((tag) => (
                      <span key={tag}>{tag}</span>
                    ))}
                  </div>
                </article>
              ))}
            </section>
          </div>
        </section>
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

