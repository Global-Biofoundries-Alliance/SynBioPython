# Synbiopython lab automation module

## Code organization:

The different classes are organized as follows:

- A *Plate* contains *Wells* organized in a grid.
- A *Well* contains data (which can be of any kind, barcode, plate reader time series data, etc.), and some *WellContent* which defines the volume of liquid in the well and the different quantities of its components.
- A *Picklist* is a list of *Transfers* from a *Well* to another *Well*.
