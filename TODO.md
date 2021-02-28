## Todo

  > I'm privileged to have a full-time job during this pandemic. Progress will be slow as my time is limited. Please bear with me.

 - [ ] The basics
   <details>
   <summary>Click to expand!</summary>

   - [ ] Data
      - [x] Storage
      - [x] Manipulation
      - [ ] Regions
   - [ ] User interface
      - [ ] Grid
         - [ ] Boundaries
            - [x] Outer-most
            - [x] Between cells
            - [ ] Between boxes (aka regions)
      - [ ] Modes
         - [ ] Digit
         - [ ] Corner
         - [ ] Center
         - [ ] Color
      - [ ] Navigation
         - [ ] Enter coordinates
         - [ ] Rotate around
            - [ ] Row
            - [ ] Column
   </details>
 - [ ] Proof of concept with 4x4x4
      - [ ] Store data in JSON file
         - [ ] Save
         - [ ] Load
 - [ ] Manually code solving algorithm from [Sudoku Wiki](https://www.sudokuwiki.org/sudoku.htm)
   - Copyrighted and limited to 9x9
   - Python
   - Also use for setting assist
   - [ ] Strategies (copied from the wiki):
      <details>
      <summary>Click to expand!</summary>
     
      - [ ] 1: Hidden Singles
      - [ ] 2: Naked Pairs/Triples
      - [ ] 3: Hidden Pairs/Triples
      - [ ] 4: Naked/Hidden Quads
      - [ ] 5: Pointing Pairs
      - [ ] 6: Box/Line Reduction
      - [ ] 7: X-Wing
      - [ ] 8: Simple Colouring
      - [ ] 9: Y-Wing
      - [ ] 10: Swordfish
      - [ ] 11: XYZ Wing
      - [ ] 12: X-Cycles
      - [ ] 13: BUG
      - [ ] 14: XY-Chain
      - [ ] 15: 3D Medusa
      - [ ] 16: Jellyfish
      - [ ] 17: Unique Rectangles
      - [ ] 18: SK Loops
      - [ ] 19: Extended Unique Rect.
      - [ ] 20: Hidden Unique Rect's
      - [ ] 21: WXYZ Wing
      - [ ] 22: Aligned Pair Exclusion
      - [ ] 23: Exocet
      - [ ] 24: Grouped X-Cycles
      - [ ] 25: Empty Rectangles
      - [ ] 26: Finned X-Wing
      - [ ] 27: Finned Swordfish
      - [ ] 28: Altern. Inference Chains
      - [ ] 29: Sue-de-Cog
      - [ ] 30: Digit Forcing Chains
      - [ ] 31: Nishio Forcing Chains
      - [ ] 32: Cell Forcing Chains
      - [ ] 33: Unit Forcing Chains
      - [ ] 34: Almost Locked Sets
      - [ ] 35: Death Blossom
      - [ ] 36: Pattern Overlay Method
      - [ ] 37: Quad Forcing Chains
      - [ ] 38: Bowman's Bingo
     </details>
 - [ ] Continue to try larger 3-dimensional puzzles
   - Eg. 6x6x6, 8x8x8, 9x9x9
 - [ ] Approximate minimum number of givens for a solution count of 1
   - Add a single given at a time
   - Once solution count gets close to 1, try adding different givens (try one, undo, try different one, undo, etc) 
   - (essentially trial and error)
   - Is this even a good idea? necessary? feasible (for larger grids)?
 - [ ] Is 4D (9x9x9x9) even possible? (Yes/No)
   - By "possible" I mean "does a valid, solved grid exist"
 - [ ] Web interface for manual solving
   <details>
   <summary>Click to expand!</summary>

   - This is what I hope and plan to present to Simon and Mark
   - Preferably similar to their web app
   - [ ] With pause button that stops the clock and hides the puzzle; for when you get interrupted
   - [ ] Only view a single 2D puzzle at once (eg, 9x9)
   - [ ] Additional controls for navigating the other dimensions
     - [ ] Coordinates
     - [ ] Translate
     - [ ] Rotate (like [Miegakure](https://miegakure.com), specifically [this clip](https://youtu.be/9yW--eQaA2I?t=43))
   - [ ] Coordinates of currently viewing plane should be shown somewhere on screen
     - Maybe add an option to enable/disable
   - [ ] Add option for coordinate system
     - [ ] Letter/Number
     - [ ] rYcX
   </details>
 - [ ] Allow others to implement variants; specifically for, but not limited to setting assist
   <details>
   <summary>Click to expand examples</summary>

   - Chess
   - Killer
   - Non-consecutive
   - Sandwich
   - Thermo
   </details>
 - [ ] Support other pencil puzzles
   <details>
   <summary>Click to expand examples</summary>

   - Akari
   - Fillomino
   - LITS
   - Pentominous
   - Siltherlink
   - Yajilin
   </details>
