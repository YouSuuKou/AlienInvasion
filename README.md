# Alien Invasion

Alien Invasion 是一个基于 Python 和 Pygame 的经典射击游戏项目。改编自 Eric Matthes 的《Python Crash Course》一书中的示例代码，旨在帮助初学者学习游戏开发的基础知识，包括图形渲染、事件处理、碰撞检测和游戏逻辑设计。

## 游戏简介
你将驾驶飞船消灭不断下落的外星人，获得积分并挑战更高的关卡。

## 主要特性
- 飞船移动与射击
- 外星人编队与进攻
- 子弹自动索敌（追踪外星人）
- 计分板与关卡提升
- 游戏暂停与重新开始

## 安装与运行
1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
2. 运行游戏：
   ```bash
   python main.py
   ```

## 操作说明
- **A/D**：左右移动飞船
- **左Shift**：加速移动
- **鼠标左键**：发射子弹
- **ESC**：退出游戏

## 改进原版功能
- 添加了子弹自动索敌功能，使游戏更具挑战性。
- 根据密度生成的外星人编队，循序渐进。

## 代码结构
- `main.py`：游戏主循环与事件处理
- `settings.py`：游戏设置
- `ship.py`：飞船逻辑
- `alien.py`：外星人逻辑
- `bullet.py`：子弹与索敌逻辑
- `game_stats.py`：分数与状态
- `scoreboard.py`：计分板显示
- `button.py`：按钮控件

## 贡献
欢迎提交 issue 和 pull request 改进本项目。

## License
MIT
This is a simple 2D game called "Alien Invasion" where the player controls a spaceship and must defend against waves of invading aliens. The game is built using Python and the Pygame library.
## Features
- Player-controlled spaceship
- Multiple waves of invading aliens
- score tracking
- bullet firing mechanics
- physics-based movement
- mathematical calculations for collision detection and movement