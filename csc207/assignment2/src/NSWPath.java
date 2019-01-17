/**

The NSWPath class.  An NSWPath object has three ends, at the north, south and west.

*/
class NSWPath extends SwitchPath {

    public NSWPath(GridLoc loc, Map T) {
        super(Direction.NORTH, Direction.SOUTH, Direction.WEST, loc, T);
        setLoc(loc);
        startAngle = 270;
    }

    public void setLoc(GridLoc loc) {
        super.setLoc(loc);
        x1 = 0.5;
        y1 = 0.0;
        x2 = 0.5;
        y2 = 1.0;
        x3 = -0.5;
        y3 = -0.5;
    }

    public String toString() {
        return "NSWPath";
    }
}