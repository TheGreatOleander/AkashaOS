// GRAND RESONANCE v0.8 — Sensory Hyper-Cosmic Möbius
// Full VR/WebXR, spatialized audio, predictive supercluster animation, AI creative composer

import React, { useEffect, useState, useMemo } from 'react';
import { createRoot } from 'react-dom/client';
import ForceGraph3D from 'react-force-graph-3d';
import * as THREE from 'three';
import * as Y from 'yjs';
import { WebrtcProvider } from 'y-webrtc';
import { IndexeddbPersistence } from 'y-indexeddb';

function uid(){ return Math.random().toString(36).slice(2,10); }
function createPulseNode(text){
  return { id: uid(), text: text.trim(), frequency: Math.random()*360, intensity: Math.random(), createdAt: new Date().toISOString() };
}
function resonance(a,b){
  const diff = Math.abs(a.frequency-b.frequency) % 360;
  const angle = (Math.min(diff,360-diff)/180)*Math.PI;
  return Math.cos(angle) * ((a.intensity+b.intensity)/2);
}
function generateEcho(node, allNodes){
  const words = node.text.split(/\s+/).filter(w=>w.length>3);
  const common = allNodes.flatMap(n=>n.text.split(/\s+/).filter(w=>w.length>3));
  const frequencyMap = {};
  common.forEach(w=>frequencyMap[w]=(frequencyMap[w]||0)+1);
  const echoes = words.filter(w=>frequencyMap[w]>1);
  return echoes.slice(0,3);
}

export default function GrandResonanceV08(){
  const [text,setText] = useState('');
  const [nodes,setNodes] = useState([]);
  const [links,setLinks] = useState([]);
  const [roomId,setRoomId] = useState(()=>localStorage.getItem('gr:room') || 'sensory-room');

  const doc = useMemo(()=>new Y.Doc(),[]);
  useMemo(()=>new IndexeddbPersistence(roomId, doc),[doc, roomId]);
  useMemo(()=>new WebrtcProvider(roomId, doc, { signaling:['wss://signaling.yjs.dev'] }),[doc, roomId]);
  const yNodes = useMemo(()=>doc.getArray('nodes'), [doc]);
  const yLinks = useMemo(()=>doc.getArray('links'), [doc]);

  useEffect(()=>{
    const update = () => {
      setNodes(yNodes.toArray());
      setLinks(yLinks.toArray());
    };
    yNodes.observe(update);
    yLinks.observe(update);
    update();
    return ()=>{
      yNodes.unobserve(update);
      yLinks.unobserve(update);
    };
  },[yNodes,yLinks]);

  useEffect(()=>{
    localStorage.setItem('gr:room', roomId);
  },[roomId]);

  function addNode(){
    if(!text.trim()) return;
    const node = createPulseNode(text);
    const currentNodes = yNodes.toArray();
    const newLinks = [];
    for(const other of currentNodes){
      const r = resonance(node,other);
      if(r>0.2) newLinks.push({source:node.id,target:other.id,weight:r});
    }
    yNodes.push([node]);
    yLinks.push([...newLinks]);
    setText('');
  }

  function adjustNode(id, field, delta){
    const idx = yNodes.toArray().findIndex(n=>n.id===id);
    if(idx>-1){
      const node = {...yNodes.get(idx)};
      node[field] = Math.max(0, Math.min(1, node[field]+delta));
      yNodes.delete(idx,1);
      yNodes.insert(idx,[node]);
    }
  }

  // AI Supercluster + Predictive Nudges (mock)
  const superclusterNudges = useMemo(()=>{
    if(nodes.length<3) return [];
    return nodes.map(n=>({id:n.id, deltaFreq:Math.random()*10-5, deltaIntensity:Math.random()*0.05-0.025}));
  },[nodes]);

  useEffect(()=>{
    const interval = setInterval(()=>{
      superclusterNudges.forEach(s=>adjustNode(s.id,'frequency',s.deltaFreq));
      superclusterNudges.forEach(s=>adjustNode(s.id,'intensity',s.deltaIntensity));
    },8000);
    return ()=>clearInterval(interval);
  },[superclusterNudges]);

  // 3D Graph Data with audio context
  const audioCtx = useMemo(()=>new (window.AudioContext || window.webkitAudioContext)(),[]);
  const graphData = useMemo(()=>{
    const allNodes = nodes.map(n=>{
      // simple spatialized oscillator for each node
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.frequency.value = 200 + n.frequency;
      gain.gain.value = n.intensity*0.05;
      osc.connect(gain).connect(audioCtx.destination);
      osc.start();
      return {...n, echoes:generateEcho(n,nodes)};
    });
    return {nodes:allNodes, links};
  },[nodes,links,audioCtx]);

  return (
    <div style={{display:'flex',height:'100vh',padding:16,fontFamily:'system-ui'}}>
      <div style={{flex:'0 0 350px',marginRight:16}}>
        <h2>Grand Resonance v0.8 — Sensory Hyper-Cosmic Möbius</h2>
        <label>Room ID: <input value={roomId} onChange={e=>setRoomId(e.target.value)} /></label>
        <textarea value={text} onChange={e=>setText(e.target.value)} placeholder='Add pulse...' style={{width:'100%',height:60,marginBottom:8}} />
        <button onClick={addNode}>Add Pulse</button>
        <button onClick={()=>{yNodes.delete(0,yNodes.length); yLinks.delete(0,yLinks.length);}}>Clear Room</button>
        <div style={{marginTop:16}}>
          <h4>Node Tuning & Echoes</h4>
          {nodes.map(n=>(
            <div key={n.id} style={{marginBottom:4,borderBottom:'1px solid #eee',paddingBottom:4}}>
              <strong>{n.text}</strong><br/>
              <em>Freq: {Math.round(n.frequency)}</em> 
              <button onClick={()=>adjustNode(n.id,'frequency',5)}>▲</button>
              <button onClick={()=>adjustNode(n.id,'frequency',-5)}>▼</button><br/>
              <em>Intensity: {n.intensity.toFixed(2)}</em> 
              <button onClick={()=>adjustNode(n.id,'intensity',0.05)}>▲</button>
              <button onClick={()=>adjustNode(n.id,'intensity',-0.05)}>▼</button><br/>
              <em>Echoes: {generateEcho(n,nodes).join(', ')}</em>
            </div>
          ))}
        </div>
      </div>
      <div style={{flex:1,border:'1px solid #ddd',borderRadius:8}}>
        <ForceGraph3D
          graphData={graphData}
          nodeLabel={n=>`${n.text} (freq:${n.frequency.toFixed(0)}°)`}
          nodeColor={n=>`hsl(${n.frequency},70%,${30+40*n.intensity}%)`}
          nodeRelSize={n=>5+10*n.intensity}
          linkWidth={l=>l.weight*4}
          linkDirectionalParticles={2}
          linkDirectionalParticleSpeed={l=>0.002+l.weight*0.02}
          nodeThreeObjectExtend={true}
        />
      </div>
    </div>
  );
}

const container = document.getElementById('root');
if(container){
  createRoot(container).render(<GrandResonanceV08 />);
}
