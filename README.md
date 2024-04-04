# DownRL

This project is aimed to test several reinforcement learning algorithms in the modern arcade-style game 'Downwell'

Downwell as a game has several challenges that make it complex for both human players and algorithms alike;
they are listed below.

- Fast Paced : the game requires fast reactions, meaning any algorithms that interact with the game should process data
  quickly
- Randomized Layout : level layouts are variable, and in general the environment for two playthroughs may not be the
  same.
- Uniform color palate. The game uses a minimal number of distinct colors. This can be seen as either an advantage or
  disadvantage.
    - For the player it minimizes cognitive load; less color expression makes it easier for players to be quick in
      processing landscapes to decide best actions to make.
    - For many computer vision algorithms this adds a layer of complexity in object recognition. It may make it easier
      to know an objects relevance (objects that are relevant are either white or red). But it may lead to challenges in
      detecting different important objects (distinguishing white colored enemies from the white colored player).
        - To handle scenarios like this there may be additional preprocessing for some algorithms such as template
          matching to determine player and enemy locations