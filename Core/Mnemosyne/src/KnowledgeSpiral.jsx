
import React, { useMemo, useRef, useState, useEffect } from "react";
import ForceGraph2D from "react-force-graph-2d";

// Minimal UI: basic buttons and inputs without external UI library
function uid(){ return Math.random().toString(36).slice(2,10); }
const STOP = new Set(["the","and","with","that","this","from","into","your","about","there","their","then","have","more","than","over","under","between","while","where","what","when","which","would","could","should","shall","might","like","just","also","very","much","even","into","onto","for","are","was","were","will","can","cant","cannot","is","be","to","of","in","on","a","an","it","as","by","or","if","we","you","they","i"]);

function tokenize(text){
  return text.toLowerCase().replace(/[^a-z0-9\s#\-]/g," ").split(/\s+/).filter(Boolean);
}
function keywords(text){
  const toks = tokenize(text);
  return Array.from(new Set(toks.filter((t)=>!STOP.has(t) && (t.length>3 || t.startsWith("#"))))).slice(0,12);
}
function detectIntent(text){
  const t = text.toLowerCase();
  if (/^q[:?]/.test(t) || /\?$/.test(t)) return "question";
  if (/(we\s+should|let's|i will|plan to|roadmap|action)/.test(t)) return "proposal";
  if (/(hypothesis|i think|maybe|could be|might be)/.test(t)) return "hypothesis";
  if (/(learned|tested|result|because|therefore|so\s+we)/.test(t)) return "insight";
  return "observation";
}
function intentColor(intent){
  switch(intent){
    case "question": return "#fde68a";
    case "proposal": return "#bbf7d0";
    case "hypothesis": return "#bae6fd";
    case "insight": return "#e9d5ff";
    default: return "#e5e7eb";
  }
}
function consensusScore(votes){
  if(!votes||votes.length===0) return 0;
  const avg = votes.reduce((acc,v)=>({ benefit: acc.benefit+(v.benefit||0), effort: acc.effort+(v.effort||0), risk: acc.risk+(v.risk||0) }), {benefit:0, effort:0, risk:0});
  const n = votes.length;
  const b = avg.benefit / n / 10;
  const e = avg.effort / n / 10;
  const r = avg.risk / n / 10;
  return Math.max(0, Math.min(1, (b*0.6 + (1-e)*0.3 + (1-r)*0.1)));
}
function storageKey(roomId){ return `knowledge_spiral:${roomId}`; }

export default function KnowledgeSpiral(){
  const [roomId, setRoomId] = useState(()=> localStorage.getItem("ks:room") || "default-room");
  const [entries, setEntries] = useState([]);
  const [edges, setEdges] = useState([]);
  const [text, setText] = useState("");
  const [autoLink, setAutoLink] = useState(true);
  const [threshold, setThreshold] = useState(0.2);
  useEffect(()=>{
    localStorage.setItem("ks:room", roomId);
    const data = localStorage.getItem(storageKey(roomId));
    if(data){
      try{
        const p = JSON.parse(data);
        setEntries(p.entries||[]);
        setEdges(p.edges||[]);
      }catch(e){
        console.warn("parse fail", e);
      }
    } else { setEntries([]); setEdges([]); }
  }, [roomId]);
  useEffect(()=>{ localStorage.setItem(storageKey(roomId), JSON.stringify({entries, edges}) ); }, [entries, edges, roomId]);

  function uidLocal(){ return uid(); }
  function addEntry(raw){
    if(!raw.trim()) return;
    const id = uidLocal();
    const k = keywords(raw);
    const intent = detectIntent(raw);
    const node = { id, text: raw.trim(), intent, tags: k, createdAt: new Date().toISOString(), votes: [] };
    const newEdges = [];
    if(autoLink){
      for(const other of entries){
        const sim = jaccard(k, other.tags || []);
        if(sim >= threshold) newEdges.push({ source: node.id, target: other.id, weight: Number(sim.toFixed(3)), reason: `keyword_overlap:${sim.toFixed(2)}`});
        const comp = complementaryIntent(intent, other.intent);
        if(comp) newEdges.push({ source: node.id, target: other.id, weight: 0.15, reason: `intent:${intent}↔${other.intent}`});
      }
    }
    setEntries((e)=> [node, ...e]);
    setEdges((ed)=> [...newEdges, ...ed]);
    setText("");
  }
  function jaccard(a,b){ const A=new Set(a), B=new Set(b); const inter=[...A].filter(x=>B.has(x)).length; const union=new Set([...a,...b]).size; return union? inter/union : 0; }
  function complementaryIntent(a,b){ const pairs = new Set(["question:insight","proposal:insight","proposal:observation","hypothesis:insight","question:proposal"]); return pairs.has(`${a}:${b}`)||pairs.has(`${b}:${a}`); }
  function removeNode(id){ setEntries((e)=>e.filter(n=>n.id!==id)); setEdges((ed)=>ed.filter(l=>l.source!==id && l.target!==id)); }
  function exportRoom(){ const blob = new Blob([JSON.stringify({roomId, entries, edges},null,2)], {type:"application/json"}); const url=URL.createObjectURL(blob); const a=document.createElement("a"); a.href=url; a.download=`ks-room-${roomId}-${new Date().toISOString().slice(0,10)}.json`; a.click(); URL.revokeObjectURL(url); }
  function importRoom(file, options={merge:false}){ const reader=new FileReader(); reader.onload=()=>{ try{ const data = JSON.parse(String(reader.result)); if(!options.merge){ setEntries(data.entries||[]); setEdges(data.edges||[]); } else { const existing = new Map(entries.map(n=>[n.id,n])); for(const n of data.entries||[]) existing.set(n.id,n); const links = new Map(edges.map(l=>[l.source+'::'+l.target,l])); for(const l of data.edges||[]) links.set(l.source+'::'+l.target,l); setEntries([...existing.values()]); setEdges([...links.values()]); } }catch(e){ alert("Invalid JSON"); } }; reader.readAsText(file); }
  function vote(nodeId, voterId, vote){ setEntries((list)=> list.map((n)=>{ if(n.id!==nodeId) return n; const others = (n.votes||[]).filter(v=>v.voter!==voterId); return {...n, votes:[...others, {voter:voterId, ...vote}] }; })); }
  function computeSpiral(){
    const freq = new Map();
    for(const e of entries) for(const t of e.tags||[]) freq.set(t,(freq.get(t)||0)+1);
    const themes = [...freq.entries()].sort((a,b)=>b[1]-a[1]).slice(0,6).map(([k,v])=>`#${k} ×${v}`);
    const tensions = [];
    const opposites = new Set(["question:proposal","hypothesis:insight"]);
    for(const e of entries){
      const linked = edges.filter(l=>l.source===e.id||l.target===e.id);
      const intents = new Set(linked.map(l=>{ const otherId = l.source===e.id? l.target : l.source; return entries.find(n=>n.id===otherId)?.intent; }).filter(Boolean));
      for(const i of intents){ const pair = `${e.intent}:${i}`; if(opposites.has(pair)||opposites.has(`${i}:${e.intent}`)) tensions.push(`Tension ${e.intent}↔${i} near: \"${e.text.slice(0,60)}…\"`); }
    }
    const actions = [];
    for(const n of entries.filter(e=>e.intent==='proposal')) actions.push(`Pilot: ${n.text} — define 3 metrics, budget est., owner.`);
    const scored = entries.map(n=>({id:n.id, text:n.text, score:consensusScore(n.votes||[])})).sort((a,b)=>b.score-a.score).slice(0,6);
    const highlights = scored.filter(s=>s.score>0).map(s=>`${(s.score*100).toFixed(0)}% — ${s.text.slice(0,80)}…`);
    return { themes, tensions: dedupe(tensions).slice(0,8), actions: dedupe(actions).slice(0,8), highlights };
  }
  function dedupe(arr){ return Array.from(new Set(arr)); }
  function makeAIPrompt(){ return JSON.stringify({ system: "Collaborate with humans using the knowledge spiral.", data:{roomId, entries, edges}, instructions:["Prefer testable micro-experiments","Flag safety/ethics","Use node ids when referencing"] }, null, 2); }
  const graph = useMemo(()=>({ nodes: entries, links: edges }), [entries, edges]);
  const spiral = useMemo(computeSpiral, [entries, edges]);
  const voterId = useMemo(()=> localStorage.getItem('ks:voter') || (localStorage.setItem('ks:voter', uid()), localStorage.getItem('ks:voter')), []);

  return (
    <div style={{fontFamily:'system-ui,Segoe UI,Roboto,Helvetica,Arial', padding:16}}>
      <div style={{display:'flex', gap:16}}>
        <div style={{flex:'0 0 320px'}}>
          <h2>Knowledge Spiral — Room: <code>{roomId}</code></h2>
          <div style={{marginBottom:8}}>
            <input value={roomId} onChange={(e)=>setRoomId(e.target.value)} style={{width:'100%'}} />
            <button onClick={()=>setRoomId(uid())} style={{marginTop:6}}>New Room</button>
          </div>
          <textarea value={text} onChange={(e)=>setText(e.target.value)} placeholder="Add idea... Use #tags" style={{width:'100%', height:120}} />
          <div style={{display:'flex', gap:8, marginTop:8}}>
            <button onClick={()=>addEntry(text)}>Add</button>
            <button onClick={()=>{ setEntries([]); setEdges([]); localStorage.removeItem(storageKey(roomId)); }}>Clear Room</button>
            <button onClick={exportRoom}>Export</button>
            <label style={{display:'inline-block'}}>
              <input type="file" accept="application/json" onChange={(e)=>{ if(e.target.files?.[0]) importRoom(e.target.files[0], {merge:false}); }} />
              Import
            </label>
          </div>

          <div style={{marginTop:12}}>
            <h4>Consensus Highlights</h4>
            <ul>
              {spiral.highlights.length===0 ? <li>No votes yet</li> : spiral.highlights.map((h,i)=>(<li key={i}>{h}</li>))}
            </ul>
            <button onClick={()=>navigator.clipboard.writeText(makeAIPrompt())}>Copy AI Prompt</button>
          </div>
        </div>

        <div style={{flex:1}}>
          <div style={{height:480, border:'1px solid #ddd', borderRadius:8, overflow:'hidden'}}>
            <ForceGraph2D graphData={graph} nodeLabel={(n)=>`${n.intent}: ${n.text}`} nodeVal={(n)=>5 + Math.min(12, n.tags?.length || 0)} linkDirectionalParticles={2} linkDirectionalParticleSpeed={(d)=>0.002 + d.weight*0.02} linkColor={()=>"rgba(0,0,0,0.15)"} nodeCanvasObject={(node,ctx,globalScale)=>{ const label = node.tags?.slice(0,3).join(" • ") || node.intent; const size = 6 + Math.min(10, node.tags?.length || 0); ctx.beginPath(); ctx.arc(node.x,node.y,size,0,2*Math.PI,false); ctx.fillStyle = intentColor(node.intent); ctx.fill(); ctx.font = `${12/globalScale}px sans-serif`; ctx.textAlign = "center"; ctx.fillStyle = "#111827"; ctx.fillText(label, node.x, node.y - (size+4)); }} onNodeClick={(node)=>{ alert(`Node: ${node.text}\nIntent: ${node.intent}\nVotes: ${JSON.stringify(node.votes || [])}`); }} />
          </div>

          <div style={{marginTop:12}}>
            <h3>Ledger</h3>
            {entries.length===0 && <p>No entries yet.</p>}
            {entries.map((e)=>(
              <div key={e.id} style={{border:'1px solid #eee', padding:10, borderRadius:8, marginBottom:8}}>
                <div style={{display:'flex', justifyContent:'space-between'}}>
                  <div><div style={{fontSize:12, color:'#666'}}>{new Date(e.createdAt).toLocaleString()}</div><div style={{fontWeight:600}}>{e.text}</div></div>
                  <div style={{textAlign:'right'}}><div style={{fontSize:12}}>Score: {(consensusScore(e.votes||[])*100).toFixed(0)}%</div><button onClick={()=>removeNode(e.id)}>Remove</button></div>
                </div>
                <div style={{marginTop:8}}>
                  <small>Intent: {e.intent}</small>
                  <div>{(e.tags||[]).map(t=>(<span key={t} style={{display:'inline-block', padding:'2px 6px', margin:4, background:'#f3f4f6', borderRadius:6}}>{t}</span>))}</div>
                </div>
                <div style={{marginTop:8}}>
                  <VoteMini node={e} onVote={(v)=>vote(e.id, voterId, v)} />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function VoteMini({ node, onVote }){
  const [b,setB] = useState(7);
  const [e,setE] = useState(5);
  const [r,setR] = useState(3);
  useEffect(()=>{ const mine = (node.votes||[]).find(v=>v.voter===localStorage.getItem('ks:voter')); if(mine){ setB(mine.benefit||7); setE(mine.effort||5); setR(mine.risk||3); } }, [node.id]);
  return (
    <div style={{display:'flex', gap:8, alignItems:'center'}}>
      <div><small>Benefit</small><br/><input type="range" min="0" max="10" value={b} onChange={(ev)=>setB(Number(ev.target.value))} /></div>
      <div><small>Effort</small><br/><input type="range" min="0" max="10" value={e} onChange={(ev)=>setE(Number(ev.target.value))} /></div>
      <div><small>Risk</small><br/><input type="range" min="0" max="10" value={r} onChange={(ev)=>setR(Number(ev.target.value))} /></div>
      <div><button onClick={()=>onVote({benefit:b, effort:e, risk:r})}>Vote</button></div>
    </div>
  );
}
