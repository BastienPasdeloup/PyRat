Maze Builder
============

This interactive tool allows you to create custom mazes for PyRat.
Use the controls below to build your maze, then save it as a file to use in your games.

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
            display: block;
            max-width: 100%;
            max-height: 70vh;
            overflow: auto;
            padding: 10px;
        }
        
        .maze-inner {
            display: inline-flex;
            flex-direction: column;
            align-items: center;
            gap: 5px;
            min-width: 100%;
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
            position: relative;
            font-size: 10px;
            font-weight: bold;
            transition: background 0.1s;
        }
        
        .maze-cell.hole {
            background: #333;
        }
        
        .maze-cell.hole::after {
            content: '';
        }
        
        /* Custom red cross cursor for removal actions */
        .cursor-remove {
            cursor: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 20 20'%3E%3Cline x1='4' y1='4' x2='16' y2='16' stroke='%23dc3545' stroke-width='3' stroke-linecap='round'/%3E%3Cline x1='16' y1='4' x2='4' y2='16' stroke='%23dc3545' stroke-width='3' stroke-linecap='round'/%3E%3C/svg%3E") 10 10, crosshair;
        }
        
        /* Cell/Hole tool: pointer on cells (will add hole), red cross on holes (will remove hole) */
        .maze-grid.tool-cell .maze-cell:not(.hole) {
            cursor: pointer;
        }
        .maze-grid.tool-cell .maze-cell.hole {
            cursor: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 20 20'%3E%3Cline x1='4' y1='4' x2='16' y2='16' stroke='%23dc3545' stroke-width='3' stroke-linecap='round'/%3E%3Cline x1='16' y1='4' x2='4' y2='16' stroke='%23dc3545' stroke-width='3' stroke-linecap='round'/%3E%3C/svg%3E") 10 10, crosshair;
        }
        
        /* Cheese tool: pointer on cells without cheese (add), red cross on cells with cheese (remove), not-allowed on holes */
        .maze-grid.tool-cheese .maze-cell:not(.hole):not(.has-cheese) {
            cursor: pointer;
        }
        .maze-grid.tool-cheese .maze-cell.hole {
            cursor: not-allowed;
        }
        .maze-grid.tool-cheese .maze-cell.has-cheese {
            cursor: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 20 20'%3E%3Cline x1='4' y1='4' x2='16' y2='16' stroke='%23dc3545' stroke-width='3' stroke-linecap='round'/%3E%3Cline x1='16' y1='4' x2='4' y2='16' stroke='%23dc3545' stroke-width='3' stroke-linecap='round'/%3E%3C/svg%3E") 10 10, crosshair;
        }
        
        /* Wall/mud tools: not-allowed on cells (must click edges), specific cursors on edges */
        .maze-grid.tool-wall .maze-cell,
        .maze-grid.tool-mud .maze-cell {
            cursor: not-allowed;
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
            left: 0;
            right: 0;
            height: 6px;
        }
        
        .maze-cell .wall-bottom {
            bottom: -2px;
            left: 0;
            right: 0;
            height: 6px;
        }
        
        .maze-cell .wall-left {
            left: -2px;
            top: 0;
            bottom: 0;
            width: 6px;
        }
        
        .maze-cell .wall-right {
            right: -2px;
            top: 0;
            bottom: 0;
            width: 6px;
        }
        
        .maze-cell .wall-top.active,
        .maze-cell .wall-bottom.active,
        .maze-cell .wall-left.active,
        .maze-cell .wall-right.active {
            background: #333;
        }
        
        /* Edge hover for wall/mud tools */
        .maze-grid.tool-wall .maze-cell:not(.hole) .wall-top.clickable:hover,
        .maze-grid.tool-wall .maze-cell:not(.hole) .wall-bottom.clickable:hover,
        .maze-grid.tool-wall .maze-cell:not(.hole) .wall-left.clickable:hover,
        .maze-grid.tool-wall .maze-cell:not(.hole) .wall-right.clickable:hover,
        .maze-grid.tool-mud .maze-cell:not(.hole) .wall-top.clickable:hover,
        .maze-grid.tool-mud .maze-cell:not(.hole) .wall-bottom.clickable:hover,
        .maze-grid.tool-mud .maze-cell:not(.hole) .wall-left.clickable:hover,
        .maze-grid.tool-mud .maze-cell:not(.hole) .wall-right.clickable:hover,
        .maze-grid.tool-wall .maze-cell:not(.hole) .wall-top.hover-pair,
        .maze-grid.tool-wall .maze-cell:not(.hole) .wall-bottom.hover-pair,
        .maze-grid.tool-wall .maze-cell:not(.hole) .wall-left.hover-pair,
        .maze-grid.tool-wall .maze-cell:not(.hole) .wall-right.hover-pair,
        .maze-grid.tool-mud .maze-cell:not(.hole) .wall-top.hover-pair,
        .maze-grid.tool-mud .maze-cell:not(.hole) .wall-bottom.hover-pair,
        .maze-grid.tool-mud .maze-cell:not(.hole) .wall-left.hover-pair,
        .maze-grid.tool-mud .maze-cell:not(.hole) .wall-right.hover-pair {
            background: rgba(0, 123, 255, 0.5);
        }
        
        /* Clickable edges: pointer (hand) to add, red cross to remove */
        .maze-grid.tool-wall .maze-cell:not(.hole) .clickable:not(.has-wall) {
            cursor: pointer;
        }
        .maze-grid.tool-wall .maze-cell:not(.hole) .clickable.has-wall {
            cursor: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 20 20'%3E%3Cline x1='4' y1='4' x2='16' y2='16' stroke='%23dc3545' stroke-width='3' stroke-linecap='round'/%3E%3Cline x1='16' y1='4' x2='4' y2='16' stroke='%23dc3545' stroke-width='3' stroke-linecap='round'/%3E%3C/svg%3E") 10 10, crosshair;
        }
        .maze-grid.tool-mud .maze-cell:not(.hole) .clickable:not(.has-mud) {
            cursor: pointer;
        }
        /* Mud with same value: red cross (will remove) */
        .maze-grid.tool-mud .maze-cell:not(.hole) .clickable.has-mud.mud-same-value {
            cursor: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 20 20'%3E%3Cline x1='4' y1='4' x2='16' y2='16' stroke='%23dc3545' stroke-width='3' stroke-linecap='round'/%3E%3Cline x1='16' y1='4' x2='4' y2='16' stroke='%23dc3545' stroke-width='3' stroke-linecap='round'/%3E%3C/svg%3E") 10 10, crosshair;
        }
        /* Mud with different value: pointer (will replace) */
        .maze-grid.tool-mud .maze-cell:not(.hole) .clickable.has-mud.mud-diff-value {
            cursor: pointer;
        }
        /* Fallback for mud without class yet */
        .maze-grid.tool-mud .maze-cell:not(.hole) .clickable.has-mud:not(.mud-same-value):not(.mud-diff-value) {
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
        
        .cheese-indicator {
            font-size: 20px;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            pointer-events: none;
            z-index: 1;
        }
        
        /* Cell hover for cheese tool */
        .maze-grid.tool-cheese .maze-cell:not(.hole):hover {
            background: #fffacd;
        }
    </style>

    <div class="maze-builder-container">
        <div class="toolbar">
            <div class="tool-group">
                <label>Tool:</label>
                <button class="tool-btn active" id="tool-cell" onclick="setTool('cell')">🔲 Hole</button>
                <button class="tool-btn" id="tool-wall" onclick="setTool('wall')">🧱 Wall</button>
                <button class="tool-btn" id="tool-mud" onclick="setTool('mud')">🟤 Mud</button>
                <button class="tool-btn" id="tool-cheese" onclick="setTool('cheese')">🧀 Cheese</button>
            </div>
            <div class="tool-group">
                <label>Mud value:</label>
                <input type="number" id="mud-value" class="mud-value-input" value="2" min="2" max="20" oninput="updateMudCursorClasses()">
            </div>
            <div class="tool-group">
                <label>Actions:</label>
                <button class="tool-btn action-btn" onclick="saveMaze()">💾 Save</button>
                <button class="tool-btn load-btn" onclick="document.getElementById('load-input').click()">📂 Load</button>
                <input type="file" id="load-input" class="hidden-input" accept=".py,.json" onchange="loadMaze(event)">
            </div>
            <div class="tool-group">
                <label>View:</label>
                <input type="checkbox" id="show-indices" onchange="toggleIndices()">
                <label for="show-indices" style="font-weight: normal;">Show indices</label>
            </div>
        </div>
        
        <div class="maze-wrapper">
            <div class="maze-inner">
                <div class="column-controls" id="top-controls"></div>
                <div class="maze-row-wrapper">
                    <div class="row-controls" id="left-controls"></div>
                    <div class="maze-grid" id="maze-grid"></div>
                    <div class="row-controls" id="right-controls"></div>
                </div>
                <div class="column-controls" id="bottom-controls"></div>
            </div>
        </div>
        
        <div class="status-bar" id="status-bar">
            Maze: <span id="maze-size">5 rows × 5 columns</span> | 
            Cells: <span id="cell-count">25</span> | 
            Current tool: <span id="current-tool">Hole (click to toggle)</span>
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
        // cheese[row][col] = true if cheese exists
        let cheese = [];
        
        function initMaze() {
            cells = [];
            walls = [];
            mud = [];
            cheese = [];
            for (let r = 0; r < mazeHeight; r++) {
                cells[r] = [];
                walls[r] = [];
                mud[r] = [];
                cheese[r] = [];
                for (let c = 0; c < mazeWidth; c++) {
                    cells[r][c] = true;
                    walls[r][c] = {top: false, right: false, bottom: false, left: false};
                    mud[r][c] = {top: 0, right: 0, bottom: 0, left: 0};
                    cheese[r][c] = false;
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
                case 'cell': toolDesc = 'Hole (click to toggle)'; break;
                case 'wall': toolDesc = 'Wall (click cell edges)'; break;
                case 'mud': toolDesc = 'Mud (click cell edges)'; break;
                case 'cheese': toolDesc = 'Cheese (click to toggle)'; break;
            }
            document.getElementById('current-tool').textContent = toolDesc;
            
            // Update mud cursor classes when switching to mud tool
            if (tool === 'mud') {
                updateMudCursorClasses();
            }
        }
        
        function updateMudCursorClasses() {
            const currentMudValue = parseInt(document.getElementById('mud-value').value) || 2;
            document.querySelectorAll('.has-mud').forEach(edge => {
                const edgeMudValue = parseInt(edge.dataset.mudValue) || 0;
                if (edgeMudValue === currentMudValue) {
                    edge.classList.add('mud-same-value');
                    edge.classList.remove('mud-diff-value');
                } else {
                    edge.classList.add('mud-diff-value');
                    edge.classList.remove('mud-same-value');
                }
            });
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
                        
                        // Add has-cheese class for cursor styling
                        if (cheese[r][c]) {
                            cellDiv.classList.add('has-cheese');
                        }
                        
                        // Add wall indicators with hover support
                        ['top', 'right', 'bottom', 'left'].forEach(side => {
                            const wallDiv = document.createElement('div');
                            // Check if neighbor is a hole or out of bounds (no wall in these cases)
                            let neighborRow = r, neighborCol = c;
                            switch(side) {
                                case 'top': neighborRow = r - 1; break;
                                case 'bottom': neighborRow = r + 1; break;
                                case 'left': neighborCol = c - 1; break;
                                case 'right': neighborCol = c + 1; break;
                            }
                            const isOuterEdge = neighborRow < 0 || neighborRow >= mazeHeight || 
                                               neighborCol < 0 || neighborCol >= mazeWidth;
                            const neighborIsHole = !isOuterEdge && !cells[neighborRow][neighborCol];
                            const canHaveWall = !isOuterEdge && !neighborIsHole;
                            const hasWall = canHaveWall && walls[r][c][side];
                            const hasMud = canHaveWall && mud[r][c][side] > 0;
                            const mudValue = mud[r][c][side];
                            wallDiv.className = 'wall-' + side + (hasWall ? ' active' : '') + (canHaveWall ? ' clickable' : '') + (hasWall ? ' has-wall' : '') + (hasMud ? ' has-mud' : '');
                            wallDiv.dataset.side = side;
                            wallDiv.dataset.row = r;
                            wallDiv.dataset.col = c;
                            if (hasMud) {
                                wallDiv.dataset.mudValue = mudValue;
                            }
                            if (canHaveWall) {
                                wallDiv.onclick = (e) => handleEdgeClick(e, r, c, side);
                                wallDiv.onmouseenter = (e) => handleEdgeHover(e, r, c, side, true);
                                wallDiv.onmouseleave = (e) => handleEdgeHover(e, r, c, side, false);
                            }
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
                        
                        // Add cheese indicator
                        if (cheese[r][c]) {
                            const cheeseDiv = document.createElement('div');
                            cheeseDiv.className = 'cheese-indicator';
                            cheeseDiv.textContent = '🧀';
                            cellDiv.appendChild(cheeseDiv);
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
            
            document.getElementById('maze-size').textContent = mazeHeight + ' rows × ' + mazeWidth + ' columns';
            document.getElementById('cell-count').textContent = cellCount;
            
            renderControls();
            
            // Update mud cursor classes after rendering
            if (currentTool === 'mud') {
                updateMudCursorClasses();
            }
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
                    // Reset walls, mud and cheese when removing cell
                    walls[row][col] = {top: false, right: false, bottom: false, left: false};
                    mud[row][col] = {top: 0, right: 0, bottom: 0, left: 0};
                    cheese[row][col] = false;
                    // Also remove walls/mud from neighbors pointing to this cell
                    if (row > 0) { walls[row-1][col].bottom = false; mud[row-1][col].bottom = 0; }
                    if (row < mazeHeight-1) { walls[row+1][col].top = false; mud[row+1][col].top = 0; }
                    if (col > 0) { walls[row][col-1].right = false; mud[row][col-1].right = 0; }
                    if (col < mazeWidth-1) { walls[row][col+1].left = false; mud[row][col+1].left = 0; }
                }
                renderMaze();
            } else if (currentTool === 'cheese') {
                if (cells[row][col]) {
                    cheese[row][col] = !cheese[row][col];
                    renderMaze();
                }
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
                if (!hasNeighbor) return; // Can't add wall along hole or edge
                walls[row][col][side] = !walls[row][col][side];
                // Clear mud if adding wall
                if (walls[row][col][side]) {
                    mud[row][col][side] = 0;
                }
                // Sync with neighbor
                walls[neighborRow][neighborCol][oppositeSide] = walls[row][col][side];
                if (walls[row][col][side]) {
                    mud[neighborRow][neighborCol][oppositeSide] = 0;
                }
                renderMaze();
            } else if (currentTool === 'mud') {
                if (!hasNeighbor) return; // Can't add mud to edge
                
                // Clear wall if adding mud
                if (walls[row][col][side]) {
                    walls[row][col][side] = false;
                    walls[neighborRow][neighborCol][oppositeSide] = false;
                }
                
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
            cheese.unshift([]);
            for (let c = 0; c < mazeWidth; c++) {
                cells[0][c] = true;
                walls[0][c] = {top: false, right: false, bottom: false, left: false};
                mud[0][c] = {top: 0, right: 0, bottom: 0, left: 0};
                cheese[0][c] = false;
            }
            renderMaze();
        }
        
        function removeRowTop() {
            if (mazeHeight <= 2) return;
            mazeHeight--;
            cells.shift();
            walls.shift();
            mud.shift();
            cheese.shift();
            renderMaze();
        }
        
        function addRowBottom() {
            mazeHeight++;
            cells.push([]);
            walls.push([]);
            mud.push([]);
            cheese.push([]);
            for (let c = 0; c < mazeWidth; c++) {
                cells[mazeHeight-1][c] = true;
                walls[mazeHeight-1][c] = {top: false, right: false, bottom: false, left: false};
                mud[mazeHeight-1][c] = {top: 0, right: 0, bottom: 0, left: 0};
                cheese[mazeHeight-1][c] = false;
            }
            renderMaze();
        }
        
        function removeRowBottom() {
            if (mazeHeight <= 2) return;
            mazeHeight--;
            cells.pop();
            walls.pop();
            mud.pop();
            cheese.pop();
            renderMaze();
        }
        
        function addColumnLeft() {
            mazeWidth++;
            for (let r = 0; r < mazeHeight; r++) {
                cells[r].unshift(true);
                walls[r].unshift({top: false, right: false, bottom: false, left: false});
                mud[r].unshift({top: 0, right: 0, bottom: 0, left: 0});
                cheese[r].unshift(false);
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
                cheese[r].shift();
            }
            renderMaze();
        }
        
        function addColumnRight() {
            mazeWidth++;
            for (let r = 0; r < mazeHeight; r++) {
                cells[r].push(true);
                walls[r].push({top: false, right: false, bottom: false, left: false});
                mud[r].push({top: 0, right: 0, bottom: 0, left: 0});
                cheese[r].push(false);
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
                cheese[r].pop();
            }
            renderMaze();
        }
        
        function saveMaze() {
            // Build PyRat maze format: dict[int, dict[int, int]]
            // Key is source vertex, value is dict of {destination: weight}
            const mazeDict = {};
            const cheeseList = [];
            
            for (let r = 0; r < mazeHeight; r++) {
                for (let c = 0; c < mazeWidth; c++) {
                    if (!cells[r][c]) continue;
                    
                    const cellIndex = getCellIndex(r, c);
                    mazeDict[cellIndex] = {};
                    
                    // Track cheese positions
                    if (cheese[r][c]) {
                        cheeseList.push(cellIndex);
                    }
                    
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
            
            // Format as Python dict (integer keys, not JSON string keys)
            const formatPythonDict = (obj) => {
                const entries = Object.entries(obj).map(([k, v]) => {
                    if (typeof v === 'object' && v !== null) {
                        return `${k}: ${formatPythonDict(v)}`;
                    }
                    return `${k}: ${v}`;
                });
                return `{${entries.join(', ')}}`;
            };
            
            // Format as Python tuple with maze dict and cheese list
            const pythonMaze = formatPythonDict(mazeDict);
            const pythonCheese = `[${cheeseList.join(', ')}]`;
            const pythonOutput = `(${pythonMaze}, ${pythonCheese})`;
            
            const blob = new Blob([pythonOutput], {type: 'text/plain'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'pyrat_maze.py';
            a.click();
            URL.revokeObjectURL(url);
        }
        
        function loadMaze(event) {
            const file = event.target.files[0];
            if (!file) return;
            
            const reader = new FileReader();
            reader.onload = function(e) {
                try {
                    // Parse Python tuple format: (maze_dict, cheese_list)
                    let content = e.target.result.trim();
                    
                    // Check if it's a tuple format (maze_dict, cheese_list)
                    let mazeContent = content;
                    let cheeseArray = [];
                    
                    if (content.startsWith('(') && content.endsWith(')')) {
                        // Find the matching closing brace of the first dict
                        let braceCount = 0;
                        let dictEnd = -1;
                        for (let i = 1; i < content.length; i++) {
                            if (content[i] === '{') braceCount++;
                            else if (content[i] === '}') {
                                braceCount--;
                                if (braceCount === 0) {
                                    dictEnd = i;
                                    break;
                                }
                            }
                        }
                        
                        if (dictEnd > 0) {
                            mazeContent = content.slice(1, dictEnd + 1);
                            // Extract cheese list
                            const remaining = content.slice(dictEnd + 1, -1).trim();
                            if (remaining.startsWith(',')) {
                                const cheeseStr = remaining.slice(1).trim();
                                if (cheeseStr.startsWith('[') && cheeseStr.endsWith(']')) {
                                    const cheeseListStr = cheeseStr.slice(1, -1).trim();
                                    if (cheeseListStr.length > 0) {
                                        cheeseArray = cheeseListStr.split(',').map(s => parseInt(s.trim()));
                                    }
                                }
                            }
                        }
                    }
                    
                    // Convert Python dict format to valid JSON by quoting keys
                    // Replace unquoted integer keys with quoted ones
                    const jsonContent = mazeContent.replace(/(\{|,)\s*(\d+)\s*:/g, '$1"$2":');
                    const mazeData = JSON.parse(jsonContent);
                    
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
                    cheese = [];
                    for (let r = 0; r < mazeHeight; r++) {
                        cells[r] = [];
                        walls[r] = [];
                        mud[r] = [];
                        cheese[r] = [];
                        for (let c = 0; c < mazeWidth; c++) {
                            cells[r][c] = false; // Start with holes
                            walls[r][c] = {top: false, right: false, bottom: false, left: false}; // No walls for holes
                            mud[r][c] = {top: 0, right: 0, bottom: 0, left: 0};
                            cheese[r][c] = false;
                        }
                    }
                    
                    // Set cheese from loaded data
                    for (const idx of cheeseArray) {
                        const r = Math.floor(idx / mazeWidth);
                        const c = idx % mazeWidth;
                        if (r >= 0 && r < mazeHeight && c >= 0 && c < mazeWidth) {
                            cheese[r][c] = true;
                        }
                    }
                    
                    // Fill in cells and connections from maze data
                    for (const [srcStr, neighbors] of Object.entries(mazeData)) {
                        const src = parseInt(srcStr);
                        const srcRow = Math.floor(src / mazeWidth);
                        const srcCol = src % mazeWidth;
                        cells[srcRow][srcCol] = true;
                        // Initialize walls only for interior edges (not at borders)
                        walls[srcRow][srcCol] = {
                            top: srcRow > 0,
                            right: srcCol < mazeWidth - 1,
                            bottom: srcRow < mazeHeight - 1,
                            left: srcCol > 0
                        };
                        
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
                    
                    // Clear walls that face holes
                    for (let r = 0; r < mazeHeight; r++) {
                        for (let c = 0; c < mazeWidth; c++) {
                            if (!cells[r][c]) continue;
                            // Check each direction for holes
                            if (r > 0 && !cells[r-1][c]) walls[r][c].top = false;
                            if (r < mazeHeight-1 && !cells[r+1][c]) walls[r][c].bottom = false;
                            if (c > 0 && !cells[r][c-1]) walls[r][c].left = false;
                            if (c < mazeWidth-1 && !cells[r][c+1]) walls[r][c].right = false;
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

- **Hole**: Click on a cell to toggle it between a valid cell (light gray) and a hole (dark). Holes are not part of the maze.
- **Wall**: Click on the edges between cells to add or remove walls. Walls block movement between adjacent cells.
- **Mud**: Click on edges between cells to add mud. Set the mud value first (the number of turns required to cross). Click again to remove mud.
- **Cheese**: Click on cells to place or remove cheese. Cheese positions will be saved with your maze.

**Maze Controls:**

- Use the **+** and **−** buttons around the maze to add or remove rows and columns.
- Check **Show indices** to display the cell index numbers (useful for debugging).

**Save/Load:**

- Click **Save** to download your maze as a file.
- Click **Load** to import a previously saved maze.

Using the Maze in PyRat
-----------------------

Once you've saved your maze, you can load it in your PyRat game.
The saved file contains a Python tuple ``(maze_dict, cheese_list)`` with the maze structure and cheese positions:

.. code-block:: python

    # Import the necessary modules
    import ast
    from pyrat import Game

    # Load the maze and cheese from saved file
    with open("pyrat_maze.py", "r") as f:
        maze_dict, cheese_list = ast.literal_eval(f.read())

    # Create a game with the custom maze and cheese
    game = Game(fixed_maze=maze_dict, fixed_cheese=cheese_list)

You can also create a ``MazeFromDict`` object if you prefer.
This has the advantages of validating the maze structure and providing additional methods.

.. code-block:: python

    # Import the necessary modules
    import ast
    from pyrat import Game, MazeFromDict

    # Load the maze and cheese from saved file
    with open("pyrat_maze.py", "r") as f:
        maze_dict, cheese_list = ast.literal_eval(f.read())

    # Create a MazeFromDict object
    maze = MazeFromDict(maze_dict)

    # Create a game with the maze object and cheese
    game = Game(fixed_maze=maze, fixed_cheese=cheese_list)

**Remarks:**

- When starting a game, players are added before the cheese.
  Therefore, make sure that fixed cheese positions do not overlap with player starting positions.

- If you only want to use this tool to design a maze, just remove the `fixed_cheese` parameter when creating the `Game` object.
  Cheese will then be placed randomly by the game.