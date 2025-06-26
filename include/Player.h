#ifndef PLAYER_H
#define PLAYER_H

#include "Utils.h"
#include <string>
#include <vector>
#include <memory>
#include <chrono>

// Forward declarations
class Weapon;
class Item;

class Player {
private:
    // Basic properties
    int id;
    std::string name;
    Vector2D position;
    Vector2D velocity;
    Vector2D direction;
    
    // Health and status
    double health;
    double maxHealth;
    double armor;
    double maxArmor;
    bool isAlive;
    bool isMoving;
    
    // Combat
    std::unique_ptr<Weapon> currentWeapon;
    std::vector<std::unique_ptr<Weapon>> weapons;
    int kills;
    int deaths;
    
    // Movement and controls
    double speed;
    double rotationSpeed;
    bool isShooting;
    std::chrono::steady_clock::time_point lastShotTime;
    
    // Visual properties
    double radius;
    std::string color;
    
    // Inventory
    std::vector<std::unique_ptr<Item>> inventory;
    int maxInventorySize;
    
public:
    Player(int id, const std::string& name, const Vector2D& position);
    ~Player();
    
    // Core gameplay methods
    void update(double deltaTime);
    void move(const Vector2D& direction);
    void rotate(const Vector2D& target);
    void shoot();
    void takeDamage(double damage);
    void heal(double amount);
    void addArmor(double amount);
    
    // Inventory management
    bool pickUpItem(std::unique_ptr<Item> item);
    void dropItem(int itemIndex);
    void useItem(int itemIndex);
    void switchWeapon(int weaponIndex);
    
    // Combat methods
    bool canShoot() const;
    double getDamage() const;
    Vector2D getShootDirection() const;
    bool isInRange(const Vector2D& target, double range) const;
    
    // Getters
    int getId() const { return id; }
    const std::string& getName() const { return name; }
    const Vector2D& getPosition() const { return position; }
    const Vector2D& getVelocity() const { return velocity; }
    const Vector2D& getDirection() const { return direction; }
    double getHealth() const { return health; }
    double getMaxHealth() const { return maxHealth; }
    double getArmor() const { return armor; }
    double getMaxArmor() const { return maxArmor; }
    bool getIsAlive() const { return isAlive; }
    double getRadius() const { return radius; }
    const std::string& getColor() const { return color; }
    int getKills() const { return kills; }
    int getDeaths() const { return deaths; }
    Weapon* getCurrentWeapon() const { return currentWeapon.get(); }
    const std::vector<std::unique_ptr<Weapon>>& getWeapons() const { return weapons; }
    const std::vector<std::unique_ptr<Item>>& getInventory() const { return inventory; }
    
    // Setters
    void setPosition(const Vector2D& pos) { position = pos; }
    void setVelocity(const Vector2D& vel) { velocity = vel; }
    void setDirection(const Vector2D& dir) { direction = dir; }
    void setHealth(double h) { health = Utils::clamp(h, 0, maxHealth); }
    void setArmor(double a) { armor = Utils::clamp(a, 0, maxArmor); }
    void setIsAlive(bool alive) { isAlive = alive; }
    void setIsMoving(bool moving) { isMoving = moving; }
    void setIsShooting(bool shooting) { isShooting = shooting; }
    void setColor(const std::string& c) { color = c; }
    
    // Utility methods
    void addKill() { kills++; }
    void addDeath() { deaths++; }
    void respawn(const Vector2D& newPosition);
    bool isCollidingWith(const Player& other) const;
    bool isCollidingWith(const Vector2D& point, double radius) const;
    
private:
    void updateMovement(double deltaTime);
    void updateCombat(double deltaTime);
    void updateAnimation(double deltaTime);
    void handleDeath();
    void initializeDefaultWeapon();
};

#endif // PLAYER_H
