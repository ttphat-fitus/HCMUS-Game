// HCMUS Battle Royale Game - JavaScript Engine
// Built with OOP principles

class Vector2D {
    constructor(x = 0, y = 0) {
        this.x = x;
        this.y = y;
    }
    
    add(other) {
        return new Vector2D(this.x + other.x, this.y + other.y);
    }
    
    subtract(other) {
        return new Vector2D(this.x - other.x, this.y - other.y);
    }
    
    multiply(scalar) {
        return new Vector2D(this.x * scalar, this.y * scalar);
    }
    
    magnitude() {
        return Math.sqrt(this.x * this.x + this.y * this.y);
    }
    
    normalized() {
        const mag = this.magnitude();
        if (mag > 0) {
            return new Vector2D(this.x / mag, this.y / mag);
        }
        return new Vector2D(0, 0);
    }
    
    distanceTo(other) {
        return this.subtract(other).magnitude();
    }
}

class GameObject {
    constructor(id, position, radius = 10) {
        this.id = id;
        this.position = position;
        this.radius = radius;
        this.isActive = true;
    }
    
    update(deltaTime) {
        // Base update method
    }
    
    render(ctx, camera) {
        // Base render method
    }
    
    isCollidingWith(other) {
        return this.position.distanceTo(other.position) < (this.radius + other.radius);
    }
}

class Player extends GameObject {
    constructor(id, name, position) {
        super(id, position, 15);
        this.name = name;
        this.velocity = new Vector2D();
        this.direction = new Vector2D(1, 0);
        this.health = 100;
        this.maxHealth = 100;
        this.armor = 0;
        this.maxArmor = 100;
        this.isAlive = true;
        this.kills = 0;
        this.deaths = 0;
        this.speed = 200;
        this.color = '#00ff00';
        this.inventory = [];
        this.currentWeapon = null;
        this.isShooting = false;
        this.lastShotTime = 0;
    }
    
    update(deltaTime) {
        if (!this.isAlive) return;
        
        // Update position based on velocity
        this.position = this.position.add(this.velocity.multiply(deltaTime));
        
        // Reset velocity
        this.velocity = new Vector2D();
    }
    
    move(direction) {
        if (!this.isAlive) return;
        
        this.direction = direction.normalized();
        this.velocity = this.direction.multiply(this.speed);
    }
    
    shoot() {
        if (!this.isAlive || !this.canShoot()) return false;
        
        this.isShooting = true;
        this.lastShotTime = Date.now();
        return true;
    }
    
    canShoot() {
        if (!this.currentWeapon) return false;
        return (Date.now() - this.lastShotTime) >= (1000 / this.currentWeapon.fireRate);
    }
    
    takeDamage(damage) {
        if (!this.isAlive) return;
        
        let remainingDamage = damage;
        
        // Armor absorbs damage first
        if (this.armor > 0) {
            if (this.armor >= remainingDamage) {
                this.armor -= remainingDamage;
                remainingDamage = 0;
            } else {
                remainingDamage -= this.armor;
                this.armor = 0;
            }
        }
        
        // Remaining damage goes to health
        if (remainingDamage > 0) {
            this.health -= remainingDamage;
            if (this.health <= 0) {
                this.health = 0;
                this.die();
            }
        }
    }
    
    heal(amount) {
        if (!this.isAlive) return;
        this.health = Math.min(this.health + amount, this.maxHealth);
    }
    
    addArmor(amount) {
        if (!this.isAlive) return;
        this.armor = Math.min(this.armor + amount, this.maxArmor);
    }
    
    die() {
        this.isAlive = false;
        this.deaths++;
        console.log(`Player ${this.name} has died!`);
    }
    
    render(ctx, camera) {
        if (!this.isAlive) return;
        
        const screenPos = camera.worldToScreen(this.position);
        
        // Draw player body
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(screenPos.x, screenPos.y, this.radius, 0, Math.PI * 2);
        ctx.fill();
        
        // Draw direction indicator
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(screenPos.x, screenPos.y);
        ctx.lineTo(
            screenPos.x + this.direction.x * this.radius,
            screenPos.y + this.direction.y * this.radius
        );
        ctx.stroke();
        
        // Draw name
        ctx.fillStyle = '#ffffff';
        ctx.font = '12px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(this.name, screenPos.x, screenPos.y - this.radius - 10);
        
        // Draw health bar
        this.renderHealthBar(ctx, screenPos);
    }
    
    renderHealthBar(ctx, screenPos) {
        const barWidth = 30;
        const barHeight = 4;
        const barY = screenPos.y - this.radius - 20;
        
        // Background
        ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
        ctx.fillRect(screenPos.x - barWidth/2, barY, barWidth, barHeight);
        
        // Health
        const healthPercent = this.health / this.maxHealth;
        ctx.fillStyle = healthPercent > 0.5 ? '#00ff00' : healthPercent > 0.25 ? '#ffff00' : '#ff0000';
        ctx.fillRect(screenPos.x - barWidth/2, barY, barWidth * healthPercent, barHeight);
        
        // Armor
        if (this.armor > 0) {
            const armorPercent = this.armor / this.maxArmor;
            ctx.fillStyle = '#0066ff';
            ctx.fillRect(screenPos.x - barWidth/2, barY - 6, barWidth * armorPercent, 2);
        }
    }
}

class Enemy extends GameObject {
    constructor(id, type, name, position) {
        super(id, position, 12);
        this.type = type;
        this.name = name;
        this.velocity = new Vector2D();
        this.direction = new Vector2D(1, 0);
        this.health = 100;
        this.maxHealth = 100;
        this.isAlive = true;
        this.detectionRange = 150;
        this.attackRange = 50;
        this.damage = 20;
        this.attackSpeed = 1.0;
        this.speed = 100;
        this.lastAttackTime = 0;
        this.currentTarget = null;
        
        this.initializeStats();
    }
    
    initializeStats() {
        switch (this.type) {
            case 'zombie':
                this.health = 80;
                this.maxHealth = 80;
                this.speed = 80;
                this.damage = 15;
                this.attackSpeed = 0.8;
                this.detectionRange = 120;
                this.attackRange = 40;
                this.color = '#8B4513';
                break;
            case 'bandit':
                this.health = 100;
                this.maxHealth = 100;
                this.speed = 120;
                this.damage = 25;
                this.attackSpeed = 1.2;
                this.detectionRange = 180;
                this.attackRange = 60;
                this.color = '#FF4500';
                break;
            case 'boss':
                this.health = 200;
                this.maxHealth = 200;
                this.speed = 100;
                this.damage = 40;
                this.attackSpeed = 0.6;
                this.detectionRange = 250;
                this.attackRange = 80;
                this.color = '#8B0000';
                this.radius = 20;
                break;
        }
    }
    
    update(deltaTime, players) {
        if (!this.isAlive) return;
        
        this.findTarget(players);
        this.updateAI(deltaTime);
        
        // Update position
        this.position = this.position.add(this.velocity.multiply(deltaTime));
        this.velocity = new Vector2D();
    }
    
    findTarget(players) {
        let closestTarget = null;
        let closestDistance = this.detectionRange;
        
        for (const player of players) {
            if (!player.isAlive) continue;
            
            const distance = this.position.distanceTo(player.position);
            if (distance < closestDistance) {
                closestTarget = player;
                closestDistance = distance;
            }
        }
        
        this.currentTarget = closestTarget;
    }
    
    updateAI(deltaTime) {
        if (!this.currentTarget) return;
        
        const distance = this.position.distanceTo(this.currentTarget.position);
        
        if (distance <= this.attackRange) {
            this.attack();
        } else if (distance <= this.detectionRange) {
            this.chase();
        }
    }
    
    chase() {
        const direction = this.currentTarget.position.subtract(this.position).normalized();
        this.velocity = direction.multiply(this.speed);
        this.direction = direction;
    }
    
    attack() {
        if (!this.canAttack()) return;
        
        this.currentTarget.takeDamage(this.damage);
        this.lastAttackTime = Date.now();
    }
    
    canAttack() {
        return (Date.now() - this.lastAttackTime) >= (1000 / this.attackSpeed);
    }
    
    takeDamage(damage) {
        if (!this.isAlive) return;
        
        this.health -= damage;
        if (this.health <= 0) {
            this.health = 0;
            this.die();
        }
    }
    
    die() {
        this.isAlive = false;
        console.log(`Enemy ${this.name} has died!`);
    }
    
    render(ctx, camera) {
        if (!this.isAlive) return;
        
        const screenPos = camera.worldToScreen(this.position);
        
        // Draw enemy body
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(screenPos.x, screenPos.y, this.radius, 0, Math.PI * 2);
        ctx.fill();
        
        // Draw health bar
        const barWidth = 25;
        const barHeight = 3;
        const barY = screenPos.y - this.radius - 15;
        
        ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
        ctx.fillRect(screenPos.x - barWidth/2, barY, barWidth, barHeight);
        
        const healthPercent = this.health / this.maxHealth;
        ctx.fillStyle = healthPercent > 0.5 ? '#00ff00' : healthPercent > 0.25 ? '#ffff00' : '#ff0000';
        ctx.fillRect(screenPos.x - barWidth/2, barY, barWidth * healthPercent, barHeight);
    }
}

class Item extends GameObject {
    constructor(type, name, position, value) {
        super(0, position, 8);
        this.type = type;
        this.name = name;
        this.value = value;
        this.isActive = true;
    }
    
    render(ctx, camera) {
        if (!this.isActive) return;
        
        const screenPos = camera.worldToScreen(this.position);
        
        // Draw item
        ctx.fillStyle = this.getColor();
        ctx.beginPath();
        ctx.arc(screenPos.x, screenPos.y, this.radius, 0, Math.PI * 2);
        ctx.fill();
        
        // Draw border
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 1;
        ctx.stroke();
        
        // Draw name
        ctx.fillStyle = '#ffffff';
        ctx.font = '10px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(this.name, screenPos.x, screenPos.y + this.radius + 12);
    }
    
    getColor() {
        switch (this.type) {
            case 'health': return '#ff0000';
            case 'ammo': return '#ffff00';
            case 'weapon': return '#00ff00';
            case 'armor': return '#0066ff';
            default: return '#ffffff';
        }
    }
}

class Obstacle extends GameObject {
    constructor(id, type, name, position) {
        super(id, position, 25);
        this.type = type;
        this.name = name;
        this.size = new Vector2D(50, 50);
        this.isDestructible = false;
        this.health = 100;
        this.maxHealth = 100;
        
        this.initializeStats();
    }
    
    initializeStats() {
        switch (this.type) {
            case 'tree':
                this.size = new Vector2D(40, 60);
                this.radius = 20;
                this.isDestructible = false;
                this.health = 200;
                this.maxHealth = 200;
                this.color = '#228B22';
                break;
            case 'rock':
                this.size = new Vector2D(30, 30);
                this.radius = 15;
                this.isDestructible = true;
                this.health = 150;
                this.maxHealth = 150;
                this.color = '#696969';
                break;
            case 'building':
                this.size = new Vector2D(100, 80);
                this.radius = 50;
                this.isDestructible = false;
                this.health = 500;
                this.maxHealth = 500;
                this.color = '#8B4513';
                break;
        }
    }
    
    render(ctx, camera) {
        const screenPos = camera.worldToScreen(this.position);
        
        // Draw obstacle
        ctx.fillStyle = this.color;
        ctx.fillRect(
            screenPos.x - this.size.x/2,
            screenPos.y - this.size.y/2,
            this.size.x,
            this.size.y
        );
        
        // Draw border
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 1;
        ctx.strokeRect(
            screenPos.x - this.size.x/2,
            screenPos.y - this.size.y/2,
            this.size.x,
            this.size.y
        );
    }
}

class Camera {
    constructor(width, height) {
        this.width = width;
        this.height = height;
        this.position = new Vector2D(0, 0);
        this.zoom = 1;
    }
    
    follow(target) {
        this.position = target.position;
    }
    
    worldToScreen(worldPos) {
        const screenX = (worldPos.x - this.position.x) * this.zoom + this.width / 2;
        const screenY = (worldPos.y - this.position.y) * this.zoom + this.height / 2;
        return new Vector2D(screenX, screenY);
    }
    
    screenToWorld(screenPos) {
        const worldX = (screenPos.x - this.width / 2) / this.zoom + this.position.x;
        const worldY = (screenPos.y - this.height / 2) / this.zoom + this.position.y;
        return new Vector2D(worldX, worldY);
    }
}

class GameEngine {
    constructor() {
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.camera = new Camera(this.canvas.width, this.canvas.height);
        
        this.players = [];
        this.enemies = [];
        this.obstacles = [];
        this.items = [];
        
        this.gameState = 'waiting'; // waiting, playing, gameOver
        this.gameWidth = 1600;
        this.gameHeight = 900;
        this.redZoneRadius = 800;
        this.redZoneCenter = new Vector2D(this.gameWidth / 2, this.gameHeight / 2);
        this.redZoneDamage = 10;
        this.redZoneShrinkRate = 50;
        
        this.lastUpdate = Date.now();
        this.isRunning = false;
        
        this.setupEventListeners();
        this.initialize();
    }
    
    initialize() {
        this.spawnObstacles();
        this.spawnEnemies();
        this.updateUI();
    }
    
    setupEventListeners() {
        // Mouse events
        this.canvas.addEventListener('mousemove', (e) => this.handleMouseMove(e));
        this.canvas.addEventListener('click', (e) => this.handleMouseClick(e));
        
        // Keyboard events
        document.addEventListener('keydown', (e) => this.handleKeyDown(e));
        document.addEventListener('keyup', (e) => this.handleKeyUp(e));
        
        // UI events
        document.getElementById('startGame').addEventListener('click', () => this.startGame());
        document.getElementById('joinGame').addEventListener('click', () => this.showMenu());
        document.getElementById('confirmJoin').addEventListener('click', () => this.joinGame());
        document.getElementById('cancelMenu').addEventListener('click', () => this.hideMenu());
    }
    
    startGame() {
        if (this.gameState === 'waiting') {
            this.gameState = 'playing';
            this.isRunning = true;
            this.gameLoop();
        }
    }
    
    joinGame() {
        const name = document.getElementById('nameInput').value || 'Player';
        const spawnPos = this.getRandomPosition();
        const player = new Player(this.players.length, name, spawnPos);
        this.players.push(player);
        this.hideMenu();
        this.updateUI();
    }
    
    showMenu() {
        document.getElementById('gameMenu').classList.remove('hidden');
    }
    
    hideMenu() {
        document.getElementById('gameMenu').classList.add('hidden');
    }
    
    gameLoop() {
        if (!this.isRunning) return;
        
        const now = Date.now();
        const deltaTime = (now - this.lastUpdate) / 1000;
        this.lastUpdate = now;
        
        this.update(deltaTime);
        this.render();
        
        requestAnimationFrame(() => this.gameLoop());
    }
    
    update(deltaTime) {
        // Update players
        for (const player of this.players) {
            player.update(deltaTime);
        }
        
        // Update enemies
        for (const enemy of this.enemies) {
            enemy.update(deltaTime, this.players);
        }
        
        // Update red zone
        this.updateRedZone(deltaTime);
        
        // Spawn items
        this.spawnItems();
        
        // Check collisions
        this.checkCollisions();
        
        // Update camera to follow first player
        if (this.players.length > 0 && this.players[0].isAlive) {
            this.camera.follow(this.players[0]);
        }
        
        // Check game over
        if (this.isGameOver()) {
            this.endGame();
        }
        
        this.updateUI();
    }
    
    updateRedZone(deltaTime) {
        this.redZoneRadius -= this.redZoneShrinkRate * deltaTime;
        this.redZoneRadius = Math.max(this.redZoneRadius, 100);
        
        // Apply damage to players in red zone
        for (const player of this.players) {
            if (player.isAlive && this.isInRedZone(player.position)) {
                player.takeDamage(this.redZoneDamage * deltaTime);
            }
        }
    }
    
    isInRedZone(position) {
        return position.distanceTo(this.redZoneCenter) > this.redZoneRadius;
    }
    
    spawnItems() {
        if (Math.random() < 0.01) {
            const pos = this.getRandomPosition();
            const types = ['health', 'ammo', 'weapon', 'armor'];
            const type = types[Math.floor(Math.random() * types.length)];
            const item = new Item(type, `${type.charAt(0).toUpperCase() + type.slice(1)}`, pos, 50);
            this.items.push(item);
        }
    }
    
    checkCollisions() {
        // Player vs Item collisions
        for (let i = this.items.length - 1; i >= 0; i--) {
            const item = this.items[i];
            for (const player of this.players) {
                if (player.isAlive && item.isActive && player.isCollidingWith(item)) {
                    this.pickUpItem(player, item);
                    this.items.splice(i, 1);
                    break;
                }
            }
        }
        
        // Player vs Obstacle collisions
        for (const player of this.players) {
            for (const obstacle of this.obstacles) {
                if (player.isAlive && player.isCollidingWith(obstacle)) {
                    const direction = player.position.subtract(obstacle.position).normalized();
                    player.position = player.position.add(direction.multiply(5));
                }
            }
        }
    }
    
    pickUpItem(player, item) {
        switch (item.type) {
            case 'health':
                player.heal(item.value);
                break;
            case 'armor':
                player.addArmor(item.value);
                break;
            case 'ammo':
                // Add ammo to current weapon
                break;
            case 'weapon':
                // Add weapon to inventory
                break;
        }
    }
    
    spawnObstacles() {
        for (let i = 0; i < 20; i++) {
            const pos = this.getRandomPosition();
            const types = ['tree', 'rock', 'building'];
            const type = types[Math.floor(Math.random() * types.length)];
            const obstacle = new Obstacle(i, type, `${type}_${i}`, pos);
            this.obstacles.push(obstacle);
        }
    }
    
    spawnEnemies() {
        for (let i = 0; i < 10; i++) {
            const pos = this.getRandomPosition();
            const types = ['zombie', 'bandit'];
            const type = types[Math.floor(Math.random() * types.length)];
            const enemy = new Enemy(i, type, `${type}_${i}`, pos);
            this.enemies.push(enemy);
        }
    }
    
    getRandomPosition() {
        const margin = 50;
        const x = margin + Math.random() * (this.gameWidth - 2 * margin);
        const y = margin + Math.random() * (this.gameHeight - 2 * margin);
        return new Vector2D(x, y);
    }
    
    render() {
        // Clear canvas
        this.ctx.fillStyle = '#2d5016';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw red zone
        this.renderRedZone();
        
        // Draw obstacles
        for (const obstacle of this.obstacles) {
            obstacle.render(this.ctx, this.camera);
        }
        
        // Draw items
        for (const item of this.items) {
            item.render(this.ctx, this.camera);
        }
        
        // Draw enemies
        for (const enemy of this.enemies) {
            enemy.render(this.ctx, this.camera);
        }
        
        // Draw players
        for (const player of this.players) {
            player.render(this.ctx, this.camera);
        }
    }
    
    renderRedZone() {
        const center = this.camera.worldToScreen(this.redZoneCenter);
        const radius = this.redZoneRadius * this.camera.zoom;
        
        // Draw red zone border
        this.ctx.strokeStyle = 'rgba(255, 0, 0, 0.8)';
        this.ctx.lineWidth = 3;
        this.ctx.beginPath();
        this.ctx.arc(center.x, center.y, radius, 0, Math.PI * 2);
        this.ctx.stroke();
        
        // Draw red zone fill
        this.ctx.fillStyle = 'rgba(255, 0, 0, 0.1)';
        this.ctx.fill();
    }
    
    handleMouseMove(e) {
        const rect = this.canvas.getBoundingClientRect();
        const mousePos = new Vector2D(e.clientX - rect.left, e.clientY - rect.top);
        const worldPos = this.camera.screenToWorld(mousePos);
        
        // Update player direction
        if (this.players.length > 0 && this.players[0].isAlive) {
            this.players[0].direction = worldPos.subtract(this.players[0].position).normalized();
        }
    }
    
    handleMouseClick(e) {
        if (this.players.length > 0 && this.players[0].isAlive) {
            this.players[0].shoot();
        }
    }
    
    handleKeyDown(e) {
        if (this.players.length === 0 || !this.players[0].isAlive) return;
        
        const player = this.players[0];
        let direction = new Vector2D();
        
        switch (e.key.toLowerCase()) {
            case 'w':
                direction.y -= 1;
                break;
            case 's':
                direction.y += 1;
                break;
            case 'a':
                direction.x -= 1;
                break;
            case 'd':
                direction.x += 1;
                break;
        }
        
        if (direction.magnitude() > 0) {
            player.move(direction);
        }
    }
    
    handleKeyUp(e) {
        // Handle key up events if needed
    }
    
    updateUI() {
        if (this.players.length > 0) {
            const player = this.players[0];
            
            document.getElementById('playerName').textContent = player.name;
            document.getElementById('healthText').textContent = `${Math.round(player.health)}/${player.maxHealth}`;
            document.getElementById('armorText').textContent = `${Math.round(player.armor)}/${player.maxArmor}`;
            
            // Update health bar
            const healthPercent = player.health / player.maxHealth;
            document.getElementById('healthFill').style.width = `${healthPercent * 100}%`;
            
            // Update armor bar
            const armorPercent = player.armor / player.maxArmor;
            document.getElementById('armorFill').style.width = `${armorPercent * 100}%`;
            
            // Update stats
            const alivePlayers = this.players.filter(p => p.isAlive).length;
            document.getElementById('playersAlive').textContent = `Players Alive: ${alivePlayers}`;
            document.getElementById('redZoneInfo').textContent = `Red Zone: ${Math.round(this.redZoneRadius)}m`;
            document.getElementById('kills').textContent = `Kills: ${player.kills}`;
        }
    }
    
    isGameOver() {
        const alivePlayers = this.players.filter(p => p.isAlive);
        return alivePlayers.length <= 1;
    }
    
    endGame() {
        this.isRunning = false;
        this.gameState = 'gameOver';
        
        if (this.players.length > 0) {
            const player = this.players[0];
            document.getElementById('finalKills').textContent = player.kills;
            document.getElementById('gameOverScreen').classList.remove('hidden');
        }
    }
}

// Initialize game when page loads
document.addEventListener('DOMContentLoaded', () => {
    // Hide loading screen
    setTimeout(() => {
        document.getElementById('loadingScreen').classList.add('hidden');
        
        // Initialize game engine
        window.gameEngine = new GameEngine();
    }, 2000);
});
