# Higher Dimensional Sudoku
Navigate, solve, and assist in setting sudokus that escape "Flatland"

Inspired by [Cracking the Cryptic](https://www.youtube.com/channel/UCC-UOdK8-mIjxBQm_ot1T-Q), and hope/plan to present to them to solve a puzzle or two

## Roadmap
Note: I'm privileged to have a job during this pndemic, so my time is limited. Therefore, progress will be slow, so please bear with me.

 - Proof of concept with 4x4x4
 - Manually code solving algorithm from [Sudoku Wiki](https://www.sudokuwiki.org/sudoku.htm)
   - Copyrighted and limited to 9x9
   - Python
   - Also use for setting assist
 - Continue to try larger 3-dimensional puzzles
   - Eg. 6x6x6, 8x8x8, 9x9x9
 - Approximate minimum number of givens for a solution count of 1
   - Add a single given at a time
   - Once solution count gets close to 1, try adding different givens (try one, undo, try different one, undo, etc) 
   - (essentially trial and error)
 - Is 4D (9x9x9x9) even possible?
 - Web interface for manual solving
   - This is what I hope and plan to present to Simon and Mark
   - Preferably similar to their web app
   - With pause button that stops the clock and hides the puzzle; for when you get interrupted
   - Only view a single 2D puzzle at once (eg, 9x9)
   - Additional controls for navigating the other dimensions
     - Translate
     - Rotate (like [Miegakure](https://miegakure.com), specifically [this clip](https://youtu.be/9yW--eQaA2I?t=43))
   - Coordinates of currently viewing plane should be shown somewhere on screen
     - Maybe add an option to enable/disable
   - Add option for coordinate system
     - Letter/Number
     - rYcX
 - Allow others to implement variants; specifically for, but not limited to setting assist eg:
   - Chess
   - Thermo
   - Sandwich
   - Non-consecutive
   - (to name a few)

## Concept
Imagine 9 (valid, solved) standard sudokus stacked on top of each other. Every plane should itself be a valid, solved 9x9 sudoku.

Not these (from Google searches):

 - [3D Looking paper puzzles on Innoludic](http://www.innoludic.com/sudoku-rule/2015-02-08-20-11-14/3d-simple/13-rule-of-sudoku-3d)
 - ["4D Sudoku Hand-Held Game" on Pinterest](https://www.pinterest.de/pin/175218241722913074/)

More like these (also from Google searches):

 - ["3D Sudoku game for iOS" on Reddit](https://www.reddit.com/r/sudoku/comments/e5qv6n/i_spent_the_last_10_months_developing_a_3d_sudoku/) "true 3D Sudoku experience"
 - [Q & A on Puzzling Stack Exchange](https://puzzling.stackexchange.com/questions/85217/is-this-3d-sudoku-possible) (this, but not just 3D, but any n-D where n > 2)
