"use client";

import { useMemo, useState } from "react";

type Kind = "Try this" | "Learn this" | "Real-world solution";
type Signal = { id: number; title: string; kind: Kind; source: string; score: number; summary: string; why: string; action: string; tags: string[] };

const topics = ["AI agents", "Python", "RAG", "Vector search", "Web apps"];
const signals: Signal[] = [
  { id: 1, title: "A practical reliability pattern for long-running AI agent tasks", kind: "Try this", source: "GitHub release", score: 94, summary: "A release adds checkpoints, retry handling, and recoverable state for multi-step agent workflows.", why: "It overlaps with your focus on Python and AI-agent workflows.", action: "Compare its checkpoint approach with the workflow state SignalStack will need.", tags: ["AI agents", "Python"] },
  { id: 2, title: "Evaluation-driven retrieval reduces irrelevant RAG answers", kind: "Learn this", source: "Research paper", score: 91, summary: "A research approach measures retrieval quality before generation, revealing weak evidence early.", why: "SignalStack needs accurate semantic matching and transparent recommendations.", action: "Use these ideas for recommendation-quality tests.", tags: ["RAG", "Vector search"] },
  { id: 3, title: "How an engineering team kept a high-volume feed fresh without duplicates", kind: "Real-world solution", source: "Engineering blog", score: 88, summary: "The team combined content fingerprints, source rules, and freshness windows to prevent duplicate updates.", why: "It addresses the same ingestion and deduplication problem SignalStack faces.", action: "Review its trade-offs before choosing the first ingestion strategy.", tags: ["Python", "Web apps"] },
  { id: 4, title: "A new embedding model targets technical documentation search", kind: "Try this", source: "Official release", score: 85, summary: "The model specializes in technical vocabulary, code-adjacent text, and dense documentation.", why: "It may improve matching between a user profile and technical source material.", action: "Compare it offline against a general embedding model.", tags: ["Vector search", "RAG"] }
];
const filters: Array<Kind | "All"> = ["All", "Try this", "Learn this", "Real-world solution"];

export default function Home() {
  const [profileReady, setProfileReady] = useState(false);
  const [resumeName, setResumeName] = useState("");
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [resumeSummary, setResumeSummary] = useState("");
  const [github, setGithub] = useState("");
  const [githubSummary, setGithubSummary] = useState("");
  const [building, setBuilding] = useState(false);
  const [question, setQuestion] = useState("");
  const [ragAnswer, setRagAnswer] = useState("");
  const [ragSources, setRagSources] = useState<Array<{ title: string; source: string; url: string }>>([]);
  const [asking, setAsking] = useState(false);
  const [filter, setFilter] = useState<(typeof filters)[number]>("All");
  const [activeTopics, setActiveTopics] = useState(topics);
  const [saved, setSaved] = useState<number[]>([]);
  const [selected, setSelected] = useState<Signal | null>(null);
  const shown = useMemo(() => signals.filter(s => (filter === "All" || s.kind === filter) && s.tags.some(t => activeTopics.includes(t))), [filter, activeTopics]);
  const toggleTopic = (topic: string) => setActiveTopics(current => current.includes(topic) ? current.filter(t => t !== topic) : [...current, topic]);
  const toggleSaved = (id: number) => setSaved(current => current.includes(id) ? current.filter(x => x !== id) : [...current, id]);
  async function buildProfile() {
    setBuilding(true);
    if (resumeFile) {
      const form = new FormData();
      form.append("file", resumeFile);
      const response = await fetch("http://127.0.0.1:8000/profile/resume", { method: "POST", body: form });
      const data = await response.json();
      if (response.ok) {
        const skills = data.analysis.skills as string[];
        const suggestedTopics = data.analysis.suggested_topics as string[];
        setResumeSummary(`${skills.length ? skills.slice(0, 6).join(", ") : "Technical experience detected"} · ${data.analysis.projects.length} project signals found`);
        setActiveTopics(current => [...new Set([...current, ...skills, ...suggestedTopics.map((topic: string) => topic.replace(/^./, (letter: string) => letter.toUpperCase()))])]);
      } else {
        setResumeSummary(data.detail || "Resume could not be analyzed. You can still continue.");
      }
    }
    if (github.trim()) {
      const response = await fetch(`/api/github?username=${encodeURIComponent(github.trim().replace(/^@/, ""))}`);
      const data = await response.json();
      setGithubSummary(data.ok ? `${data.name} · ${data.publicRepos} public repositories · ${data.topLanguages.join(", ") || "no languages found"}` : "GitHub profile could not be found. You can still continue.");
    }
    setBuilding(false);
    setProfileReady(true);
  }
  async function askSignalStack() {
    if (!question.trim()) return;
    setAsking(true);
    setRagAnswer("");
    const response = await fetch("http://127.0.0.1:8000/rag/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, profile: { topics: activeTopics, skills: activeTopics } })
    });
    const data = await response.json();
    setRagAnswer(response.ok ? data.answer : data.detail || "The research service is unavailable.");
    setRagSources(response.ok ? data.sources : []);
    setAsking(false);
  }
  if (!profileReady) return <main className="shell onboarding"><header><a className="brand" href="#top"><b>S</b>SignalStack</a><span className="updated"><i />Private by design</span></header><section className="setup-card" id="top"><p className="eyebrow">Set up your signal profile</p><h1>Tell us what you work with, once.</h1><p>SignalStack uses your resume, public GitHub work, and technical interests to make your tech feed relevant from the first briefing.</p><label className="upload"><input type="file" accept=".pdf,.txt" onChange={event => { const file = event.target.files?.[0] || null; setResumeFile(file); setResumeName(file?.name || ""); }} /><b>{resumeName ? "✓ Resume attached" : "Upload your resume"}</b><span>{resumeName || "PDF or TXT · analyzed locally by the SignalStack profile API"}</span></label><label className="field">GitHub username <input value={github} onChange={event => setGithub(event.target.value)} placeholder="e.g. mukulmeena" /></label><label className="field">What are you interested in right now? <textarea defaultValue="AI agents, Python, RAG, vector search, web apps" /></label><button className="build-button" onClick={buildProfile} disabled={building}>{building ? "Building your profile…" : "Build my tech profile →"}</button><small>GitHub is optional. We only read public profile and repository information in this first version.</small></section></main>;
  return <main className="shell">
    <header><a className="brand" href="#top"><b>S</b>SignalStack</a><span className="updated"><i />Briefing updated now</span><button className="avatar">M</button></header>
    <section id="top" className="hero"><div><p className="eyebrow">Your tech briefing</p><h1>Only the tech signals that matter to your work.</h1><p>SignalStack brings together trusted technical sources, then explains why each update is relevant to you and what you can do with it.</p>{resumeName && <p className="profile-note">✓ Resume analyzed: {resumeName}{resumeSummary ? ` · ${resumeSummary}` : ""}</p>}{githubSummary && <p className="profile-note">✓ GitHub assessed: {githubSummary}</p>}</div><div className="score"><span>Briefing quality</span><strong>94%</strong><small>Based on your current focus</small></div></section>
    <div className="layout"><aside><p className="eyebrow">Your focus</p><h2>What SignalStack is using</h2><p>Adjust these topics anytime. Your briefing updates immediately.</p><div className="topics">{topics.map(topic => <button className={activeTopics.includes(topic) ? "on" : ""} onClick={() => toggleTopic(topic)} key={topic}>{activeTopics.includes(topic) ? "✓" : "+"} {topic}</button>)}</div><footer>Watching<br /><b>GitHub · Research · Engineering · Releases</b></footer></aside>
    <section className="feed"><div className="feed-top"><div><p className="eyebrow">Today</p><h2>Recommended for you</h2><p>{shown.length} high-relevance signals found</p></div><span>Saved <b>{saved.length}</b></span></div><nav>{filters.map(item => <button className={filter === item ? "active" : ""} onClick={() => setFilter(item)} key={item}>{item}</button>)}</nav><div className="cards">{shown.map(signal => <article key={signal.id}><div className="meta"><span className={signal.kind.toLowerCase().replaceAll(" ", "-")}>{signal.kind}</span><span>{signal.source}</span><em>High confidence · {signal.score}%</em></div><h3>{signal.title}</h3><p>{signal.summary}</p><div className="actions"><button onClick={() => setSelected(signal)}>Why you&apos;re seeing this →</button><button className="save" onClick={() => toggleSaved(signal.id)}>{saved.includes(signal.id) ? "Saved" : "Save"}</button></div></article>)}{shown.length === 0 && <div className="empty">No signals match this view. Add a focus area or select another filter.</div>}</div></section></div>
    <section className="trust"><div><b>Not popularity-ranked.</b> Relevance, source quality, freshness, and feedback decide what you see.</div><div><b>Real-world context.</b> Engineering solutions appear alongside research and releases.</div><div><b>Always explainable.</b> Every recommendation has a visible reason.</div></section>
    <section className="ask-panel"><div><p className="eyebrow">Ask your technical sources</p><h2>Get an evidence-grounded answer.</h2><p>SignalStack retrieves matching GitHub, research, release, and engineering sources before responding.</p></div><div className="ask-form"><textarea value={question} onChange={event => setQuestion(event.target.value)} placeholder="Example: How should I make an AI-agent workflow more reliable?" /><button className="build-button" onClick={askSignalStack} disabled={asking}>{asking ? "Retrieving evidence…" : "Ask SignalStack →"}</button>{ragAnswer && <div className="rag-result"><b>Grounded answer</b><p>{ragAnswer}</p>{ragSources.length > 0 && <div className="rag-sources">{ragSources.map(source => <a href={source.url} target="_blank" rel="noreferrer" key={source.title}>{source.source}: {source.title} ↗</a>)}</div>}</div>}</div></section>
    {selected && <div className="modal-bg" onClick={() => setSelected(null)}><section className="modal" onClick={e => e.stopPropagation()}><button className="close" onClick={() => setSelected(null)}>×</button><p className="eyebrow">Why you&apos;re seeing this</p><h2>{selected.title}</h2><div><b>Profile match</b><p>{selected.why}</p></div><div><b>Suggested next step</b><p>{selected.action}</p></div></section></div>}
  </main>;
}
