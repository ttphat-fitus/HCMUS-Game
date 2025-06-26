#ifndef OBSTACLE_H
#define OBSTACLE_H

#include "Utils.h"
#include <string>

enum class ObstacleType {
    TREE,
    ROCK,
    BUILDING,
    WALL,
    BARRIER
};

class Obstacle {
private:
    int id;
    ObstacleType type;
    std::string name;
    Vector2D position;
    Vector2D size;
    double radius;
    bool isDestructible;
    double health;
    double maxHealth;
    std::string color;
    
public:
    Obstacle(int id, ObstacleType type, const std::string& name, const Vector2D& position);
    ~Obstacle();
    
    // Core methods
    void update(double deltaTime);
    void takeDamage(double damage);
    void destroy();
    
    // Collision detection
    bool isCollidingWith(const Vector2D& point, double pointRadius) const;
    bool isCollidingWith(const Vector2D& rectPos, const Vector2D& rectSize) const;
    bool isCollidingWith(const Obstacle& other) const;
    
    // Getters
    int getId() const { return id; }
    ObstacleType getType() const { return type; }
    const std::string& getName() const { return name; }
    const Vector2D& getPosition() const { return position; }
    const Vector2D& getSize() const { return size; }
    double getRadius() const { return radius; }
    bool getIsDestructible() const { return isDestructible; }
    double getHealth() const { return health; }
    double getMaxHealth() const { return maxHealth; }
    const std::string& getColor() const { return color; }
    bool isDestroyed() const { return health <= 0; }
    
    // Setters
    void setPosition(const Vector2D& pos) { position = pos; }
    void setSize(const Vector2D& s) { size = s; }
    void setRadius(double r) { radius = r; }
    void setHealth(double h) { health = Utils::clamp(h, 0, maxHealth); }
    void setColor(const std::string& c) { color = c; }
    
private:
    void initializeStats();
    void initializeVisual();
};

#endif // OBSTACLE_H
