/**

The NSEPath class.  An NSEPath object has three exits.

*/
class NSEPath extends SwitchPath {

    public NSEPath(GridLoc loc, Map T) {
        super(Direction.NORTH, Direction.SOUTH, Direction.EAST, loc, T);
        setLoc(loc);
        startAngle = 180;
    }

    public void setLoc(GridLoc loc) {
        super.setLoc(loc);
        x1 = 0.5;
        y1 = 0.0;
        x2 = 0.5;
        y2 = 1.0;
        x3 = 0.5;
        y3 = -0.5;
    }

    public String toString() {
        return "NSEPath";
    }
}

