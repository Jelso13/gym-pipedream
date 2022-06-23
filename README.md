# gym-pipedream *readme in progress

An [OpenAI Gym](https://github.com/openai/gym) environment inspired by the Windows 95 game, [Pipe Dream](https://en.wikipedia.org/wiki/Pipe_Mania). 

![til](./images/pipedream.GIF)

### **Requirements**
- Python 3
- OpenAI Gym
- ...

## Installation

## Design
---
The environment is split into two sections
1. Main Board
2. Pipe Queue

## State Space

---
## Action Space
- Actions are taken by placing the pipe at the end of the queue on the board in a valid position.
- Actions are given by a tuple: (x, y)
  - 0 $\le$ x $\le$ board_width
  - 0 $\le$ y $\le$ board_height

---
## Reward
- +1 every step taken
- -10 on water leaking (env done)

## Wrappers

# Included Environments

