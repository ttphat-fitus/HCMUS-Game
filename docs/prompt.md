# Game Rewrite in Python

## Task
You're a senior software engineer and a game developer who has a lot of experience in **Python** and the **Godot** library. You're now helping a student learning Object-oriented Programming to rewrite an old game - written in Godot - to Python. 

## Resources
You are provided two folders: `HCMUS-Game` and `Game-Python`:
- The `HCMUS-Game` directory contains the **ORIGINAL** game, written in **Godot**.
- The `Game-Python` directory SHOULD BE the folder where you put the rewritten game, in **Python**.

## Core requirements
Given the above two directories, you NEED to CAREFULLY ANALYZE the source code of the Godot-based game project. Use your analytical skills to analyze EVERY objects, scenes, elements, etc. in the original game, then **RE-IMPLEMENT** each of this **EXACTLY THE SAME** using Python.

You need to develop the game that comply with the Object-oriented principles and design patterns:
- You must **HEAVILY LEVERAGE** core OOP concepts of Inheritance, Polymorphism, Abstraction, and Encapsulation. Make sure to justify your design decisions in relation to these principles.
- The project must thoughtfully implement **AT LEAST** three software development design patterns. Use the most appropriate design pattern for solving the problem in the game design. You SHOULD explain why the chosen pattern is a suitable solution for the problem at hand. If possible, output a **comparison table** with the following columns: `Index`, `Design Pattern`, `Why would we use or not use it`, `How it could / could not help with the project`, `Final decision of use / not use it`.
- During the implementation of these, if you encounter any case of unapplicable design patterns / OOP concepts (I mean these can't be used in the rewritten project), note those into `UNAPPLICABLE.md` file. Then explain your decision in a comprehensive manner.

## Preferred library
- You might want to use `pygame` as the rendering engine for the rewritten Python game.
- Before using any library, make sure you search the internet first for the appropriate documentation according.
- Make sure that you guide the user to create and enter virtual environment, install any dependencies, and run the game, in DETAIL.

## Further needs
- Professionally use separated files or folders for each object, scene, or element. 
- For the resources (audio, music, or image files), you might want to copy over to the new project directory.
- Before starting, you should create a file called `PLAN.md`. This file contains what you are planning to do, using bulleted list. If you've just done creating this file **INITIALLY**, asks for approval from the user, so that they will manually analyze the plan carefully before giving you the permission to start rewriting the game. **Yes, REMEMBER, ask the user for permission before STARTING your work!!!!**

## Documentation
During our chat, make sure that you **LOG EVERYTHING**, including my messages and your responses, into a file called `AI_LOG.md`, using the following format:

```
----------
USER'S MESSAGE 1
- TIMESTAMP: ${CURRENT DATETIME}
- CONTENT: ${THE ENTIRE MESSAGE, PUT IN CODEBLOCK}
- SUMMARY OF MESSAGE: ${MESSAGE SUMMARY}

----------
COPILOT RESPONSE 1
- TIMESTAMP: ${CURRENT DATETIME}
- YOUR RESPONSE: ${YOUR ENTIRE RESPONSE, PUT IN CODEBLOCK}
- FILES CHANGED: ${Bulleted list of changed files directory}
- SUMMARY OF RESPONSE: ${RESPONSE SUMMARY}
- USER'S FEEDBACK: JUST LEAVE THIS FIELD BLANK

----------
```
... and continue for every single other messages/responses.
