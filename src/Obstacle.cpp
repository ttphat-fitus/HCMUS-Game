#include "../include/Obstacle.h"
#include "../include/Utils.h"
#include <iostream>

Obstacle::Obstacle(int id, ObstacleType type, const std::string& name, const Vector2D& position)
    : id(id), type(type), name(name), position(position), size(50, 50), radius(25),
      isDestructible(false), health(100), maxHealth(100), color("#8B4513") {
    
    initializeStats();
    initializeVisual();
}

Obstacle::~Obstacle() = default;

void Obstacle::update(double deltaTime) {
    // Obstacles are mostly static, but can have animations or effects
    if (health <= 0 && isDestructible) {
        destroy();
    }
}

void Obstacle::takeDamage(double damage) {
    if (!isDestructible) return;
    
    health -= damage;
    if (health <= 0) {
        health = 0;
        destroy();
    }
}

void Obstacle::destroy() {
    health = 0;
    std::cout << "Obstacle " << name << " has been destroyed!" << std::endl;
}

bool Obstacle::isCollidingWith(const Vector2D& point, double pointRadius) const {
    double distance = position.distanceTo(point);
    return distance < (radius + pointRadius);
}

bool Obstacle::isCollidingWith(const Vector2D& rectPos, const Vector2D& rectSize) const {
    // Check if circle (obstacle) intersects with rectangle
    Vector2D closestPoint;
    
    // Find the closest point on the rectangle to the circle center
    closestPoint.x = Utils::clamp(position.x, rectPos.x, rectPos.x + rectSize.x);
    closestPoint.y = Utils::clamp(position.y, rectPos.y, rectPos.y + rectSize.y);
    
    // Check if the closest point is inside the circle
    return position.distanceTo(closestPoint) <= radius;
}

bool Obstacle::isCollidingWith(const Obstacle& other) const {
    double distance = position.distanceTo(other.position);
    return distance < (radius + other.radius);
}

void Obstacle::initializeStats() {
    switch (type) {
        case ObstacleType::TREE:
            size = Vector2D(40, 60);
            radius = 20;
            isDestructible = false;
            health = 200;
            maxHealth = 200;
            break;
        case ObstacleType::ROCK:
            size = Vector2D(30, 30);
            radius = 15;
            isDestructible = true;
            health = 150;
            maxHealth = 150;
            break;
        case ObstacleType::BUILDING:
            size = Vector2D(100, 80);
            radius = 50;
            isDestructible = false;
            health = 500;
            maxHealth = 500;
            break;
        case ObstacleType::WALL:
            size = Vector2D(20, 60);
            radius = 10;
            isDestructible = true;
            health = 100;
            maxHealth = 100;
            break;
        case ObstacleType::BARRIER:
            size = Vector2D(50, 10);
            radius = 25;
            isDestructible = true;
            health = 80;
            maxHealth = 80;
            break;
    }
}

void Obstacle::initializeVisual() {
    switch (type) {
        case ObstacleType::TREE:
            color = "#228B22"; // Forest green
            break;
        case ObstacleType::ROCK:
            color = "#696969"; // Dim gray
            break;
        case ObstacleType::BUILDING:
            color = "#8B4513"; // Saddle brown
            break;
        case ObstacleType::WALL:
            color = "#A0522D"; // Sienna
            break;
        case ObstacleType::BARRIER:
            color = "#FFD700"; // Gold
            break;
    }
}
