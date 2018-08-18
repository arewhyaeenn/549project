# Graphy
Visualize graph creation and search
Visually build neural nets, export, and use in C#

Run Graphy.py to start.

## Modes:
> Graphy is in graph mode by default; if you'd like to build a neural net, click "File-->New-->Neural Net"
> Created graphs and nets can be saved (File-->Save/Save As)
> Saved graphs can be opened (File-->Open)
> A few other basic functionalities exist... see for yourself!

## Controls (graph mode):

### To create a vertex:
> 1) left click vertex creation button (bottom left)
> 2) position vertex as desired and left click again to place

### To create an edge:
> 1) left click a vertex to start the edge
> 2) left click a second vertex to complete the edge

### To reposition an edge or vertex:
> 1) right click object to pick it up
> 2) reposition as desired, left click to place

### To select an edge or vertex:
> middle click desired object (or CTRL click it)

## Controls(neural net mode):
> The controls are nearly identical to graph mode
> Each vertex is a layer in your neural net
> Each edge is actually multiple edges, connecting every node in one layer to every node in the other
> Exported nets can be read and used in C# using the Net class in Nets/csharp