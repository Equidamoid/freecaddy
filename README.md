## freecaddy: FreeCAD models as code

This project aims at providing utilities for those who wants to make 3d models with code and only code.

### But... why would someone want that?
Isn't it harder and doesn't it take longer than just use the GUI? Yup, it is and it does. Up until the point when 2 hours
later you realise, that in the very beginning that thingie should've gone to the left from this and not vice versa.

Tools like Fusion360 allow certain degree of going back and reapplying changes, but it doesn't always do enough magic.
F360 also requires a Windows VM. Nope.

Another side is that code is much easier to manage compared to whatever project files. Broke something that was just fine 
yesterday? `git diff` will tell you what exactly you touched recently.

And finally, reusability. Pieces of code are easier to adapt and reuse than model files.

### Just use OpenSCAD!
Yes, I did! In fact my first ever functional 3d print was modelled with it! But, despite all the greatness it has two
flaws:
 - One can't interact with a shape once it's created. One example that affected me the most: you can't automatically 
 join 2 shapes and fillet the edges in a generic way.
 - Custom language. I want my `numpy`, damn it! And an IDE with autocompletes, etc.
 
`SolidPython` solves the second problem (and their concept of holes is awesome!), but the fillet problem stays strong. 

Another interesting project is `pythonocc-core`: a python wrapper for OpenCascade. Definitely worth trying. 

### So, FreeCAD helpers?
Yes. A set of assorted modules that make FreeCAD API a bit friendlier to your code:

 - `freecaddy.transforms`: "baked" transforms, separate from shapes and between components.
 - `freecaddy.functional`: shape operations as standalone functions: `a.cut(b).cut(c).cut(d)` becomes `diff(a, b, c, d)`
 - `freecaddy.run_in_freecad`: a one-line way to run code in existing freecad document straight from your IDE.
