#include "../include/Game.h"
#include "../include/Utils.h"
#include <iostream>
#include <algorithm>

Game::Game(int width, int height, int maxPlayers)
    : currentState(GameState::WAITING), gameWidth(width), gameHeight(height),
      playerCount(0), maxPlayers(maxPlayers), redZoneRadius(RED_ZONE_INITIAL_RADIUS),
      redZoneDamage(RED_ZONE_DAMAGE_PER_SECOND), redZoneShrinkRate(RED_ZONE_SHRINK_RATE),
      redZoneCenter(width / 2, height / 2), deltaTime(0) {
    
    lastUpdate = std::chrono::steady_clock::now();
    rng.seed(std::chrono::steady_clock::now().time_since_epoch().count());
}

Game::~Game() = default;

void Game::initialize() {
    std::cout << "Initializing HCMUS Battle Royale Game..." << std::endl;
    initializeRedZone();
    spawnObstacles();
    currentState = GameState::WAITING;
}

void Game::update() {
    auto now = std::chrono::steady_clock::now();
    deltaTime = std::chrono::duration<double>(now - lastUpdate).count();
    lastUpdate = now;
    
    if (currentState == GameState::PLAYING) {
        updatePlayers();
        updateEnemies();
        updateItems();
        updateRedZone();
        checkCollisions();
        
        if (isGameOver()) {
            currentState = GameState::GAME_OVER;
        }
    }
}

void Game::render() {
    // Web rendering will be handled by JavaScript
}

void Game::reset() {
    players.clear();
    enemies.clear();
    obstacles.clear();
    items.clear();
    playerCount = 0;
    currentState = GameState::WAITING;
    initialize();
}

void Game::addPlayer(const std::string& name, double x, double y) {
    if (playerCount >= maxPlayers) return;
    
    Vector2D spawnPos = getRandomPosition();
    auto player = std::make_unique<Player>(playerCount, name, spawnPos);
    players.push_back(std::move(player));
    playerCount++;
    
    if (currentState == GameState::WAITING && playerCount >= 2) {
        currentState = GameState::PLAYING;
    }
}

void Game::removePlayer(int playerId) {
    auto it = std::find_if(players.begin(), players.end(),
                          [playerId](const std::unique_ptr<Player>& player) {
                              return player->getId() == playerId;
                          });
    
    if (it != players.end()) {
        players.erase(it);
        playerCount--;
    }
}

Player* Game::getPlayer(int playerId) {
    auto it = std::find_if(players.begin(), players.end(),
                          [playerId](const std::unique_ptr<Player>& player) {
                              return player->getId() == playerId;
                          });
    
    return (it != players.end()) ? it->get() : nullptr;
}

std::vector<Player*> Game::getAlivePlayers() {
    std::vector<Player*> alivePlayers;
    for (const auto& player : players) {
        if (player->getIsAlive()) {
            alivePlayers.push_back(player.get());
        }
    }
    return alivePlayers;
}

void Game::updateRedZone() {
    redZoneRadius -= redZoneShrinkRate * deltaTime;
    redZoneRadius = std::max(redZoneRadius, 100.0);
    
    for (auto& player : players) {
        if (player->getIsAlive() && isInRedZone(player->getPosition())) {
            player->takeDamage(redZoneDamage * deltaTime);
        }
    }
}

void Game::spawnItems() {
    if (Utils::randomDouble(0, 1) < 0.01) {
        Vector2D itemPos = getRandomPosition();
        auto item = std::make_unique<HealthItem>("Med Kit", 50);
        item->position = itemPos;
        items.push_back(std::move(item));
    }
}

void Game::checkCollisions() {
    // Basic collision detection
    for (auto& player : players) {
        for (auto& obstacle : obstacles) {
            if (player->getIsAlive() && 
                obstacle->isCollidingWith(player->getPosition(), player->getRadius())) {
                Vector2D direction = (player->getPosition() - obstacle->getPosition()).normalized();
                player->setPosition(player->getPosition() + direction * 5);
            }
        }
    }
}

void Game::handlePlayerDeath(int playerId) {
    Player* player = getPlayer(playerId);
    if (player) {
        // Drop all items in inventory (không copy vector unique_ptr)
        const auto& inventory = player->getInventory();
        for (const auto& item : inventory) {
            if (item && item->isActive) {
                // Tạo item mới cùng loại (ở đây chỉ demo với HealthItem, thực tế cần phân biệt loại)
                auto newItem = std::make_unique<HealthItem>(item->name, item->value);
                newItem->position = player->getPosition();
                newItem->isActive = true;
                items.push_back(std::move(newItem));
            }
        }
    }
}

bool Game::isGameOver() {
    return getAlivePlayers().size() <= 1;
}

void Game::initializeRedZone() {
    redZoneCenter = Vector2D(gameWidth / 2, gameHeight / 2);
    redZoneRadius = RED_ZONE_INITIAL_RADIUS;
}

void Game::spawnObstacles() {
    for (int i = 0; i < 20; i++) {
        Vector2D pos = getRandomPosition();
        ObstacleType type = static_cast<ObstacleType>(Utils::randomInt(0, 4));
        std::string name = "Obstacle_" + std::to_string(i);
        auto obstacle = std::make_unique<Obstacle>(i, type, name, pos);
        obstacles.push_back(std::move(obstacle));
    }
}

void Game::updatePlayers() {
    for (auto& player : players) {
        if (player->getIsAlive()) {
            player->update(deltaTime);
        }
    }
}

void Game::updateEnemies() {
    std::vector<Player*> alivePlayers = getAlivePlayers();
    for (auto& enemy : enemies) {
        if (enemy->getIsAlive()) {
            enemy->update(deltaTime, alivePlayers);
        }
    }
}

void Game::updateItems() {
    // Update items logic
}

bool Game::isInRedZone(const Vector2D& position) {
    return position.distanceTo(redZoneCenter) > redZoneRadius;
}

Vector2D Game::getRandomPosition() {
    double margin = 50;
    return Utils::randomPosition(margin, gameWidth - margin, margin, gameHeight - margin);
}
