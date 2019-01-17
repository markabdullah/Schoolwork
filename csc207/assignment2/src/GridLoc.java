/**
 * Represents an (x,y) location.
 */
public class GridLoc {
    public int row;
    public int col;

    public GridLoc(int row, int col) {
        this.row = row;
        this.col = col;
    }

    public String toString() {
        return (row + " " + col);
    }
}

