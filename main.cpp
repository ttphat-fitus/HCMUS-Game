#include "include/Game.h"
#include <iostream>
#include <thread>
#include <chrono>

int main() {
    std::cout << "=== HCMUS Battle Royale Game ===" << std::endl;
    std::cout << "A 2D Battle Royale inspired by survev.io" << std::endl;
    std::cout << "Built with OOP principles" << std::endl;
    std::cout << "=================================" << std::endl;
    
    // Create game instance
    Game game(1600, 900, 50);
    game.initialize();
    
    // Add some test players
    game.addPlayer("Player1", 100, 100);
    game.addPlayer("Player2", 200, 200);
    game.addPlayer("Player3", 300, 300);
    
    std::cout << "Game started with " << game.getPlayerCount() << " players" << std::endl;
    
    // Simple game loop for testing
    const double targetFPS = 60.0;
    const double frameTime = 1.0 / targetFPS;
    
    while (game.getState() != Game::GameState::GAME_OVER) {
        auto start = std::chrono::steady_clock::now();
        
        game.update();
        game.render();
        
        // Frame rate limiting
        auto end = std::chrono::steady_clock::now();
        auto elapsed = std::chrono::duration<double>(end - start).count();
        
        if (elapsed < frameTime) {
            std::this_thread::sleep_for(std::chrono::duration<double>(frameTime - elapsed));
        }
    }
    
    std::cout << "Game finished!" << std::endl;
    return 0;
}
