#ifndef GAME_H
#define GAME_H

#include <vector>
#include <memory>
#include <random>
#include <chrono>
#include "Player.h"
#include "Enemy.h"
#include "Obstacle.h"
#include "Utils.h"

class Game {
public:
    // Game state
    enum class GameState {
        WAITING,
        PLAYING,
        GAME_OVER
    };
    
    // Game settings
    static const int INITIAL_PLAYER_HEALTH = 100;
    static const int INITIAL_PLAYER_AMMO = 30;
    static constexpr double PLAYER_SPEED = 200.0;
    static constexpr double BULLET_SPEED = 500.0;
    static constexpr double RED_ZONE_INITIAL_RADIUS = 800.0;
    static constexpr double RED_ZONE_DAMAGE_PER_SECOND = 10.0;
    static constexpr double RED_ZONE_SHRINK_RATE = 50.0; // pixels per second
    
private:
    // Game state
    GameState currentState;
    int gameWidth;
    int gameHeight;
    int playerCount;
    int maxPlayers;
    
    // Game objects
    std::vector<std::unique_ptr<Player>> players;
    std::vector<std::unique_ptr<Enemy>> enemies;
    std::vector<std::unique_ptr<Obstacle>> obstacles;
    std::vector<std::unique_ptr<Item>> items;
    
    // Game mechanics
    double redZoneRadius;
    double redZoneDamage;
    double redZoneShrinkRate;
    Vector2D redZoneCenter;
    
    // Timing
    std::chrono::steady_clock::time_point lastUpdate;
    double deltaTime;
    
    // Random generator
    std::mt19937 rng;
    
public:
    Game(int width = 1600, int height = 900, int maxPlayers = 50);
    ~Game();
    
    // Game lifecycle
    void initialize();
    void update();
    void render();
    void reset();
    
    // Player management
    void addPlayer(const std::string& name, double x, double y);
    void removePlayer(int playerId);
    Player* getPlayer(int playerId);
    std::vector<Player*> getAlivePlayers();
    
    // Game mechanics
    void updateRedZone();
    void spawnItems();
    void checkCollisions();
    void handlePlayerDeath(int playerId);
    bool isGameOver();
    
    // Getters
    GameState getState() const { return currentState; }
    int getPlayerCount() const { return playerCount; }
    int getMaxPlayers() const { return maxPlayers; }
    double getRedZoneRadius() const { return redZoneRadius; }
    Vector2D getRedZoneCenter() const { return redZoneCenter; }
    
    // Setters
    void setState(GameState state) { currentState = state; }
    
private:
    void initializeRedZone();
    void spawnObstacles();
    void updatePlayers();
    void updateEnemies();
    void updateItems();
    bool isInRedZone(const Vector2D& position);
    Vector2D getRandomPosition();
};

#endif // GAME_H
