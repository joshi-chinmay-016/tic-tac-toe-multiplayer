let replayMoves = [];
let replayCurrentStep = 0;
let replayBoardState = Array(9).fill('');

async function loadMatchHistory() {
    const el = document.getElementById('history-list');
    if (!currentUser) return;
    try {
        const res = await apiFetch(`/games/history/${currentUser.username}`);
        const data = await res.json();
        if (!data.length) { el.innerHTML = '<p style="color:var(--muted);text-align:center;padding:20px 0">No matches yet.</p>'; return; }

        el.innerHTML = data.map(game => {
            let resultText = "Draw";
            let resultColor = "var(--warning)";
            if (game.winner === 'X' || game.winner === 'O') {
                const iWon = (game.player_x === currentUser.username && game.winner === 'X') ||
                             (game.player_o === currentUser.username && game.winner === 'O');
                resultText = iWon ? "Victory" : "Defeat";
                resultColor = iWon ? "var(--success)" : "var(--accent2)";
            }

            const opponent = game.player_x === currentUser.username ? (game.player_o || game.ai_difficulty) : (game.player_x || game.ai_difficulty);
            const date = new Date(game.completed_at).toLocaleString();

            return `
              <div class="lb-row" style="justify-content:space-between">
                <div>
                    <div style="font-weight:bold; color:${resultColor}">${resultText} <span style="font-weight:normal; color:var(--muted); font-size:0.8rem">vs ${opponent}</span></div>
                    <div style="font-size:0.75rem; color:var(--muted)">${date} • ${game.move_count} moves</div>
                </div>
                <button class="btn btn-secondary" style="padding:4px 10px; font-size:0.75rem;" onclick="watchReplay(${game.id})">Watch</button>
              </div>
            `;
        }).join('');
    } catch {
        el.innerHTML = '<p style="color:var(--muted);text-align:center">Could not load history.</p>';
    }
}

async function watchReplay(gameId) {
    try {
        const res = await apiFetch(`/games/${gameId}/replay`);
        const data = await res.json();
        replayMoves = data.events;
        replayCurrentStep = 0;
        replayBoardState = Array(9).fill('');

        document.getElementById('replay-label').textContent = `Match #${gameId}`;

        renderReplayBoard();
        updateReplayStatus();
        showScreen('replay-screen');
    } catch {
        toast("Failed to load replay.");
    }
}

function replayNext() {
    if (replayCurrentStep < replayMoves.length) {
        const move = replayMoves[replayCurrentStep];
        replayBoardState[move.position] = move.symbol;
        replayCurrentStep++;
        renderReplayBoard();
        updateReplayStatus();
    }
}

function replayPrev() {
    if (replayCurrentStep > 0) {
        replayCurrentStep--;
        const move = replayMoves[replayCurrentStep];
        replayBoardState[move.position] = '';
        renderReplayBoard();
        updateReplayStatus();
    }
}

function renderReplayBoard() {
    const boardEl = document.getElementById('replay-board');
    if (!boardEl) return;
    boardEl.style.display = 'grid';
    boardEl.style.gridTemplateColumns = 'repeat(3, 1fr)';
    boardEl.style.gap = '10px';
    boardEl.style.width = 'min(360px, 90vw)';

    boardEl.innerHTML = '';
    replayBoardState.forEach((val, i) => {
        const cell = document.createElement('div');
        cell.className = 'cell' + (val ? ' taken ' + (val === 'X' ? 'x-cell' : 'o-cell') : '');

        const inner = document.createElement('span');
        inner.className = 'cell-inner';
        inner.textContent = val === 'X' ? '✕' : val === 'O' ? '○' : '';
        cell.appendChild(inner);
        boardEl.appendChild(cell);
    });
}

function updateReplayStatus() {
    document.getElementById('replay-status').textContent = `Move ${replayCurrentStep} / ${replayMoves.length}`;
}
