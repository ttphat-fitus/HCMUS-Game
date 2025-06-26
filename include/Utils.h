#ifndef UTILS_H
#define UTILS_H

#include <string>
#include <cmath>
#include <random>

// Forward declaration
class Player;

// Vector2D class for 2D coordinates and calculations
class Vector2D {
public:
    double x, y;
    
    Vector2D() : x(0.0), y(0.0) {}
    Vector2D(double x, double y) : x(x), y(y) {}
    
    // Vector operations
    Vector2D operator+(const Vector2D& other) const {
        return Vector2D(x + other.x, y + other.y);
    }
    
    Vector2D operator-(const Vector2D& other) const {
        return Vector2D(x - other.x, y - other.y);
    }
    
    Vector2D operator*(double scalar) const {
        return Vector2D(x * scalar, y * scalar);
    }
    
    Vector2D operator/(double scalar) const {
        return Vector2D(x / scalar, y / scalar);
    }
    
    // Magnitude and normalization
    double magnitude() const {
        return std::sqrt(x * x + y * y);
    }
    
    Vector2D normalized() const {
        double mag = magnitude();
        if (mag > 0) {
            return Vector2D(x / mag, y / mag);
        }
        return Vector2D(0, 0);
    }
    
    // Distance between two points
    double distanceTo(const Vector2D& other) const {
        return (*this - other).magnitude();
    }
    
    // Dot product
    double dot(const Vector2D& other) const {
        return x * other.x + y * other.y;
    }
};

// Item types for loot system
enum class ItemType {
    WEAPON,
    AMMO,
    HEALTH,
    ARMOR,
    SCOPE
};

// Item class for loot
class Item {
public:
    ItemType type;
    std::string name;
    Vector2D position;
    double value;
    bool isActive;
    
    Item(ItemType type, const std::string& name, const Vector2D& pos, double value)
        : type(type), name(name), position(pos), value(value), isActive(true) {}
    
    virtual ~Item() = default;
    virtual void use(Player* player) = 0;
};

// Weapon class
class Weapon : public Item {
public:
    double damage;
    double fireRate;
    double range;
    int maxAmmo;
    int currentAmmo;
    
    Weapon(const std::string& name, double damage, double fireRate, double range, int maxAmmo)
        : Item(ItemType::WEAPON, name, Vector2D(0, 0), damage),
          damage(damage), fireRate(fireRate), range(range), maxAmmo(maxAmmo), currentAmmo(maxAmmo) {}
    
    void use(Player* player) override;
    bool canFire() const;
    void fire();
    void reload();
};

// Health item class
class HealthItem : public Item {
public:
    HealthItem(const std::string& name, double healAmount)
        : Item(ItemType::HEALTH, name, Vector2D(0, 0), healAmount) {}
    
    void use(Player* player) override;
};

// Ammo item class
class AmmoItem : public Item {
public:
    AmmoItem(const std::string& name, int ammoAmount)
        : Item(ItemType::AMMO, name, Vector2D(0, 0), ammoAmount) {}
    
    void use(Player* player) override;
};

// Utility functions
namespace Utils {
    double clamp(double value, double min, double max);
    double lerp(double a, double b, double t);
    double randomDouble(double min, double max);
    int randomInt(int min, int max);
    Vector2D randomPosition(double minX, double maxX, double minY, double maxY);
    bool isPointInCircle(const Vector2D& point, const Vector2D& center, double radius);
    bool isPointInRectangle(const Vector2D& point, const Vector2D& topLeft, const Vector2D& bottomRight);
}

#endif // UTILS_H
