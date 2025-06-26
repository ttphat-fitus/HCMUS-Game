#include "../include/Utils.h"
#include "../include/Player.h"
#include <random>
#include <chrono>

// Utility functions implementation
namespace Utils {
    double clamp(double value, double min, double max) {
        if (value < min) return min;
        if (value > max) return max;
        return value;
    }
    
    double lerp(double a, double b, double t) {
        return a + (b - a) * t;
    }
    
    double randomDouble(double min, double max) {
        static std::mt19937 rng(std::chrono::steady_clock::now().time_since_epoch().count());
        std::uniform_real_distribution<double> dist(min, max);
        return dist(rng);
    }
    
    int randomInt(int min, int max) {
        static std::mt19937 rng(std::chrono::steady_clock::now().time_since_epoch().count());
        std::uniform_int_distribution<int> dist(min, max);
        return dist(rng);
    }
    
    Vector2D randomPosition(double minX, double maxX, double minY, double maxY) {
        return Vector2D(randomDouble(minX, maxX), randomDouble(minY, maxY));
    }
    
    bool isPointInCircle(const Vector2D& point, const Vector2D& center, double radius) {
        return point.distanceTo(center) <= radius;
    }
    
    bool isPointInRectangle(const Vector2D& point, const Vector2D& topLeft, const Vector2D& bottomRight) {
        return point.x >= topLeft.x && point.x <= bottomRight.x &&
               point.y >= topLeft.y && point.y <= bottomRight.y;
    }
}

// Item class implementations
void Item::use(Player* player) {
    if (player && isActive) {
        // Base implementation - can be overridden by derived classes
        isActive = false;
    }
}

// Weapon class implementations
void Weapon::use(Player* player) {
    if (player && isActive) {
        // Give weapon to player
        isActive = false;
    }
}

bool Weapon::canFire() const {
    return currentAmmo > 0;
}

void Weapon::fire() {
    if (canFire()) {
        currentAmmo--;
    }
}

void Weapon::reload() {
    currentAmmo = maxAmmo;
}

// HealthItem class implementations
void HealthItem::use(Player* player) {
    if (player && isActive) {
        player->heal(value);
        isActive = false;
    }
}

// AmmoItem class implementations
void AmmoItem::use(Player* player) {
    if (player && isActive) {
        // Add ammo to player's current weapon
        Weapon* currentWeapon = player->getCurrentWeapon();
        if (currentWeapon) {
            currentWeapon->reload();
        }
        isActive = false;
    }
}
