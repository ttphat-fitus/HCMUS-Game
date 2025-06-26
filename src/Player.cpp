#include "../include/Player.h"
#include "../include/Utils.h"
#include <algorithm>
#include <iostream>

Player::Player(int id, const std::string& name, const Vector2D& position)
    : id(id), name(name), position(position), velocity(0, 0), direction(1, 0),
      health(100), maxHealth(100), armor(0), maxArmor(100), isAlive(true), isMoving(false),
      kills(0), deaths(0), speed(200), rotationSpeed(5.0), isShooting(false),
      radius(15), color("#00ff00"), maxInventorySize(10) {
    
    lastShotTime = std::chrono::steady_clock::now();
    initializeDefaultWeapon();
}

Player::~Player() = default;

void Player::update(double deltaTime) {
    if (!isAlive) return;
    
    updateMovement(deltaTime);
    updateCombat(deltaTime);
    updateAnimation(deltaTime);
}

void Player::move(const Vector2D& direction) {
    if (!isAlive) return;
    
    this->direction = direction.normalized();
    velocity = this->direction * speed;
    isMoving = true;
}

void Player::rotate(const Vector2D& target) {
    if (!isAlive) return;
    
    Vector2D targetDirection = (target - position).normalized();
    direction = targetDirection;
}

void Player::shoot() {
    if (!isAlive || !currentWeapon || !canShoot()) return;
    
    currentWeapon->fire();
    lastShotTime = std::chrono::steady_clock::now();
    isShooting = true;
}

void Player::takeDamage(double damage) {
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
            handleDeath();
        }
    }
}

void Player::heal(double amount) {
    if (!isAlive) return;
    health = Utils::clamp(health + amount, 0, maxHealth);
}

void Player::addArmor(double amount) {
    if (!isAlive) return;
    armor = Utils::clamp(armor + amount, 0, maxArmor);
}

bool Player::pickUpItem(std::unique_ptr<Item> item) {
    if (!isAlive || inventory.size() >= maxInventorySize) return false;
    
    inventory.push_back(std::move(item));
    return true;
}

void Player::dropItem(int itemIndex) {
    if (itemIndex >= 0 && itemIndex < static_cast<int>(inventory.size())) {
        inventory.erase(inventory.begin() + itemIndex);
    }
}

void Player::useItem(int itemIndex) {
    if (itemIndex >= 0 && itemIndex < static_cast<int>(inventory.size()) && isAlive) {
        inventory[itemIndex]->use(this);
        if (!inventory[itemIndex]->isActive) {
            dropItem(itemIndex);
        }
    }
}

void Player::switchWeapon(int weaponIndex) {
    if (weaponIndex >= 0 && weaponIndex < static_cast<int>(weapons.size()) && isAlive) {
        currentWeapon = std::move(weapons[weaponIndex]);
        weapons.erase(weapons.begin() + weaponIndex);
    }
}

bool Player::canShoot() const {
    if (!currentWeapon || !isAlive) return false;
    
    auto now = std::chrono::steady_clock::now();
    auto timeSinceLastShot = std::chrono::duration<double>(now - lastShotTime).count();
    
    return currentWeapon->canFire() && timeSinceLastShot >= (1.0 / currentWeapon->fireRate);
}

double Player::getDamage() const {
    return currentWeapon ? currentWeapon->damage : 0;
}

Vector2D Player::getShootDirection() const {
    return direction;
}

bool Player::isInRange(const Vector2D& target, double range) const {
    return position.distanceTo(target) <= range;
}

void Player::respawn(const Vector2D& newPosition) {
    position = newPosition;
    velocity = Vector2D(0, 0);
    health = maxHealth;
    armor = 0;
    isAlive = true;
    isMoving = false;
    isShooting = false;
    
    // Reset weapons
    if (currentWeapon) {
        currentWeapon->reload();
    }
}

bool Player::isCollidingWith(const Player& other) const {
    double distance = position.distanceTo(other.position);
    return distance < (radius + other.radius);
}

bool Player::isCollidingWith(const Vector2D& point, double pointRadius) const {
    double distance = position.distanceTo(point);
    return distance < (radius + pointRadius);
}

void Player::updateMovement(double deltaTime) {
    if (isMoving) {
        position = position + velocity * deltaTime;
        isMoving = false;
    }
}

void Player::updateCombat(double deltaTime) {
    // Reset shooting state
    if (isShooting) {
        isShooting = false;
    }
}

void Player::updateAnimation(double deltaTime) {
    // Animation logic can be added here
}

void Player::handleDeath() {
    isAlive = false;
    deaths++;
    std::cout << "Player " << name << " has died!" << std::endl;
}

void Player::initializeDefaultWeapon() {
    // Create a basic pistol as default weapon
    auto pistol = std::make_unique<Weapon>("Pistol", 25, 2.0, 200, 12);
    currentWeapon = std::move(pistol);
}
