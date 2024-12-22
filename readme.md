## Set viewBox to the SVG file genarated by PowerPoint

The svg file genarated by PowerPoint doesn't have viewBox attribute.

This script spcifies viewBox attribute by using width and height values.  
The width and height values are removed instead adding viewBox.  
And also, remove [overflow="hidden"] attribute.

This script enumerates all '*.svg' files in the current folder, and processes all of them.

The svg files will be overwritten.

example :  
befor modify  
> <svg width="1234" height="789" overflow="hidden" ... >

after modify  
> <svg viewBox="0 0 1234 789" ... >

## Environment

- Windows 11 Pro
- Python 3.13.0

