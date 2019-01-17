/**

The NSPath class.  A NSPath object has a north and south end.

*/
class NSPath extends StraightPath {

    public NSPath(GridLoc loc, Map T) {
        super(Direction.NORTH, Direction.SOUTH, loc, T);
        setLoc(loc);
    }

    public void setLoc(GridLoc loc) {
        super.setLoc(loc);
        x1 = 0.5;
        y1 = 0.0;
        x2 = 0.5;
        y2 = 1.0;
    }

    public String toString() {
        return "NSPath";
    }
}

