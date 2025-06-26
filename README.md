# HCMUS Battle Royale Game

Một game battle royale 2D hoàn chỉnh được xây dựng với các nguyên tắc OOP, lấy cảm hứng từ [survev.io](https://survev.io/).

## 🎮 Tính năng Game

### Core Gameplay
- **Battle Royale**: 50 người chơi chiến đấu để trở thành người cuối cùng sống sót
- **Red Zone**: Vùng đỏ thu hẹp dần gây sát thương cho người chơi ở ngoài
- **Loot System**: Thu thập vũ khí, đạn, vật phẩm hồi máu và giáp
- **AI Enemies**: Zombie, Bandit và Boss với AI thông minh
- **Obstacles**: Cây, đá, tòa nhà tạo môi trường chiến đấu

### Hệ thống Combat
- **Health & Armor**: Hệ thống máu và giáp
- **Weapon System**: Nhiều loại vũ khí với damage và fire rate khác nhau
- **Inventory**: Hệ thống túi đồ với giới hạn slot
- **Collision Detection**: Phát hiện va chạm chính xác

### OOP Architecture
- **Encapsulation**: Mỗi class có private data và public methods
- **Inheritance**: Player, Enemy, Item kế thừa từ GameObject
- **Polymorphism**: Virtual methods cho update() và render()
- **Abstraction**: GameEngine quản lý toàn bộ game logic

## 🏗️ Cấu trúc Project

```
HCMUS-Game/
├── include/           # Header files (C++)
│   ├── Game.h        # Main game class
│   ├── Player.h      # Player class
│   ├── Enemy.h       # Enemy AI class
│   ├── Obstacle.h    # Obstacle class
│   └── Utils.h       # Utility classes
├── src/              # Source files (C++)
│   ├── Game.cpp
│   ├── Player.cpp
│   ├── Enemy.cpp
│   ├── Obstacle.cpp
│   └── Utils.cpp
├── web/              # Web version
│   └── game.js       # JavaScript game engine
├── main.cpp          # C++ main function
├── index.html        # Web interface
├── style.css         # Web styling
├── CMakeLists.txt    # Build configuration
└── README.md         # This file
```

## 🚀 Cách Chạy Game

### Phiên bản Web (Khuyến nghị)
1. Mở file `index.html` trong trình duyệt web
2. Nhấn "Join Game" để tạo nhân vật
3. Nhấn "Start Game" để bắt đầu chơi

### Phiên bản C++
1. Cài đặt CMake và compiler (g++, clang++)
2. Build project:
```bash
mkdir build
cd build
cmake ..
make
```
3. Chạy game:
```bash
./HCMUS-Game
```

## 🎯 Điều khiển

### Movement
- **WASD**: Di chuyển nhân vật
- **Mouse**: Ngắm
- **Left Click**: Bắn

### Actions
- **E**: Nhặt vật phẩm
- **R**: Nạp đạn
- **1-9**: Sử dụng vật phẩm trong túi

## 🎨 Classes và OOP Design

### Core Classes

#### GameObject (Base Class)
```cpp
class GameObject {
    protected:
        int id;
        Vector2D position;
        double radius;
        bool isActive;
    
    public:
        virtual void update(double deltaTime);
        virtual void render();
        bool isCollidingWith(GameObject* other);
};
```

#### Player (Inherits GameObject)
```cpp
class Player : public GameObject {
    private:
        std::string name;
        double health, armor;
        std::vector<Weapon*> weapons;
        std::vector<Item*> inventory;
    
    public:
        void move(Vector2D direction);
        void shoot();
        void takeDamage(double damage);
        bool pickUpItem(Item* item);
};
```

#### Enemy (Inherits GameObject)
```cpp
class Enemy : public GameObject {
    private:
        EnemyType type;
        EnemyState state;
        Player* currentTarget;
        double detectionRange, attackRange;
    
    public:
        void updateAI(double deltaTime, std::vector<Player*> players);
        void findTarget(std::vector<Player*> players);
        void attack();
};
```

### Design Patterns

#### Factory Pattern
- `ItemFactory`: Tạo các loại vật phẩm khác nhau
- `EnemyFactory`: Tạo các loại enemy với stats khác nhau

#### Observer Pattern
- `GameState`: Thông báo khi game state thay đổi
- `PlayerEvents`: Thông báo khi player chết, nhặt item

#### Strategy Pattern
- `AIBehavior`: Các strategy khác nhau cho enemy AI
- `WeaponStrategy`: Các loại vũ khí với behavior khác nhau

## 🎮 Game Mechanics

### Red Zone System
- Vùng đỏ thu hẹp dần theo thời gian
- Gây sát thương cho người chơi ở ngoài
- Tốc độ thu hẹp và damage tăng dần

### Loot System
- **Health Items**: Hồi máu
- **Armor Items**: Tăng giáp
- **Weapons**: Vũ khí với damage và fire rate khác nhau
- **Ammo**: Đạn cho vũ khí

### AI System
- **Zombie**: Chậm, ít máu, damage thấp
- **Bandit**: Cân bằng, AI thông minh hơn
- **Boss**: Mạnh, nhiều máu, AI phức tạp

## 🔧 Technical Features

### Performance
- **60 FPS**: Game loop tối ưu
- **Efficient Collision**: Spatial partitioning cho collision detection
- **Memory Management**: Smart pointers, RAII

### Cross-platform
- **C++**: Desktop version
- **Web**: JavaScript version
- **Responsive**: Hỗ trợ nhiều kích thước màn hình

### Extensibility
- **Modular Design**: Dễ thêm tính năng mới
- **Plugin System**: Có thể mở rộng với plugins
- **Configuration**: File config cho game settings

## 🎯 Future Enhancements

### Planned Features
- [ ] Multiplayer support
- [ ] More weapon types
- [ ] Vehicle system
- [ ] Weather effects
- [ ] Sound effects
- [ ] Particle effects
- [ ] Leaderboard system
- [ ] Custom maps

### Technical Improvements
- [ ] WebGL rendering
- [ ] Physics engine
- [ ] Networking optimization
- [ ] Mobile support
- [ ] VR support

## 📝 License

Project này được tạo cho mục đích học tập tại HCMUS. Dựa trên gameplay của [survev.io](https://survev.io/).

## 👥 Contributors

- **HCMUS Students**: OOP Project Team
- **Inspired by**: [survev.io](https://survev.io/)

---

**Chúc bạn chơi game vui vẻ! 🎮**
