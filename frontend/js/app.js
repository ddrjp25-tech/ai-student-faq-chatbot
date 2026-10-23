/**
 * AIET Voice Assistant & College Chatbot - Main Application Logic
 */

document.addEventListener('DOMContentLoaded', () => {
  // State
  const state = {
    sessionId: 'session_' + Math.random().toString(36).substring(2, 9),
    history: [],
    activeTab: 'assistant-tab',
    adminKey: localStorage.getItem('aiet_admin_key') || '',
    courses: [],
    faculty: [],
    fees: [],
    scholarships: [],
    infrastructure: [],
    sources: [],
    isProcessing: false,
    systemInfo: null
  };

  // DOM Elements
  const chatMessagesEl = document.getElementById('chatMessages');
  const chatInputEl = document.getElementById('chatTextInput');
  const chatSendBtn = document.getElementById('chatSendBtn');
  const micBtn = document.getElementById('micHeroBtn');
  const voiceBannerEl = document.getElementById('voiceLiveBanner');
  const voiceLiveTextEl = document.getElementById('voiceLiveText');
  const voiceToggleBtn = document.getElementById('voiceToggleBtn');
  const stopSpeakingBtn = document.getElementById('stopSpeakingBtn');
  const clearChatBtn = document.getElementById('clearChatBtn');
  const statusBadgeEl = document.getElementById('systemStatusBadge');

  // Initialize Voice Controller
  const voice = new VoiceController({
    onTranscriptUpdate: (text) => {
      voiceLiveTextEl.textContent = text || 'Listening...';
    },
    onFinalTranscript: (text) => {
      voiceBannerEl.classList.remove('active');
      if (text) {
        sendMessage(text);
      }
    },
    onStateChange: ({ status }) => {
      if (status === 'listening') {
        micBtn.classList.add('listening');
        voiceBannerEl.classList.add('active');
        voiceLiveTextEl.textContent = 'Listening to your question... Speak now.';
      } else if (status === 'speaking') {
        micBtn.classList.remove('listening');
        stopSpeakingBtn.style.display = 'inline-flex';
      } else {
        micBtn.classList.remove('listening');
        voiceBannerEl.classList.remove('active');
        stopSpeakingBtn.style.display = 'none';
      }
    },
    onError: (errMsg) => {
      showToast(errMsg, 'warning');
      voiceBannerEl.classList.remove('active');
      micBtn.classList.remove('listening');
    }
  });

  // Check microphone support on load
  if (!voice.isRecognitionSupported()) {
    const micWarning = document.getElementById('micSupportWarning');
    if (micWarning) micWarning.style.display = 'block';
  }

  // Initial Welcome Message
  appendAssistantMessage({
    answer: "Hello! Welcome to AIET. I’m your AIET Voice Assistant. You can ask me about courses, faculty, fees, scholarships, admissions, campus floor directory, college timings, office hours, and college rules. How can I help you today?",
    sources: [
      {
        title: "AIET Official Portal",
        url: "https://akashiet.com/",
        category: "College Profile",
        last_verified_date: "2026-03-15",
        verification_status: "VERIFIED_OFFICIAL"
      }
    ],
    suggested_followups: [
      "What are the college rules?",
      "What are the college timings?",
      "Where is the library located?",
      "Where are the labs located?"
    ]
  });

  // Event Listeners
  micBtn.addEventListener('click', () => {
    voice.toggleListening();
  });

  chatSendBtn.addEventListener('click', () => {
    const text = chatInputEl.value.trim();
    if (text) sendMessage(text);
  });

  chatInputEl.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      const text = chatInputEl.value.trim();
      if (text) sendMessage(text);
    }
  });

  if (stopSpeakingBtn) {
    stopSpeakingBtn.addEventListener('click', () => {
      voice.stopSpeaking();
    });
  }

  if (voiceToggleBtn) {
    voiceToggleBtn.addEventListener('click', () => {
      const enabled = voice.toggleSpeechOutput();
      voiceToggleBtn.classList.toggle('active', enabled);
      showToast(enabled ? "Spoken answers enabled" : "Spoken answers muted", "info");
    });
  }

  if (clearChatBtn) {
    clearChatBtn.addEventListener('click', () => {
      chatMessagesEl.innerHTML = '';
      state.history = [];
      voice.stopSpeaking();
      appendAssistantMessage({
        answer: "Conversation cleared. Feel free to ask another question about Akash Institute of Engineering and Technology!",
        suggested_followups: [
          "What courses does AIET offer?",
          "What are the college timings?",
          "What is the KCET code for AIET?"
        ]
      });
    });
  }

  // Tab Navigation
  document.querySelectorAll('.nav-tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const tabTarget = btn.getAttribute('data-tab');
      switchTab(tabTarget);
    });
  });

  // Suggested Questions clicks (Delegation)
  document.addEventListener('click', (e) => {
    const target = e.target.closest('[data-question]');
    if (target) {
      const q = target.getAttribute('data-question');
      if (q) {
        switchTab('assistant-tab');
        sendMessage(q);
      }
    }
  });

  // Switch Tab Helper
  function switchTab(tabId) {
    document.querySelectorAll('.nav-tab-btn').forEach(b => {
      b.classList.toggle('active', b.getAttribute('data-tab') === tabId);
    });
    document.querySelectorAll('.tab-panel').forEach(panel => {
      panel.classList.toggle('active', panel.id === tabId);
    });
    state.activeTab = tabId;

    // Load data for secondary tabs on first view
    if (tabId === 'courses-tab' && state.courses.length === 0) loadCourses();
    if (tabId === 'faculty-tab' && state.faculty.length === 0) loadFaculty();
    if (tabId === 'fees-tab' && state.fees.length === 0) loadFees();
    if (tabId === 'scholarships-tab' && state.scholarships.length === 0) loadScholarships();
    if (tabId === 'infra-tab' && state.infrastructure.length === 0) loadInfrastructure();
    if (tabId === 'admin-tab') initAdminTab();
  }

  // ==========================================
  // Core Chat & QA Workflow
  // ==========================================

  async function sendMessage(questionText) {
    if (state.isProcessing || !questionText) return;

    chatInputEl.value = '';
    state.isProcessing = true;

    // Append User message to UI
    appendUserMessage(questionText);
    state.history.push({ role: 'user', content: questionText });

    // Show typing loader
    const loaderId = appendTypingLoader();

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: questionText,
          session_id: state.sessionId,
          history: state.history.slice(-6)
        })
      });

      if (!response.ok) {
        throw new Error(`Server returned ${response.status}`);
      }

      const data = await response.json();
      removeTypingLoader(loaderId);

      // Append Assistant message
      appendAssistantMessage(data);
      state.history.push({ role: 'assistant', content: data.answer });

      // Spoken Answer
      voice.speak(data.answer);

    } catch (err) {
      console.error("Chat error:", err);
      removeTypingLoader(loaderId);
      appendAssistantMessage({
        answer: "I'm experiencing difficulty connecting to the AIET knowledge base server. Please ensure the backend is running at http://localhost:8000, or contact the admissions desk at +91 9513107575.",
        sources: []
      });
      showToast("Could not connect to AIET server", "error");
    } finally {
      state.isProcessing = false;
    }
  }

  function appendUserMessage(text) {
    const msg = document.createElement('div');
    msg.className = 'chat-message user';
    msg.innerHTML = `
      <div class="msg-avatar">You</div>
      <div class="msg-body">
        <div class="msg-bubble">${escapeHtml(text)}</div>
        <div class="msg-meta">${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</div>
      </div>
    `;
    chatMessagesEl.appendChild(msg);
    scrollToBottom();
  }

  function appendAssistantMessage(data) {
    const msg = document.createElement('div');
    msg.className = 'chat-message assistant';

    let sourcesHtml = '';
    if (data.sources && data.sources.length > 0) {
      const chips = data.sources.map(s => `
        <a href="${s.url}" target="_blank" rel="noopener noreferrer" class="source-chip" title="Verified: ${s.last_verified_date}">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>
          ${escapeHtml(s.title)} (${s.last_verified_date})
        </a>
      `).join('');

      sourcesHtml = `
        <div class="sources-card">
          <div class="sources-card-title">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>
            Verified Official Sources
          </div>
          <div class="source-chips">${chips}</div>
        </div>
      `;
    }

    let confirmationHtml = '';
    if (data.needs_confirmation) {
      confirmationHtml = `
        <div class="confirmation-notice">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
          <div>
            <strong>Admissions Office Confirmation Required:</strong> ${escapeHtml(data.confirmation_note || "Fees and policies vary by year. Contact admissions office directly for confirmation.")}
            <div style="margin-top: 4px;">📞 +91 9513107575 | ✉️ admissions@akashinstitutions.com</div>
          </div>
        </div>
      `;
    }

    let followupsHtml = '';
    if (data.suggested_followups && data.suggested_followups.length > 0) {
      const followupBtns = data.suggested_followups.map(q => `
        <button class="followup-chip" data-question="${escapeHtml(q)}">${escapeHtml(q)}</button>
      `).join('');
      followupsHtml = `<div class="inline-followups">${followupBtns}</div>`;
    }

    const formattedAnswer = formatMarkdownText(data.answer);

    msg.innerHTML = `
      <div class="msg-avatar">AI</div>
      <div class="msg-body">
        <div class="msg-bubble">${formattedAnswer}</div>
        ${confirmationHtml}
        ${sourcesHtml}
        ${followupsHtml}
        <div class="msg-meta">
          <span>${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
          <button class="replay-btn" title="Replay spoken answer">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/></svg>
            Speak
          </button>
        </div>
      </div>
    `;

    // Replay button listener
    const replayBtn = msg.querySelector('.replay-btn');
    if (replayBtn) {
      replayBtn.addEventListener('click', () => {
        voice.speak(data.answer);
      });
    }

    chatMessagesEl.appendChild(msg);
    scrollToBottom();
  }

  function appendTypingLoader() {
    const id = 'loader_' + Math.random().toString(36).substring(2, 7);
    const msg = document.createElement('div');
    msg.className = 'chat-message assistant';
    msg.id = id;
    msg.innerHTML = `
      <div class="msg-avatar">AI</div>
      <div class="msg-body">
        <div class="msg-bubble" style="display:flex; align-items:center; gap:8px;">
          <span style="font-size:0.85rem; color:var(--text-muted)">Searching AIET knowledge base...</span>
          <div class="voice-wave-anim">
            <div class="voice-wave-bar"></div>
            <div class="voice-wave-bar"></div>
            <div class="voice-wave-bar"></div>
            <div class="voice-wave-bar"></div>
          </div>
        </div>
      </div>
    `;
    chatMessagesEl.appendChild(msg);
    scrollToBottom();
    return id;
  }

  function removeTypingLoader(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
  }

  function scrollToBottom() {
    chatMessagesEl.scrollTop = chatMessagesEl.scrollHeight;
  }

  function formatMarkdownText(text) {
    if (!text) return '';
    let out = escapeHtml(text);
    // Bold
    out = out.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    // Bullets
    out = out.replace(/^[•*-]\s+(.+)$/gm, '<li>$1</li>');
    out = out.replace(/(<li>.*<\/li>)/s, '<ul style="padding-left:20px; margin:8px 0;">$1</ul>');
    // Newlines
    out = out.replace(/\n\n/g, '<br><br>');
    out = out.replace(/\n/g, '<br>');
    return out;
  }

  function escapeHtml(string) {
    const div = document.createElement('div');
    div.innerText = string;
    return div.innerHTML;
  }

  function showToast(message, type = 'info') {
    let container = document.getElementById('toastContainer');
    if (!container) {
      container = document.createElement('div');
      container.id = 'toastContainer';
      container.className = 'toast-container';
      document.body.appendChild(container);
    }
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    container.appendChild(toast);
    setTimeout(() => {
      toast.remove();
    }, 4000);
  }

  // ==========================================
  // Health Check & Server Status
  // ==========================================

  async function checkHealth() {
    try {
      const res = await fetch('/api/health');
      if (res.ok) {
        const data = await res.json();
        state.systemInfo = data;
        statusBadgeEl.innerHTML = `
          <span class="status-dot"></span>
          AIET Knowledge Active (${data.total_chunks_indexed} Chunks)
        `;
      }
    } catch (e) {
      statusBadgeEl.innerHTML = `
        <span class="status-dot" style="background:#ef4444;"></span>
        Offline
      `;
    }
  }
  checkHealth();

  // ==========================================
  // Secondary Pages Data Fetching & Rendering
  // ==========================================

  async function loadCourses() {
    const grid = document.getElementById('coursesGrid');
    if (!grid) return;
    grid.innerHTML = '<div style="color:var(--text-muted); padding:20px;">Loading courses...</div>';

    try {
      const res = await fetch('/api/courses');
      const data = await res.json();
      state.courses = data;
      renderCourses(data);
    } catch (e) {
      grid.innerHTML = '<div style="color:red">Failed to load courses.</div>';
    }
  }

  function renderCourses(courses) {
    const grid = document.getElementById('coursesGrid');
    if (!grid) return;
    if (courses.length === 0) {
      grid.innerHTML = '<div style="color:var(--text-muted); grid-column:1/-1;">No matching courses found.</div>';
      return;
    }

    grid.innerHTML = courses.map(c => `
      <div class="data-card">
        <span class="card-badge">${escapeHtml(c.level)} • ${escapeHtml(c.duration)}</span>
        <h3 class="card-h3">${escapeHtml(c.course_name)}</h3>
        <div style="font-size:0.8rem; color:var(--aiet-orange); font-weight:600; margin-bottom:10px;">
          ${escapeHtml(c.department)}
        </div>
        <p class="card-text">${escapeHtml(c.eligibility)}</p>
        <div style="margin-bottom:14px; font-size:0.8rem; color:var(--text-muted)">
          <strong>HOD:</strong> ${escapeHtml(c.head_of_department || "Check faculty directory")}
        </div>
        <div class="card-footer-action">
          <button class="action-link" style="background:none; border:none; cursor:pointer;" data-question="Tell me about ${escapeHtml(c.short_name)} eligibility and curriculum">
            Ask AI Assistant →
          </button>
          <a href="${c.source_url}" target="_blank" rel="noopener noreferrer" class="source-chip">Official Link</a>
        </div>
      </div>
    `).join('');
  }

  // Course Filter & Search
  const courseSearchInput = document.getElementById('courseSearchInput');
  if (courseSearchInput) {
    courseSearchInput.addEventListener('input', (e) => {
      const val = e.target.value.toLowerCase();
      const filtered = state.courses.filter(c =>
        c.course_name.toLowerCase().includes(val) ||
        c.short_name.toLowerCase().includes(val) ||
        c.department.toLowerCase().includes(val)
      );
      renderCourses(filtered);
    });
  }

  document.querySelectorAll('.course-level-pill').forEach(pill => {
    pill.addEventListener('click', () => {
      document.querySelectorAll('.course-level-pill').forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      const level = pill.getAttribute('data-level');
      if (level === 'ALL') {
        renderCourses(state.courses);
      } else {
        renderCourses(state.courses.filter(c => c.level.toUpperCase().includes(level)));
      }
    });
  });

  // Faculty Directory
  async function loadFaculty() {
    const grid = document.getElementById('facultyGrid');
    if (!grid) return;
    grid.innerHTML = '<div style="color:var(--text-muted); padding:20px;">Loading faculty directory...</div>';

    try {
      const res = await fetch('/api/faculty');
      const data = await res.json();
      state.faculty = data;
      renderFaculty(data);
      populateFacultyDeptFilter();
    } catch (e) {
      grid.innerHTML = '<div style="color:red">Failed to load faculty directory.</div>';
    }
  }

  function renderFaculty(facultyList) {
    const grid = document.getElementById('facultyGrid');
    if (!grid) return;
    if (facultyList.length === 0) {
      grid.innerHTML = '<div style="color:var(--text-muted); grid-column:1/-1;">No faculty members matched your search.</div>';
      return;
    }

    grid.innerHTML = facultyList.map(f => `
      <div class="data-card">
        <div class="faculty-card-header">
          <div class="faculty-avatar" style="display:flex;align-items:center;justify-content:center;color:#38bdf8;font-weight:700;">
            ${escapeHtml(f.name.replace(/^(Dr\.|Mr\.|Mrs\.|Ms\.)\s*/, '').substring(0, 2).toUpperCase())}
          </div>
          <div class="faculty-meta">
            <div class="faculty-name">${escapeHtml(f.name)}</div>
            <div class="faculty-desig">${escapeHtml(f.designation)}</div>
            <div class="faculty-dept">${escapeHtml(f.department)}</div>
          </div>
        </div>
        ${f.is_head_of_department ? '<span class="card-badge hod-badge">Head of Department (HOD)</span>' : ''}
        <div class="card-footer-action" style="margin-top:auto;">
          ${f.profile_pdf_url ? `
            <a href="${f.profile_pdf_url}" target="_blank" rel="noopener noreferrer" class="action-link" style="color:var(--aiet-blue-light);">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
              View Profile PDF
            </a>
          ` : '<span style="font-size:0.75rem; color:var(--text-dim)">AIET Faculty</span>'}
          <button class="action-link" style="background:none; border:none; cursor:pointer;" data-question="Tell me about ${escapeHtml(f.name)} in ${escapeHtml(f.department)}">
            Ask AI →
          </button>
        </div>
      </div>
    `).join('');
  }

  function populateFacultyDeptFilter() {
    const select = document.getElementById('facultyDeptSelect');
    if (!select) return;
    const depts = Array.from(new Set(state.faculty.map(f => f.department))).sort();
    select.innerHTML = '<option value="">All Departments</option>' + depts.map(d => `
      <option value="${escapeHtml(d)}">${escapeHtml(d)}</option>
    `).join('');

    select.addEventListener('change', filterFaculty);
  }

  const facultySearchInput = document.getElementById('facultySearchInput');
  if (facultySearchInput) {
    facultySearchInput.addEventListener('input', filterFaculty);
  }

  function filterFaculty() {
    const q = (facultySearchInput ? facultySearchInput.value : '').toLowerCase();
    const dept = (document.getElementById('facultyDeptSelect') ? document.getElementById('facultyDeptSelect').value : '').toLowerCase();
    const hodOnly = document.getElementById('facultyHodCheckbox') ? document.getElementById('facultyHodCheckbox').checked : false;

    const filtered = state.faculty.filter(f => {
      const matchQ = f.name.toLowerCase().includes(q) || f.designation.toLowerCase().includes(q) || f.department.toLowerCase().includes(q);
      const matchDept = !dept || f.department.toLowerCase() === dept;
      const matchHod = !hodOnly || f.is_head_of_department;
      return matchQ && matchDept && matchHod;
    });
    renderFaculty(filtered);
  }

  const facultyHodCheckbox = document.getElementById('facultyHodCheckbox');
  if (facultyHodCheckbox) {
    facultyHodCheckbox.addEventListener('change', filterFaculty);
  }

  // Fees & Expenses
  async function loadFees() {
    const grid = document.getElementById('feesGrid');
    if (!grid) return;
    grid.innerHTML = '<div style="color:var(--text-muted); padding:20px;">Loading fee guidelines...</div>';

    try {
      const res = await fetch('/api/fees');
      const data = await res.json();
      state.fees = data;
      grid.innerHTML = data.map(f => `
        <div class="data-card">
          <span class="card-badge" style="background:rgba(245,158,11,0.15); border-color:var(--accent-gold); color:#fef08a;">
            ${escapeHtml(f.quota_type || f.category)} • ${escapeHtml(f.academic_year)}
          </span>
          <h3 class="card-h3">${escapeHtml(f.title)}</h3>
          <p class="card-text"><strong>Estimated / Regulated:</strong> ${escapeHtml(f.fee_range_inr || f.fee_details)}</p>
          <div style="padding:10px; background:rgba(255,255,255,0.03); border-radius:8px; font-size:0.8rem; color:var(--text-muted); margin-bottom:14px;">
            ${escapeHtml(f.official_guidance_rule || f.policy_summary)}
          </div>
          <div class="card-footer-action">
            <span style="font-size:0.75rem; color:var(--text-dim)">Verified: ${f.last_verified_date}</span>
            <button class="btn-primary" style="padding:6px 14px; font-size:0.78rem;" data-question="What is the fee for ${escapeHtml(f.title)}?">
              Ask AI Details
            </button>
          </div>
        </div>
      `).join('');
    } catch (e) {
      grid.innerHTML = '<div style="color:red">Failed to load fees data.</div>';
    }
  }

  // Scholarships
  async function loadScholarships() {
    const grid = document.getElementById('scholarshipsGrid');
    if (!grid) return;
    grid.innerHTML = '<div style="color:var(--text-muted); padding:20px;">Loading scholarships...</div>';

    try {
      const res = await fetch('/api/scholarships');
      const data = await res.json();
      state.scholarships = data;
      grid.innerHTML = data.map(s => `
        <div class="data-card">
          <span class="card-badge" style="background:rgba(16,185,129,0.15); border-color:var(--accent-emerald); color:#6ee7b7;">
            ${escapeHtml(s.offered_by)}
          </span>
          <h3 class="card-h3">${escapeHtml(s.scheme_name)}</h3>
          <p class="card-text">${escapeHtml(s.applicable_to || s.eligibility_criteria || '')}</p>
          <div style="font-size:0.85rem; font-weight:600; color:#38bdf8; margin-bottom:10px;">
            Benefit: ${escapeHtml(s.benefit || s.benefit_amount || 'Tuition concession / financial grant')}
          </div>
          <div class="card-footer-action">
            ${s.application_portal || s.portal ? `<a href="${s.application_portal || s.portal}" target="_blank" rel="noopener noreferrer" class="action-link">Portal Link ↗</a>` : '<span></span>'}
            <button class="action-link" style="background:none; border:none; cursor:pointer;" data-question="How can I apply for ${escapeHtml(s.scheme_name)}?">
              Ask AI Eligibility →
            </button>
          </div>
        </div>
      `).join('');
    } catch (e) {
      grid.innerHTML = '<div style="color:red">Failed to load scholarships.</div>';
    }
  }

  // Infrastructure
  async function loadInfrastructure() {
    const grid = document.getElementById('infraGrid');
    if (!grid) return;
    grid.innerHTML = '<div style="color:var(--text-muted); padding:20px;">Loading facilities...</div>';

    try {
      const res = await fetch('/api/infrastructure');
      const data = await res.json();
      state.infrastructure = data;
      grid.innerHTML = data.map(i => `
        <div class="data-card">
          <span class="card-badge">Campus Amenity</span>
          <h3 class="card-h3">${escapeHtml(i.title)}</h3>
          <p class="card-text">${escapeHtml(i.description)}</p>
          <div class="card-footer-action">
            <span style="font-size:0.75rem; color:var(--text-dim)">Source: official alet portal</span>
            <button class="action-link" style="background:none; border:none; cursor:pointer;" data-question="Tell me about ${escapeHtml(i.title)} at AIET">
              Ask AI →
            </button>
          </div>
        </div>
      `).join('');
    } catch (e) {
      grid.innerHTML = '<div style="color:red">Failed to load infrastructure.</div>';
    }
  }

  // ==========================================
  // Knowledge Base Admin Workflow
  // ==========================================

  function initAdminTab() {
    const adminKeyInput = document.getElementById('adminKeyInput');
    const saveAdminKeyBtn = document.getElementById('saveAdminKeyBtn');
    const adminPanelArea = document.getElementById('adminPanelArea');

    if (state.adminKey) {
      adminKeyInput.value = state.adminKey;
      adminPanelArea.style.display = 'block';
      loadAdminDocuments();
    }

    saveAdminKeyBtn.addEventListener('click', () => {
      const key = adminKeyInput.value.trim();
      if (!key) {
        showToast("Please enter an Admin Key", "warning");
        return;
      }
      state.adminKey = key;
      localStorage.setItem('aiet_admin_key', key);
      adminPanelArea.style.display = 'block';
      loadAdminDocuments();
      showToast("Admin Key saved", "success");
    });

    const rebuildBtn = document.getElementById('rebuildKbBtn');
    if (rebuildBtn) {
      rebuildBtn.addEventListener('click', async () => {
        if (!confirm("Are you sure you want to rebuild the entire AIET vector index from official records?")) return;
        try {
          const res = await fetch('/api/admin/rebuild', {
            method: 'POST',
            headers: { 'x-admin-key': state.adminKey }
          });
          const data = await res.json();
          if (res.ok) {
            showToast("Knowledge Base rebuilt successfully!", "success");
            loadAdminDocuments();
            checkHealth();
          } else {
            showToast(data.detail || "Rebuild failed", "error");
          }
        } catch (e) {
          showToast("Network error rebuilding index", "error");
        }
      });
    }

    // Direct text ingestion form
    const adminIngestForm = document.getElementById('adminIngestForm');
    if (adminIngestForm) {
      adminIngestForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const title = document.getElementById('ingestTitle').value.trim();
        const category = document.getElementById('ingestCategory').value.trim();
        const sourceUrl = document.getElementById('ingestSourceUrl').value.trim();
        const content = document.getElementById('ingestContent').value.trim();

        if (!title || !content) {
          showToast("Title and content are required", "warning");
          return;
        }

        try {
          const res = await fetch('/api/admin/ingest', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'x-admin-key': state.adminKey
            },
            body: JSON.stringify({
              title,
              category: category || 'General',
              source_url: sourceUrl || 'https://akashiet.com/',
              content,
              last_verified_date: new Date().toISOString().split('T')[0]
            })
          });

          if (res.ok) {
            showToast("Document successfully indexed into ChromaDB!", "success");
            adminIngestForm.reset();
            loadAdminDocuments();
            checkHealth();
          } else {
            const data = await res.json();
            showToast(data.detail || "Ingest failed", "error");
          }
        } catch (e) {
          showToast("Error indexing document", "error");
        }
      });
    }
  }

  async function loadAdminDocuments() {
    const docListEl = document.getElementById('adminDocsList');
    if (!docListEl) return;
    docListEl.innerHTML = '<div style="color:var(--text-muted); padding:10px;">Loading indexed documents...</div>';

    try {
      const res = await fetch('/api/admin/documents', {
        headers: { 'x-admin-key': state.adminKey }
      });
      if (res.status === 401) {
        docListEl.innerHTML = '<div style="color:#ef4444; padding:10px;">Unauthorized: Incorrect Admin Key</div>';
        return;
      }
      const data = await res.json();
      docListEl.innerHTML = `
        <div style="margin-bottom:12px; font-weight:600; color:#38bdf8;">
          Total Indexed Chunks in ChromaDB: ${data.total_count}
        </div>
        <div style="display:flex; flex-direction:column; gap:8px; max-height:360px; overflow-y:auto;">
          ${data.documents.map(d => `
            <div style="display:flex; align-items:center; justify-content:space-between; padding:10px 14px; background:rgba(255,255,255,0.03); border:1px solid var(--border-glass); border-radius:8px;">
              <div>
                <div style="font-weight:600; color:#fff; font-size:0.88rem;">${escapeHtml(d.title)}</div>
                <div style="font-size:0.75rem; color:var(--text-muted);">${escapeHtml(d.category)} • ID: ${escapeHtml(d.id)} • Verified: ${escapeHtml(d.last_verified_date || 'N/A')}</div>
              </div>
              <button class="delete-doc-btn" data-id="${escapeHtml(d.id)}" style="background:rgba(239,68,68,0.2); border:1px solid rgba(239,68,68,0.4); color:#fca5a5; padding:4px 10px; border-radius:6px; cursor:pointer; font-size:0.75rem;">
                Delete
              </button>
            </div>
          `).join('')}
        </div>
      `;

      // Attach delete handlers
      docListEl.querySelectorAll('.delete-doc-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
          const docId = btn.getAttribute('data-id');
          if (!confirm(`Delete document chunk '${docId}' from ChromaDB?`)) return;
          try {
            const delRes = await fetch(`/api/admin/documents/${docId}`, {
              method: 'DELETE',
              headers: { 'x-admin-key': state.adminKey }
            });
            if (delRes.ok) {
              showToast("Document deleted", "info");
              loadAdminDocuments();
              checkHealth();
            }
          } catch (e) {
            showToast("Failed to delete", "error");
          }
        });
      });
    } catch (e) {
      docListEl.innerHTML = '<div style="color:red">Failed to load admin documents.</div>';
    }
  }

});
