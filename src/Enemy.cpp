#include "../include/Enemy.h"
#include "../include/Player.h"
#include "../include/Utils.h"
#include <algorithm>
#include <iostream>

Enemy::Enemy(int id, EnemyType type, const std::string& name, const Vector2D& position)
    : id(id), type(type), name(name), position(position), velocity(0, 0), direction(1, 0),
      targetPosition(position), health(100), maxHealth(100), armor(0), maxArmor(50), isAlive(true),
      currentState(EnemyState::IDLE), detectionRange(150), attackRange(50), patrolRadius(100),
      spawnPosition(position), damage(20), attackSpeed(1.0), speed(100), rotationSpeed(3.0),
      wanderTimer(0), wanderDuration(3.0), radius(12), color("#ff0000"), currentTarget(nullptr),
      stateTimer(0), maxStateTime(5.0) {
    
    lastAttackTime = std::chrono::steady_clock::now();
    initializeStats();
    initializeAI();
}

Enemy::~Enemy() = default;

void Enemy::update(double deltaTime, const std::vector<Player*>& players) {
    if (!isAlive) return;
    
    updateAI(deltaTime, players);
    updateMovement(deltaTime);
    updateCombat(deltaTime);
}

void Enemy::takeDamage(double damage) {
    if (!isAlive) return;
    
    double remainingDamage = damage;
    
    // Armor absorbs damage first
    if (armor > 0) {
        if (armor >= remainingDamage) {
            armor -= remainingDamage;
            remainingDamage = 0;
        } else {
            remainingDamage -= armor;
            armor = 0;
        }
    }
    
    // Remaining damage goes to health
    if (remainingDamage > 0) {
        health -= remainingDamage;
        if (health <= 0) {
            health = 0;
            die();
        }
    }
}

void Enemy::die() {
    isAlive = false;
    currentState = EnemyState::DEAD;
    std::cout << "Enemy " << name << " has died!" << std::endl;
}

void Enemy::updateAI(double deltaTime, const std::vector<Player*>& players) {
    findTarget(players);
    updateState(deltaTime);
    
    switch (currentState) {
        case EnemyState::IDLE:
            idle(deltaTime);
            break;
        case EnemyState::PATROL:
            patrol(deltaTime);
            break;
        case EnemyState::CHASE:
            chase(deltaTime);
            break;
        case EnemyState::ATTACK:
            attack(deltaTime);
            break;
        case EnemyState::DEAD:
            // Do nothing when dead
            break;
    }
}

void Enemy::findTarget(const std::vector<Player*>& players) {
    Player* closestTarget = nullptr;
    double closestDistance = detectionRange;
    
    for (Player* player : players) {
        if (!player->getIsAlive()) continue;
        
        double distance = position.distanceTo(player->getPosition());
        if (distance < closestDistance) {
            closestTarget = player;
            closestDistance = distance;
        }
    }
    
    currentTarget = closestTarget;
}

void Enemy::updateState(double deltaTime) {
    stateTimer += deltaTime;
    
    if (currentTarget) {
        double distanceToTarget = position.distanceTo(currentTarget->getPosition());
        
        if (distanceToTarget <= attackRange) {
            setState(EnemyState::ATTACK);
        } else if (distanceToTarget <= detectionRange) {
            setState(EnemyState::CHASE);
        } else {
            setState(EnemyState::PATROL);
        }
    } else {
        if (shouldChangeState()) {
            setState(EnemyState::PATROL);
        }
    }
}

void Enemy::patrol(double deltaTime) {
    wanderTimer += deltaTime;
    
    if (wanderTimer >= wanderDuration) {
        moveToRandomPosition();
        wanderTimer = 0;
        wanderDuration = Utils::randomDouble(2.0, 5.0);
    }
    
    if (targetPosition.distanceTo(position) > 5) {
        moveTowards(targetPosition);
    }
}

void Enemy::chase(double deltaTime) {
    if (!currentTarget) return;
    
    moveTowards(currentTarget->getPosition());
    rotateTowards(currentTarget->getPosition());
}

void Enemy::attack(double deltaTime) {
    if (!currentTarget) return;
    
    rotateTowards(currentTarget->getPosition());
    
    if (canAttack()) {
        performAttack();
    }
}

void Enemy::idle(double deltaTime) {
    // Stay still for a moment
    velocity = Vector2D(0, 0);
}

void Enemy::moveTowards(const Vector2D& target) {
    Vector2D direction = (target - position).normalized();
    velocity = direction * speed;
    this->direction = direction;
}

void Enemy::moveToRandomPosition() {
    Vector2D randomPos = getRandomPatrolPosition();
    targetPosition = randomPos;
}

void Enemy::rotateTowards(const Vector2D& target) {
    Vector2D targetDirection = (target - position).normalized();
    direction = targetDirection;
}

bool Enemy::canAttack() const {
    if (!currentTarget) return false;
    
    auto now = std::chrono::steady_clock::now();
    auto timeSinceLastAttack = std::chrono::duration<double>(now - lastAttackTime).count();
    
    return timeSinceLastAttack >= (1.0 / attackSpeed);
}

void Enemy::performAttack() {
    if (!currentTarget) return;
    
    currentTarget->takeDamage(damage);
    lastAttackTime = std::chrono::steady_clock::now();
    
    std::cout << "Enemy " << name << " attacked " << currentTarget->getName() << " for " << damage << " damage!" << std::endl;
}

bool Enemy::isInAttackRange(const Vector2D& target) const {
    return position.distanceTo(target) <= attackRange;
}

bool Enemy::isInDetectionRange(const Vector2D& target) const {
    return position.distanceTo(target) <= detectionRange;
}

bool Enemy::isCollidingWith(const Enemy& other) const {
    double distance = position.distanceTo(other.position);
    return distance < (radius + other.radius);
}

bool Enemy::isCollidingWith(const Vector2D& point, double pointRadius) const {
    double distance = position.distanceTo(point);
    return distance < (radius + pointRadius);
}

double Enemy::getDistanceTo(const Vector2D& target) const {
    return position.distanceTo(target);
}

bool Enemy::hasLineOfSight(const Vector2D& target, const std::vector<Player*>& players) const {
    Vector2D direction = (target - position).normalized();
    double distance = position.distanceTo(target);
    
    // Check if any player blocks the line of sight
    for (const Player* player : players) {
        if (!player->getIsAlive()) continue;
        
        Vector2D toPlayer = player->getPosition() - position;
        double playerDistance = toPlayer.magnitude();
        
        if (playerDistance < distance) {
            double dotProduct = direction.dot(toPlayer.normalized());
            if (dotProduct > 0.9) { // Close to the line
                return false;
            }
        }
    }
    
    return true;
}

void Enemy::updateMovement(double deltaTime) {
    position = position + velocity * deltaTime;
}

void Enemy::updateCombat(double deltaTime) {
    // Combat logic updates
}

Vector2D Enemy::getRandomPatrolPosition() {
    double angle = Utils::randomDouble(0, 2 * M_PI);
    double distance = Utils::randomDouble(20, patrolRadius);
    
    Vector2D offset(cos(angle) * distance, sin(angle) * distance);
    return spawnPosition + offset;
}

bool Enemy::shouldChangeState() const {
    return stateTimer >= maxStateTime;
}

void Enemy::resetStateTimer() {
    stateTimer = 0;
}

void Enemy::initializeStats() {
    switch (type) {
        case EnemyType::ZOMBIE:
            health = 80;
            maxHealth = 80;
            speed = 80;
            damage = 15;
            attackSpeed = 0.8;
            detectionRange = 120;
            attackRange = 40;
            color = "#8B4513";
            break;
        case EnemyType::BANDIT:
            health = 100;
            maxHealth = 100;
            speed = 120;
            damage = 25;
            attackSpeed = 1.2;
            detectionRange = 180;
            attackRange = 60;
            color = "#FF4500";
            break;
        case EnemyType::BOSS:
            health = 200;
            maxHealth = 200;
            speed = 100;
            damage = 40;
            attackSpeed = 0.6;
            detectionRange = 250;
            attackRange = 80;
            color = "#8B0000";
            radius = 20;
            break;
    }
}

void Enemy::initializeAI() {
    switch (type) {
        case EnemyType::ZOMBIE:
            patrolRadius = 80;
            wanderDuration = 4.0;
            break;
        case EnemyType::BANDIT:
            patrolRadius = 120;
            wanderDuration = 3.0;
            break;
        case EnemyType::BOSS:
            patrolRadius = 150;
            wanderDuration = 2.0;
            break;
    }
}
