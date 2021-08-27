# Path visualizer

## Usage

To perform actions use the commandline provided at the bottom of the screen.  

### Command options
* help: Prompts the user with a help screen
* exit: Exit the help menu   
* search -arg:  Starts path finding using the given algorithm. 
    * args: -astar, -dijkstra, -bfs, -reset
* walls -arg: creates walls bases on argument
    * args: -random, -maze, -reset
* restart: Resets the screen
* quit: Closes the application

### Mouse options
* Left mouse: Hold down/click on the grid to create walls
* Right mouse: Hold down/click to remove wall from grid

## Algorithms
* Astar(astar): Uses heuristics to find the optimal path
* Breadth-first search(bfs): Unweighted search that finds optimal path
* Dijkstra(dijkstra): Similiar to Astar, but without heuristics. Finds optimal path

## Examples
Run visualizer using Astar:  
* search -astar   
Run visualizer using Breadth-first search:   
* search -dijkstra
Reset search:
* search -reset
Set random walls:
* walls -random
Reset walls:
* walls -reset
To reset the screen
* restart


