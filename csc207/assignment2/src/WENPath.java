/**

The WENPath class.  An WENPath object has three ends.

*/
class WENPath extends SwitchPath {

    public WENPath(GridLoc loc, Map T) {
        super(Direction.WEST, Direction.EAST, Direction.NORTH, loc, T);
        setLoc(loc);
        startAngle = 270;
    }

    public void setLoc(GridLoc loc) {
        super.setLoc(loc);
        x1 = 0.0;
        y1 = 0.5;
        x2 = 1.0;
        y2 = 0.5;
        x3 = -0.5;
        y3 = -0.5;
    }

    public String toString() {
        return "WENPath";
    }
}