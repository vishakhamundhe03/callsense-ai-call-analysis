const state = { calls: [], selectedId: null };
const $ = (id) => document.getElementById(id);
const escapeHtml = (s) => String(s ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
async function loadCalls() {
  try {
    const res = await fetch("/api/calls");
    if (!res.ok) throw new Error("API returned " + res.status);
    state.calls = await res.json();
    $("totalCalls").textContent = state.calls.length;
    $("positiveCount").textContent = state.calls.filter(c => c.sentiment === "Positive").length;
    $("avgProbability").textContent = Math.round(state.calls.reduce((s,c)=>s+c.purchase_probability,0)/Math.max(1,state.calls.length)) + "%";
    $("followUpCount").textContent = state.calls.filter(c => c.purchase_probability < 70).length;
    $("callCountPill").textContent = `${state.calls.length} RECORDINGS`;
    renderCallList();
    selectCall(state.selectedId || state.calls[0]?.id);
  } catch (e) {
    $("callList").innerHTML = `<div class="loading">Could not load API. Start the Flask server and refresh.<br><small>${escapeHtml(e.message)}</small></div>`;
  }
}
function renderCallList() {
  const query = $("searchInput").value.toLowerCase().trim();
  const sentiment = $("sentimentFilter").value;
  const filtered = state.calls.filter(c =>
    (sentiment === "All" || c.sentiment === sentiment) &&
    `${c.customer} ${c.product} ${c.id}`.toLowerCase().includes(query)
  );
  $("callList").innerHTML = filtered.length ? filtered.map(c => `
    <div class="call-item ${c.id===state.selectedId?'selected':''}" data-id="${escapeHtml(c.id)}" tabindex="0" role="button" aria-label="Open ${escapeHtml(c.customer)} call">
      <div class="call-main"><div><div class="customer">${escapeHtml(c.customer)}</div><div class="product">${escapeHtml(c.product)}</div></div><span class="badge ${escapeHtml(c.sentiment)}">${escapeHtml(c.sentiment)}</span></div>
      <div class="call-meta"><span class="duration">◷ ${escapeHtml(c.duration)} · ${escapeHtml(c.date)}</span><span class="likelihood-mini">Purchase <b>${c.purchase_probability}%</b></span></div>
    </div>`).join("") : `<div class="loading">No calls match your filters.</div>`;
  document.querySelectorAll(".call-item").forEach(el => {
    el.addEventListener("click", () => selectCall(el.dataset.id));
    el.addEventListener("keydown", e => { if(e.key==="Enter"||e.key===" "){e.preventDefault();selectCall(el.dataset.id);} });
  });
}
function selectCall(id) {
  const c = state.calls.find(x => x.id === id);
  if (!c) return;
  state.selectedId = id;
  renderCallList();
  const transcript = c.transcript.map(t => `<div class="utterance"><span class="speaker ${t.speaker}">${escapeHtml(t.speaker.toUpperCase())}</span>${escapeHtml(t.text)}</div>`).join("");
  const insights = c.key_insights.map(x => `<li>${escapeHtml(x)}</li>`).join("");
  $("detailPanel").innerHTML = `
    <div class="detail-title"><div><h2>${escapeHtml(c.customer)}</h2><div class="subline">${escapeHtml(c.id)} &nbsp;·&nbsp; ${escapeHtml(c.product)}<br>${escapeHtml(c.date)} &nbsp;·&nbsp; ${escapeHtml(c.duration)} minutes</div></div>
    <button class="btn" id="downloadReport">↓ &nbsp; Download report</button></div>
    <div class="audio-box"><div class="section-head">Call recording <span class="pill">SAMPLE AUDIO</span></div>
      <audio controls preload="metadata" src="${escapeHtml(c.audio)}">Your browser does not support audio playback.</audio>
      <div class="audio-hint">Play the sample conversation. Transcript is shown below.</div>
    </div>
    <div class="score-grid">
      <div class="score-card"><div class="label">CUSTOMER SENTIMENT</div><div class="sentiment-large"><span class="sentiment-dot ${escapeHtml(c.sentiment)}"></span>${escapeHtml(c.sentiment)}</div><div class="small-note">Lexicon score: ${c.sentiment_score} · Estimated from transcript wording</div></div>
      <div class="score-card"><div class="label">PURCHASE PROBABILITY</div><div class="prob-row"><span class="prob-number">${c.purchase_probability}%</span><span class="pill">${escapeHtml(c.purchase_intent)} intent</span></div><div class="progress"><span style="width:${c.purchase_probability}%"></span></div><div class="small-note">Illustrative heuristic estimate, not a calibrated model.</div></div>
    </div>
    <div class="section"><div class="section-head">Key insights <span class="pill">${c.key_insights.length} FINDINGS</span></div><ul class="insights">${insights}</ul></div>
    <div class="section"><div class="section-head">Customer behavior</div><div class="behavior">${escapeHtml(c.customer_behavior)}</div></div>
    <div class="section"><div class="section-head">Recommended next action</div><div class="recommendation">${escapeHtml(c.recommended_action)}</div></div>
    <div class="section"><div class="section-head">Call transcript <span class="pill">${c.transcript.length} UTTERANCES</span></div><div class="transcript">${transcript}</div></div>
    <div class="method-note"><b>Method:</b> ${escapeHtml(c.method)}. This is an educational prototype. Validate against labeled calls before using predictions for business decisions.</div>`;
  $("downloadReport").addEventListener("click", () => {
    const btn = $("downloadReport"); btn.disabled = true; btn.textContent = "Preparing report…";
    // Direct PDF endpoint streams a generated report for the selected call.
    window.location.href = `/api/reports/${encodeURIComponent(c.id)}.pdf`;
    setTimeout(() => { if(btn.isConnected){btn.disabled=false;btn.innerHTML="↓ &nbsp; Download report";}}, 1200);
  });
}
$("searchInput").addEventListener("input", renderCallList);
$("sentimentFilter").addEventListener("change", renderCallList);
loadCalls();
