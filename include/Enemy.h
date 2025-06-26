#ifndef ENEMY_H
#define ENEMY_H

#include "Utils.h"
#include <string>
#include <memory>
#include <chrono>

// Forward declarations
class Player;
class Weapon;

enum class EnemyType {
    ZOMBIE,
    BANDIT,
    BOSS
};

enum class EnemyState {
    IDLE,
    PATROL,
    CHASE,
    ATTACK,
    DEAD
};

class Enemy {
private:
    // Basic properties
    int id;
    EnemyType type;
    std::string name;
    Vector2D position;
    Vector2D velocity;
    Vector2D direction;
    Vector2D targetPosition;
    
    // Health and status
    double health;
    double maxHealth;
    double armor;
    double maxArmor;
    bool isAlive;
    
    // AI behavior
    EnemyState currentState;
    double detectionRange;
    double attackRange;
    double patrolRadius;
    Vector2D spawnPosition;
    
    // Combat
    std::unique_ptr<Weapon> weapon;
    double damage;
    double attackSpeed;
    std::chrono::steady_clock::time_point lastAttackTime;
    
    // Movement
    double speed;
    double rotationSpeed;
    double wanderTimer;
    double wanderDuration;
    
    // Visual properties
    double radius;
    std::string color;
    
    // AI variables
    Player* currentTarget;
    double stateTimer;
    double maxStateTime;
    
public:
    Enemy(int id, EnemyType type, const std::string& name, const Vector2D& position);
    ~Enemy();
    
    // Core gameplay methods
    void update(double deltaTime, const std::vector<Player*>& players);
    void takeDamage(double damage);
    void die();
    
    // AI methods
    void updateAI(double deltaTime, const std::vector<Player*>& players);
    void findTarget(const std::vector<Player*>& players);
    void updateState(double deltaTime);
    void patrol(double deltaTime);
    void chase(double deltaTime);
    void attack(double deltaTime);
    void idle(double deltaTime);
    
    // Movement methods
    void moveTowards(const Vector2D& target);
    void moveToRandomPosition();
    void rotateTowards(const Vector2D& target);
    
    // Combat methods
    bool canAttack() const;
    void performAttack();
    bool isInAttackRange(const Vector2D& target) const;
    bool isInDetectionRange(const Vector2D& target) const;
    
    // Getters
    int getId() const { return id; }
    EnemyType getType() const { return type; }
    const std::string& getName() const { return name; }
    const Vector2D& getPosition() const { return position; }
    const Vector2D& getVelocity() const { return velocity; }
    const Vector2D& getDirection() const { return direction; }
    double getHealth() const { return health; }
    double getMaxHealth() const { return maxHealth; }
    double getArmor() const { return armor; }
    bool getIsAlive() const { return isAlive; }
    EnemyState getState() const { return currentState; }
    double getRadius() const { return radius; }
    const std::string& getColor() const { return color; }
    Player* getCurrentTarget() const { return currentTarget; }
    double getDetectionRange() const { return detectionRange; }
    double getAttackRange() const { return attackRange; }
    
    // Setters
    void setPosition(const Vector2D& pos) { position = pos; }
    void setVelocity(const Vector2D& vel) { velocity = vel; }
    void setDirection(const Vector2D& dir) { direction = dir; }
    void setHealth(double h) { health = Utils::clamp(h, 0, maxHealth); }
    void setArmor(double a) { armor = Utils::clamp(a, 0, maxArmor); }
    void setState(EnemyState state) { currentState = state; stateTimer = 0; }
    void setCurrentTarget(Player* target) { currentTarget = target; }
    void setColor(const std::string& c) { color = c; }
    
    // Utility methods
    bool isCollidingWith(const Enemy& other) const;
    bool isCollidingWith(const Vector2D& point, double radius) const;
    double getDistanceTo(const Vector2D& target) const;
    bool hasLineOfSight(const Vector2D& target, const std::vector<Player*>& players) const;
    
private:
    void initializeStats();
    void initializeAI();
    void updateMovement(double deltaTime);
    void updateCombat(double deltaTime);
    Vector2D getRandomPatrolPosition();
    bool shouldChangeState() const;
    void resetStateTimer();
};

#endif // ENEMY_H
