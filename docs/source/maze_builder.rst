Maze Builder
============

This interactive tool allows you to create custom mazes for PyRat.
Use the controls below to build your maze, then save it as a JSON file that can be loaded in your games.

.. raw:: html

    <style>
        .maze-builder-container {
            font-family: Arial, sans-serif;
            max-width: 100%;
            margin: 20px 0;
        }
        
        .toolbar {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 15px;
            padding: 10px;
            background: #f5f5f5;
            border-radius: 8px;
            align-items: center;
        }
        
        .tool-group {
            display: flex;
            align-items: center;
            gap: 5px;
            padding: 5px 10px;
            border-right: 1px solid #ddd;
        }
        
        .tool-group:last-child {
            border-right: none;
        }
        
        .tool-group label {
            font-weight: bold;
            font-size: 0.9em;
            color: #333;
        }
        
        .tool-btn {
            padding: 8px 12px;
            border: 2px solid #ccc;
            background: white;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.85em;
            transition: all 0.2s;
        }
        
        .tool-btn:hover {
            background: #e0e0e0;
        }
        
        .tool-btn.active {
            border-color: #007bff;
            background: #007bff;
            color: white;
        }
        
        .tool-btn.action-btn {
            background: #28a745;
            color: white;
            border-color: #28a745;
        }
        
        .tool-btn.action-btn:hover {
            background: #218838;
        }
        
        .tool-btn.load-btn {
            background: #17a2b8;
            color: white;
            border-color: #17a2b8;
        }
        
        .tool-btn.load-btn:hover {
            background: #138496;
        }
        
        .mud-value-input {
            width: 50px;
            padding: 5px;
            border: 1px solid #ccc;
            border-radius: 4px;
            text-align: center;
        }
        
        .maze-wrapper {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 5px;
            max-width: 100%;
            max-height: 70vh;
            overflow: auto;
            padding: 10px;
        }
        
        .maze-row-wrapper {
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        .maze-grid {
            display: inline-block;
            border: 2px solid #333;
            background: #333;
            flex-shrink: 0;
        }
        
        .maze-row {
            display: flex;
        }
        
        .maze-cell {
            width: 40px;
            height: 40px;
            background: #f0f0f0;
            border: 1px solid #ccc;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            position: relative;
            font-size: 10px;
            font-weight: bold;
            transition: background 0.1s;
        }
        
        .maze-cell.hole {
            background: #333;
            cursor: not-allowed;
        }
        
        .maze-cell.hole::after {
            content: '';
        }
        
        /* Cell hover only for cell tool */
        .maze-grid.tool-cell .maze-cell:not(.hole):hover {
            background: #d0d0d0;
        }
        
        .maze-cell .wall-top,
        .maze-cell .wall-bottom,
        .maze-cell .wall-left,
        .maze-cell .wall-right {
            position: absolute;
            background: transparent;
            z-index: 2;
        }
        
        .maze-cell .wall-top {
            top: -2px;
            left: 4px;
            right: 4px;
            height: 6px;
        }
        
        .maze-cell .wall-bottom {
            bottom: -2px;
            left: 4px;
            right: 4px;
            height: 6px;
        }
        
        .maze-cell .wall-left {
            left: -2px;
            top: 4px;
            bottom: 4px;
            width: 6px;
        }
        
        .maze-cell .wall-right {
            right: -2px;
            top: 4px;
            bottom: 4px;
            width: 6px;
        }
        
        .maze-cell .wall-top.active,
        .maze-cell .wall-bottom.active,
        .maze-cell .wall-left.active,
        .maze-cell .wall-right.active {
            background: #333;
        }
        
        /* Edge hover for wall/mud tools */
        .maze-grid.tool-wall .maze-cell:not(.hole) .wall-top:hover,
        .maze-grid.tool-wall .maze-cell:not(.hole) .wall-bottom:hover,
        .maze-grid.tool-wall .maze-cell:not(.hole) .wall-left:hover,
        .maze-grid.tool-wall .maze-cell:not(.hole) .wall-right:hover,
        .maze-grid.tool-mud .maze-cell:not(.hole) .wall-top:hover,
        .maze-grid.tool-mud .maze-cell:not(.hole) .wall-bottom:hover,
        .maze-grid.tool-mud .maze-cell:not(.hole) .wall-left:hover,
        .maze-grid.tool-mud .maze-cell:not(.hole) .wall-right:hover,
        .maze-grid.tool-wall .maze-cell:not(.hole) .wall-top.hover-pair,
        .maze-grid.tool-wall .maze-cell:not(.hole) .wall-bottom.hover-pair,
        .maze-grid.tool-wall .maze-cell:not(.hole) .wall-left.hover-pair,
        .maze-grid.tool-wall .maze-cell:not(.hole) .wall-right.hover-pair,
        .maze-grid.tool-mud .maze-cell:not(.hole) .wall-top.hover-pair,
        .maze-grid.tool-mud .maze-cell:not(.hole) .wall-bottom.hover-pair,
        .maze-grid.tool-mud .maze-cell:not(.hole) .wall-left.hover-pair,
        .maze-grid.tool-mud .maze-cell:not(.hole) .wall-right.hover-pair {
            background: rgba(0, 123, 255, 0.5);
            cursor: pointer;
        }
        
        .mud-indicator {
            position: absolute;
            z-index: 3;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 9px;
            font-weight: bold;
            color: #5c3d1e;
            background: #d4a574;
            border-radius: 3px;
            padding: 1px 3px;
            pointer-events: none;
        }
        
        .mud-indicator.horizontal {
            left: 50%;
            transform: translateX(-50%);
            bottom: -5px;
        }
        
        .mud-indicator.vertical {
            top: 50%;
            transform: translateY(-50%);
            right: -8px;
        }
        
        .add-remove-btn {
            width: 30px;
            height: 30px;
            border: 1px solid #ccc;
            background: #f9f9f9;
            border-radius: 4px;
            cursor: pointer;
            font-size: 18px;
            font-weight: bold;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s;
        }
        
        .add-remove-btn:hover {
            background: #e0e0e0;
        }
        
        .add-remove-btn.add {
            color: #28a745;
        }
        
        .add-remove-btn.remove {
            color: #dc3545;
        }
        
        .column-controls {
            display: flex;
            gap: 5px;
            justify-content: center;
        }
        
        .column-control-group {
            display: flex;
            gap: 2px;
        }
        
        .row-controls {
            display: flex;
            flex-direction: column;
            gap: 5px;
            justify-content: center;
        }
        
        .row-control-group {
            display: flex;
            flex-direction: column;
            gap: 2px;
        }
        
        .status-bar {
            margin-top: 10px;
            padding: 8px;
            background: #e9ecef;
            border-radius: 4px;
            font-size: 0.9em;
            color: #495057;
        }
        
        .hidden-input {
            display: none;
        }
        
        .cell-index {
            position: absolute;
            bottom: 2px;
            right: 2px;
            font-size: 8px;
            color: #999;
        }
    </style>

    <div class="maze-builder-container">
        <div class="toolbar">
            <div class="tool-group">
                <label>Tool:</label>
                <button class="tool-btn active" id="tool-cell" onclick="setTool('cell')">🔲 Cell</button>
                <button class="tool-btn" id="tool-wall" onclick="setTool('wall')">🧱 Wall</button>
                <button class="tool-btn" id="tool-mud" onclick="setTool('mud')">🟤 Mud</button>
            </div>
            <div class="tool-group">
                <label>Mud value:</label>
                <input type="number" id="mud-value" class="mud-value-input" value="2" min="2" max="20">
            </div>
            <div class="tool-group">
                <label>Actions:</label>
                <button class="tool-btn action-btn" onclick="saveMaze()">💾 Save</button>
                <button class="tool-btn load-btn" onclick="document.getElementById('load-input').click()">📂 Load</button>
                <input type="file" id="load-input" class="hidden-input" accept=".json" onchange="loadMaze(event)">
            </div>
            <div class="tool-group">
                <label>View:</label>
                <input type="checkbox" id="show-indices" onchange="toggleIndices()">
                <label for="show-indices" style="font-weight: normal;">Show indices</label>
            </div>
        </div>
        
        <div class="maze-wrapper">
            <div class="column-controls" id="top-controls"></div>
            <div class="maze-row-wrapper">
                <div class="row-controls" id="left-controls"></div>
                <div class="maze-grid" id="maze-grid"></div>
                <div class="row-controls" id="right-controls"></div>
            </div>
            <div class="column-controls" id="bottom-controls"></div>
        </div>
        
        <div class="status-bar" id="status-bar">
            Maze size: <span id="maze-size">5 × 5</span> | 
            Cells: <span id="cell-count">25</span> | 
            Current tool: <span id="current-tool">Cell (click to toggle)</span>
        </div>
    </div>

    <script>
        let mazeWidth = 5;
        let mazeHeight = 5;
        let currentTool = 'cell';
        let showIndices = false;
        
        // Maze data structure
        // cells[row][col] = true if cell exists, false if hole
        let cells = [];
        // walls[row][col] = {top: bool, right: bool, bottom: bool, left: bool}
        let walls = [];
        // mud[row][col] = {top: int, right: int, bottom: int, left: int} (0 = no mud)
        let mud = [];
        
        function initMaze() {
            cells = [];
            walls = [];
            mud = [];
            for (let r = 0; r < mazeHeight; r++) {
                cells[r] = [];
                walls[r] = [];
                mud[r] = [];
                for (let c = 0; c < mazeWidth; c++) {
                    cells[r][c] = true;
                    walls[r][c] = {top: false, right: false, bottom: false, left: false};
                    mud[r][c] = {top: 0, right: 0, bottom: 0, left: 0};
                }
            }
            renderMaze();
        }
        
        function setTool(tool) {
            currentTool = tool;
            document.querySelectorAll('.tool-btn').forEach(btn => {
                if (btn.id && btn.id.startsWith('tool-')) {
                    btn.classList.remove('active');
                }
            });
            document.getElementById('tool-' + tool).classList.add('active');
            
            // Update grid class for hover behavior
            const grid = document.getElementById('maze-grid');
            grid.className = 'maze-grid tool-' + tool;
            
            let toolDesc = '';
            switch(tool) {
                case 'cell': toolDesc = 'Cell (click to toggle)'; break;
                case 'wall': toolDesc = 'Wall (click cell edges)'; break;
                case 'mud': toolDesc = 'Mud (click cell edges)'; break;
            }
            document.getElementById('current-tool').textContent = toolDesc;
        }
        
        function toggleIndices() {
            showIndices = document.getElementById('show-indices').checked;
            renderMaze();
        }
        
        function getCellIndex(row, col) {
            return row * mazeWidth + col;
        }
        
        function renderMaze() {
            const grid = document.getElementById('maze-grid');
            grid.innerHTML = '';
            grid.className = 'maze-grid tool-' + currentTool;
            
            let cellCount = 0;
            
            for (let r = 0; r < mazeHeight; r++) {
                const rowDiv = document.createElement('div');
                rowDiv.className = 'maze-row';
                
                for (let c = 0; c < mazeWidth; c++) {
                    const cellDiv = document.createElement('div');
                    cellDiv.className = 'maze-cell' + (cells[r][c] ? '' : ' hole');
                    cellDiv.dataset.row = r;
                    cellDiv.dataset.col = c;
                    
                    if (cells[r][c]) {
                        cellCount++;
                        
                        // Add wall indicators with hover support
                        ['top', 'right', 'bottom', 'left'].forEach(side => {
                            const wallDiv = document.createElement('div');
                            wallDiv.className = 'wall-' + side + (walls[r][c][side] ? ' active' : '');
                            wallDiv.dataset.side = side;
                            wallDiv.dataset.row = r;
                            wallDiv.dataset.col = c;
                            wallDiv.onclick = (e) => handleEdgeClick(e, r, c, side);
                            wallDiv.onmouseenter = (e) => handleEdgeHover(e, r, c, side, true);
                            wallDiv.onmouseleave = (e) => handleEdgeHover(e, r, c, side, false);
                            cellDiv.appendChild(wallDiv);
                        });
                        
                        // Add mud indicators (only on bottom and right edges to avoid duplication)
                        if (mud[r][c].bottom > 0) {
                            const mudDiv = document.createElement('div');
                            mudDiv.className = 'mud-indicator horizontal';
                            mudDiv.textContent = mud[r][c].bottom;
                            cellDiv.appendChild(mudDiv);
                        }
                        if (mud[r][c].right > 0) {
                            const mudDiv = document.createElement('div');
                            mudDiv.className = 'mud-indicator vertical';
                            mudDiv.textContent = mud[r][c].right;
                            cellDiv.appendChild(mudDiv);
                        }
                        
                        // Add cell index if enabled
                        if (showIndices) {
                            const indexDiv = document.createElement('div');
                            indexDiv.className = 'cell-index';
                            indexDiv.textContent = getCellIndex(r, c);
                            cellDiv.appendChild(indexDiv);
                        }
                    }
                    
                    cellDiv.onclick = (e) => handleCellClick(e, r, c);
                    rowDiv.appendChild(cellDiv);
                }
                
                grid.appendChild(rowDiv);
            }
            
            document.getElementById('maze-size').textContent = mazeWidth + ' × ' + mazeHeight;
            document.getElementById('cell-count').textContent = cellCount;
            
            renderControls();
        }
        
        function renderControls() {
            // Top controls (add/remove rows at top)
            const topControls = document.getElementById('top-controls');
            topControls.innerHTML = '';
            const topGroup = document.createElement('div');
            topGroup.className = 'column-control-group';
            topGroup.innerHTML = `
                <button class="add-remove-btn remove" onclick="removeRowTop()" title="Remove row from top">−</button>
                <button class="add-remove-btn add" onclick="addRowTop()" title="Add row at top">+</button>
            `;
            topControls.appendChild(topGroup);
            
            // Bottom controls (add/remove rows at bottom)
            const bottomControls = document.getElementById('bottom-controls');
            bottomControls.innerHTML = '';
            const bottomGroup = document.createElement('div');
            bottomGroup.className = 'column-control-group';
            bottomGroup.innerHTML = `
                <button class="add-remove-btn remove" onclick="removeRowBottom()" title="Remove row from bottom">−</button>
                <button class="add-remove-btn add" onclick="addRowBottom()" title="Add row at bottom">+</button>
            `;
            bottomControls.appendChild(bottomGroup);
            
            // Left controls (add/remove columns at left)
            const leftControls = document.getElementById('left-controls');
            leftControls.innerHTML = '';
            const leftGroup = document.createElement('div');
            leftGroup.className = 'row-control-group';
            leftGroup.innerHTML = `
                <button class="add-remove-btn remove" onclick="removeColumnLeft()" title="Remove column from left">−</button>
                <button class="add-remove-btn add" onclick="addColumnLeft()" title="Add column at left">+</button>
            `;
            leftControls.appendChild(leftGroup);
            
            // Right controls (add/remove columns at right)
            const rightControls = document.getElementById('right-controls');
            rightControls.innerHTML = '';
            const rightGroup = document.createElement('div');
            rightGroup.className = 'row-control-group';
            rightGroup.innerHTML = `
                <button class="add-remove-btn remove" onclick="removeColumnRight()" title="Remove column from right">−</button>
                <button class="add-remove-btn add" onclick="addColumnRight()" title="Add column at right">+</button>
            `;
            rightControls.appendChild(rightGroup);
        }
        
        function handleEdgeHover(e, row, col, side, isEntering) {
            if (currentTool === 'cell') return;
            
            // Find the neighbor cell's corresponding edge
            let neighborRow = row, neighborCol = col;
            let oppositeSide = '';
            switch(side) {
                case 'top': neighborRow = row - 1; oppositeSide = 'bottom'; break;
                case 'bottom': neighborRow = row + 1; oppositeSide = 'top'; break;
                case 'left': neighborCol = col - 1; oppositeSide = 'right'; break;
                case 'right': neighborCol = col + 1; oppositeSide = 'left'; break;
            }
            
            // Check if neighbor exists
            if (neighborRow >= 0 && neighborRow < mazeHeight && 
                neighborCol >= 0 && neighborCol < mazeWidth &&
                cells[neighborRow][neighborCol]) {
                // Find the neighbor's edge element
                const neighborCell = document.querySelector(`.maze-cell[data-row="${neighborRow}"][data-col="${neighborCol}"]`);
                if (neighborCell) {
                    const neighborEdge = neighborCell.querySelector(`.wall-${oppositeSide}`);
                    if (neighborEdge) {
                        if (isEntering) {
                            neighborEdge.classList.add('hover-pair');
                        } else {
                            neighborEdge.classList.remove('hover-pair');
                        }
                    }
                }
            }
        }
        
        function handleCellClick(e, row, col) {
            if (e.target.dataset.side) return; // Click was on edge
            
            if (currentTool === 'cell') {
                cells[row][col] = !cells[row][col];
                if (!cells[row][col]) {
                    // Reset walls and mud when removing cell
                    walls[row][col] = {top: false, right: false, bottom: false, left: false};
                    mud[row][col] = {top: 0, right: 0, bottom: 0, left: 0};
                    // Also remove walls/mud from neighbors pointing to this cell
                    if (row > 0) { walls[row-1][col].bottom = false; mud[row-1][col].bottom = 0; }
                    if (row < mazeHeight-1) { walls[row+1][col].top = false; mud[row+1][col].top = 0; }
                    if (col > 0) { walls[row][col-1].right = false; mud[row][col-1].right = 0; }
                    if (col < mazeWidth-1) { walls[row][col+1].left = false; mud[row][col+1].left = 0; }
                }
                renderMaze();
            }
        }
        
        function handleEdgeClick(e, row, col, side) {
            e.stopPropagation();
            
            if (!cells[row][col]) return;
            
            // Check if neighbor exists
            let neighborRow = row, neighborCol = col;
            let oppositeSide = '';
            switch(side) {
                case 'top': neighborRow = row - 1; oppositeSide = 'bottom'; break;
                case 'bottom': neighborRow = row + 1; oppositeSide = 'top'; break;
                case 'left': neighborCol = col - 1; oppositeSide = 'right'; break;
                case 'right': neighborCol = col + 1; oppositeSide = 'left'; break;
            }
            
            // Check bounds and if neighbor is a cell
            const hasNeighbor = neighborRow >= 0 && neighborRow < mazeHeight && 
                               neighborCol >= 0 && neighborCol < mazeWidth &&
                               cells[neighborRow][neighborCol];
            
            if (currentTool === 'wall') {
                walls[row][col][side] = !walls[row][col][side];
                // Clear mud if adding wall
                if (walls[row][col][side]) {
                    mud[row][col][side] = 0;
                }
                // Sync with neighbor
                if (hasNeighbor) {
                    walls[neighborRow][neighborCol][oppositeSide] = walls[row][col][side];
                    if (walls[row][col][side]) {
                        mud[neighborRow][neighborCol][oppositeSide] = 0;
                    }
                }
                renderMaze();
            } else if (currentTool === 'mud') {
                if (!hasNeighbor) return; // Can't add mud to edge
                if (walls[row][col][side]) return; // Can't add mud where there's a wall
                
                const mudValue = parseInt(document.getElementById('mud-value').value) || 2;
                if (mud[row][col][side] === mudValue) {
                    // Toggle off
                    mud[row][col][side] = 0;
                    mud[neighborRow][neighborCol][oppositeSide] = 0;
                } else {
                    mud[row][col][side] = mudValue;
                    mud[neighborRow][neighborCol][oppositeSide] = mudValue;
                }
                renderMaze();
            }
        }
        
        function addRowTop() {
            mazeHeight++;
            cells.unshift([]);
            walls.unshift([]);
            mud.unshift([]);
            for (let c = 0; c < mazeWidth; c++) {
                cells[0][c] = true;
                walls[0][c] = {top: false, right: false, bottom: false, left: false};
                mud[0][c] = {top: 0, right: 0, bottom: 0, left: 0};
            }
            renderMaze();
        }
        
        function removeRowTop() {
            if (mazeHeight <= 2) return;
            mazeHeight--;
            cells.shift();
            walls.shift();
            mud.shift();
            renderMaze();
        }
        
        function addRowBottom() {
            mazeHeight++;
            cells.push([]);
            walls.push([]);
            mud.push([]);
            for (let c = 0; c < mazeWidth; c++) {
                cells[mazeHeight-1][c] = true;
                walls[mazeHeight-1][c] = {top: false, right: false, bottom: false, left: false};
                mud[mazeHeight-1][c] = {top: 0, right: 0, bottom: 0, left: 0};
            }
            renderMaze();
        }
        
        function removeRowBottom() {
            if (mazeHeight <= 2) return;
            mazeHeight--;
            cells.pop();
            walls.pop();
            mud.pop();
            renderMaze();
        }
        
        function addColumnLeft() {
            mazeWidth++;
            for (let r = 0; r < mazeHeight; r++) {
                cells[r].unshift(true);
                walls[r].unshift({top: false, right: false, bottom: false, left: false});
                mud[r].unshift({top: 0, right: 0, bottom: 0, left: 0});
            }
            renderMaze();
        }
        
        function removeColumnLeft() {
            if (mazeWidth <= 2) return;
            mazeWidth--;
            for (let r = 0; r < mazeHeight; r++) {
                cells[r].shift();
                walls[r].shift();
                mud[r].shift();
            }
            renderMaze();
        }
        
        function addColumnRight() {
            mazeWidth++;
            for (let r = 0; r < mazeHeight; r++) {
                cells[r].push(true);
                walls[r].push({top: false, right: false, bottom: false, left: false});
                mud[r].push({top: 0, right: 0, bottom: 0, left: 0});
            }
            renderMaze();
        }
        
        function removeColumnRight() {
            if (mazeWidth <= 2) return;
            mazeWidth--;
            for (let r = 0; r < mazeHeight; r++) {
                cells[r].pop();
                walls[r].pop();
                mud[r].pop();
            }
            renderMaze();
        }
        
        function saveMaze() {
            // Build PyRat maze format: dict[int, dict[int, int]]
            // Key is source vertex, value is dict of {destination: weight}
            const mazeDict = {};
            
            for (let r = 0; r < mazeHeight; r++) {
                for (let c = 0; c < mazeWidth; c++) {
                    if (!cells[r][c]) continue;
                    
                    const cellIndex = getCellIndex(r, c);
                    mazeDict[cellIndex] = {};
                    
                    // Check each direction
                    const directions = [
                        {side: 'top', dr: -1, dc: 0},
                        {side: 'bottom', dr: 1, dc: 0},
                        {side: 'left', dr: 0, dc: -1},
                        {side: 'right', dr: 0, dc: 1}
                    ];
                    
                    for (const dir of directions) {
                        const nr = r + dir.dr;
                        const nc = c + dir.dc;
                        
                        // Check bounds
                        if (nr < 0 || nr >= mazeHeight || nc < 0 || nc >= mazeWidth) continue;
                        // Check if neighbor exists
                        if (!cells[nr][nc]) continue;
                        // Check if there's a wall
                        if (walls[r][c][dir.side]) continue;
                        
                        const neighborIndex = getCellIndex(nr, nc);
                        const weight = mud[r][c][dir.side] > 0 ? mud[r][c][dir.side] : 1;
                        mazeDict[cellIndex][neighborIndex] = weight;
                    }
                }
            }
            
            const blob = new Blob([JSON.stringify(mazeDict, null, 2)], {type: 'application/json'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'pyrat_maze.json';
            a.click();
            URL.revokeObjectURL(url);
        }
        
        function loadMaze(event) {
            const file = event.target.files[0];
            if (!file) return;
            
            const reader = new FileReader();
            reader.onload = function(e) {
                try {
                    const mazeData = JSON.parse(e.target.result);
                    
                    // Determine maze dimensions from cell indices
                    let maxIndex = 0;
                    for (const srcStr of Object.keys(mazeData)) {
                        const src = parseInt(srcStr);
                        if (src > maxIndex) maxIndex = src;
                        for (const dstStr of Object.keys(mazeData[srcStr])) {
                            const dst = parseInt(dstStr);
                            if (dst > maxIndex) maxIndex = dst;
                        }
                    }
                    
                    // Infer width from vertical neighbors (difference > 1)
                    let inferredWidth = 0;
                    for (const srcStr of Object.keys(mazeData)) {
                        const src = parseInt(srcStr);
                        for (const dstStr of Object.keys(mazeData[srcStr])) {
                            const dst = parseInt(dstStr);
                            const diff = Math.abs(dst - src);
                            if (diff > 1 && (inferredWidth === 0 || diff < inferredWidth)) {
                                inferredWidth = diff;
                            }
                        }
                    }
                    
                    if (inferredWidth === 0) {
                        inferredWidth = Math.ceil(Math.sqrt(maxIndex + 1));
                    }
                    
                    mazeWidth = inferredWidth;
                    mazeHeight = Math.ceil((maxIndex + 1) / mazeWidth);
                    
                    // Initialize empty maze
                    cells = [];
                    walls = [];
                    mud = [];
                    for (let r = 0; r < mazeHeight; r++) {
                        cells[r] = [];
                        walls[r] = [];
                        mud[r] = [];
                        for (let c = 0; c < mazeWidth; c++) {
                            cells[r][c] = false; // Start with holes
                            walls[r][c] = {top: true, right: true, bottom: true, left: true};
                            mud[r][c] = {top: 0, right: 0, bottom: 0, left: 0};
                        }
                    }
                    
                    // Fill in cells and connections from maze data
                    for (const [srcStr, neighbors] of Object.entries(mazeData)) {
                        const src = parseInt(srcStr);
                        const srcRow = Math.floor(src / mazeWidth);
                        const srcCol = src % mazeWidth;
                        cells[srcRow][srcCol] = true;
                        
                        for (const [dstStr, weight] of Object.entries(neighbors)) {
                            const dst = parseInt(dstStr);
                            const dstRow = Math.floor(dst / mazeWidth);
                            const dstCol = dst % mazeWidth;
                            
                            // Determine direction
                            let side = '';
                            if (dstRow < srcRow) side = 'top';
                            else if (dstRow > srcRow) side = 'bottom';
                            else if (dstCol < srcCol) side = 'left';
                            else if (dstCol > srcCol) side = 'right';
                            
                            // No wall in this direction
                            walls[srcRow][srcCol][side] = false;
                            
                            // Set mud if weight > 1
                            if (weight > 1) {
                                mud[srcRow][srcCol][side] = weight;
                            }
                        }
                    }
                    
                    renderMaze();
                } catch (err) {
                    alert('Error loading maze file: ' + err.message);
                }
            };
            reader.readAsText(file);
            event.target.value = ''; // Reset file input
        }
        
        // Initialize maze on page load
        document.addEventListener('DOMContentLoaded', initMaze);
        // Also try to init immediately in case DOM is already loaded
        if (document.readyState !== 'loading') {
            initMaze();
        }
    </script>

Using the Maze Builder
----------------------

**Tools:**

- **Cell**: Click on a cell to toggle it between a valid cell (light gray) and a hole (dark). Holes are not part of the maze.
- **Wall**: Click on the edges between cells to add or remove walls. Walls block movement between adjacent cells.
- **Mud**: Click on edges between cells to add mud. Set the mud value first (the number of turns required to cross). Click again to remove mud.

**Maze Controls:**

- Use the **+** and **−** buttons around the maze to add or remove rows and columns.
- Check **Show indices** to display the cell index numbers (useful for debugging).

**Save/Load:**

- Click **Save** to download your maze as a JSON file.
- Click **Load** to import a previously saved maze.

Using the Maze in PyRat
-----------------------

Once you've saved your maze, you can load it in your PyRat game:

.. code-block:: python

    import json
    from pyrat import Game

    # Load the maze from file
    with open("pyrat_maze.json", "r") as f:
        maze = json.load(f)

    # Create a game with the custom maze
    game = Game(fixed_maze=maze)
