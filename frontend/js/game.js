let ws = null;
let boardState = Array(9).fill('');
let currentMatchId = null;
let mySymbol = null;
let isGameOver = false;

const WS_BASE = window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost'
    ? 'ws://127.0.0.1:8000'
    : window.location.origin.replace(/^http/, 'ws');

function startGame(matchId, symbol) {
    boardState = Array(9).fill('');
    isGameOver = false;
    mySymbol = symbol;
    currentMatchId = matchId;

    document.getElementById('match-label').textContent = `Match #${matchId}`;
    document.getElementById('game-actions').innerHTML = '';

    // Using simple defaults until we get full player names from WS or match data
    document.getElementById('name-x').textContent = symbol === 'X' ? currentUser.username : 'Opponent';
    document.getElementById('name-o').textContent = symbol === 'O' ? currentUser.username : 'Opponent';

    setStatusText('Connecting…', 'live-msg');
    drawBoard();
    showScreen('game-screen');

    const token = localStorage.getItem('access_token');
    if (ws) ws.close();
    ws = new WebSocket(`${WS_BASE}/ws/game/${matchId}?token=${token}`);

    ws.onopen = () => {
        setStatusText("Connected!", 'live-msg');
    };

    ws.onmessage = (e) => {
        const data = JSON.parse(e.data);
        handleWsEvent(data);
    };

    ws.onclose = (e) => {
        if (!isGameOver) setStatusText('🔌 Disconnected', 'live-msg');
    };
}

function handleWsEvent(data) {
    if (data.type === "game_state") {
        boardState = data.board;
        drawBoard();

        if (data.status === "completed") {
            isGameOver = true;
            handleGameOver(data.winner, data.winning_line);
        } else {
            setActiveTurn(data.current_turn);
            const isMyTurn = data.current_turn === mySymbol;
            let timeMsg = data.turn_timer ? ` (${data.turn_timer}s)` : '';
            setStatusText(isMyTurn ? `🎯 Your turn!${timeMsg}` : `⏳ Opponent's turn…${timeMsg}`, 'live-msg');
        }
    }
    else if (data.type === "player_joined" || data.type === "opponent_reconnected") {
        toast("Opponent is ready");
    }
    else if (data.type === "opponent_disconnected") {
        setStatusText('💔 Opponent disconnected', 'live-msg');
    }
    else if (data.type === "error") {
        toast(`❌ ${data.error.message}`);
    }
    else if (data.type === "rematch_requested") {
        toast("Opponent requested a rematch!");
        showRematchButtons(true);
    }
    else if (data.type === "rematch_declined") {
        toast("Opponent declined rematch.");
        document.getElementById('game-actions').innerHTML = `<button class="btn btn-primary" onclick="goLobby()">🏠 Back to Lobby</button>`;
    }
    else if (data.type === "rematch_accepted") {
        toast("Rematch accepted!");
        // Small delay then start new game
        setTimeout(() => {
            // Swap symbols
            let newSymbol = mySymbol === 'X' ? 'O' : 'X';
            startGame(data.new_match_id, newSymbol);
        }, 1000);
    }
}

function makeMove(pos) {
    if (isGameOver) return;
    if (boardState[pos] !== '') return;
    if (!ws || ws.readyState !== WebSocket.OPEN) { toast('Not connected'); return; }

    // Send structured event
    ws.send(JSON.stringify({ type: "move", position: pos }));
}

function drawBoard() {
    const boardEl = document.getElementById('board');
    boardEl.innerHTML = '';
    boardState.forEach((val, i) => {
        const cell = document.createElement('div');
        cell.className = 'cell' + (val ? ' taken ' + (val === 'X' ? 'x-cell' : 'o-cell') : '');
        cell.id = `cell-${i}`;
        cell.onclick = () => makeMove(i);
        const inner = document.createElement('span');
        inner.className = 'cell-inner';
        inner.textContent = val === 'X' ? '✕' : val === 'O' ? '○' : '';
        cell.appendChild(inner);
        boardEl.appendChild(cell);
    });
}

function handleGameOver(winner, winningLine) {
    isGameOver = true;
    if (winner !== 'draw' && winningLine) {
        winningLine.forEach(idx => {
            const el = document.getElementById(`cell-${idx}`);
            if (el) el.classList.add('winning');
        });
    }

    if (winner === 'draw') {
        setStatusText("🤝 It's a draw!", 'draw-msg');
        setTimeout(() => showModal('🤝', "It's a Draw!", 'A closely fought match — well played!'), 1200);
    } else {
        const iWon = winner === mySymbol;
        setStatusText(iWon ? '🏆 You Won!' : '😞 You Lost', iWon ? 'win-msg' : '');
        setTimeout(() => {
            if (iWon) showModal('🏆', 'Victory!', "Excellent play! You crushed the opponent.");
            else showModal('😔', 'Defeated!', 'Tough luck. Try again!');
        }, 1200);
    }

    if (typeof loadProfileStats === 'function') loadProfileStats();
    showRematchButtons(false);
}

function showRematchButtons(hasRequest) {
    let html = `<button class="btn btn-secondary" onclick="goLobby()">🏠 Lobby</button>`;
    if (hasRequest) {
        html += `<button class="btn btn-primary" onclick="acceptRematch()">Accept Rematch</button>`;
        html += `<button class="btn btn-danger" onclick="declineRematch()">Decline</button>`;
    } else {
        html += `<button class="btn btn-primary" onclick="requestRematch()">Request Rematch</button>`;
    }
    document.getElementById('game-actions').innerHTML = html;
}

function requestRematch() {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: "rematch_request" }));
        document.getElementById('game-actions').innerHTML = `<p style="color:var(--muted)">Rematch requested...</p>`;
    }
}

function acceptRematch() {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: "rematch_request" }));
    }
}

function declineRematch() {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: "rematch_decline" }));
        document.getElementById('game-actions').innerHTML = `<button class="btn btn-primary" onclick="goLobby()">🏠 Lobby</button>`;
    }
}
