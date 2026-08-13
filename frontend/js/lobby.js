async function loadLeaderboard() {
    const el = document.getElementById('leaderboard-list');
    try {
        const res = await apiFetch(`/leaderboard/`);
        const data = await res.json();
        if (!data.length) { el.innerHTML = '<p style="color:var(--muted);text-align:center;padding:20px 0">No players yet.</p>'; return; }

        const ranks = ['gold', 'silver', 'bronze'];
        el.innerHTML = data.map((u, i) => `
          <div class="lb-row">
            <div class="lb-rank ${ranks[i] || ''}">${i + 1}</div>
            <div class="lb-name" style="flex:1">${escHtml(u.username)} ${u.id === (currentUser?.id) ? '<span style="color:var(--muted);font-size:0.8em">(you)</span>' : ''}</div>
            <div style="text-align:right">
                <div style="font-weight:bold; color:var(--accent)">${u.rating}</div>
                <div style="font-size:0.75rem; color:var(--muted)">${u.wins}W - ${u.losses}L</div>
            </div>
          </div>
        `).join('');
    } catch {
        el.innerHTML = '<p style="color:var(--muted);text-align:center">Could not load leaderboard.</p>';
    }
}

async function loadProfileStats() {
    if (!currentUser) return;
    try {
        const res = await apiFetch(`/users/${currentUser.username}`);
        if (!res.ok) return;
        const data = await res.json();

        document.getElementById('stat-username').textContent = data.username;
        document.getElementById('stat-wins').textContent = data.wins;
        document.getElementById('stat-losses').textContent = data.losses;
        document.getElementById('stat-wr').textContent = data.win_rate + '%';

        // Let's also load history
        if (typeof loadMatchHistory === 'function') {
            loadMatchHistory();
        }
    } catch {}
}

function escHtml(str) {
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

async function findMatch() {
    if (!currentUser) return;
    const btn = document.getElementById('btn-find');
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner"></span> Searching…';

    const dot = document.getElementById('queue-dot');
    const msg = document.getElementById('queue-msg');
    dot.className = 'dot waiting';
    msg.textContent = 'Waiting for an opponent…';

    try {
        const res = await apiFetch(`/matchmaking/join`, { method: 'POST' });
        const data = await res.json();

        if (data.match_id) {
            handleMatchFound(data);
        } else {
            msg.textContent = 'In queue – waiting for opponent…';
            pollTimer = setInterval(async () => {
                try {
                    const r = await apiFetch(`/matchmaking/join`, { method: 'POST' });
                    const d = await r.json();
                    if (d.match_id) {
                        clearInterval(pollTimer);
                        pollTimer = null;
                        handleMatchFound(d);
                    }
                } catch {}
            }, 2000);
        }
    } catch {
        toast('❌ Could not reach server');
        btn.disabled = false;
        btn.textContent = 'Find Match';
        dot.className = 'dot';
        msg.textContent = 'Press "Find Match" to join the queue';
    }
}

function handleMatchFound(data) {
    const { match_id, player_x } = data;
    const mySymbol = (player_x === currentUser.id) ? 'X' : 'O';

    const dot = document.getElementById('queue-dot');
    const msg = document.getElementById('queue-msg');
    dot.className = 'dot found';
    msg.textContent = `Match found! Match #${match_id}`;

    toast(`🎮 Match found! You are playing as ${mySymbol}`);
    setTimeout(() => startGame(match_id, mySymbol), 800);
}

// AI Match logic
async function startAIGame() {
    if (!currentUser) return;
    const diff = document.getElementById('ai-difficulty').value;
    const sym = document.getElementById('ai-symbol').value;
    const starts = sym === 'X' ? 'player' : 'ai';

    try {
        const res = await apiFetch(`/games/ai?difficulty=${diff}&symbol=${sym}&starts=${starts}`, { method: 'POST' });
        const data = await res.json();
        if (data.match_id) {
            startGame(data.match_id, sym);
        }
    } catch {
        toast('❌ Failed to start AI game');
    }
}

// Private Room logic
async function createPrivateRoom() {
    try {
        const res = await apiFetch(`/rooms/create`, { method: 'POST' });
        const data = await res.json();

        // Just show code and start polling logic similar to matchmaking
        toast(`Room created! Code: ${data.code}`);
        const msg = document.getElementById('queue-msg');
        msg.textContent = `Room created: ${data.code} - Waiting for opponent...`;

        pollTimer = setInterval(async () => {
            try {
                const r = await apiFetch(`/rooms/join?code=${data.code}`, { method: 'POST' });
                const d = await r.json();
                if (d.match_id) {
                    clearInterval(pollTimer);
                    pollTimer = null;
                    handleMatchFound(d);
                }
            } catch {}
        }, 2000);
    } catch {
        toast('❌ Failed to create room');
    }
}

async function joinPrivateRoom() {
    const code = document.getElementById('room-code-input').value.trim();
    if (!code) {
        toast('Please enter a room code');
        return;
    }

    try {
        const res = await apiFetch(`/rooms/join?code=${code}`, { method: 'POST' });
        const data = await res.json();

        if (data.match_id) {
            handleMatchFound(data);
        } else {
            toast(data.detail || 'Failed to join room');
        }
    } catch {
        toast('❌ Failed to join room');
    }
}
