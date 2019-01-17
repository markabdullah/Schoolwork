/**

The EWSPath class.  An EWSPath object has three ends.

*/
class EWSPath extends SwitchPath {

    public EWSPath(GridLoc loc, Map T) {
        super(Direction.EAST, Direction.WEST, Direction.SOUTH, loc, T);
        setLoc(loc);
        startAngle = 90;
    }

    public void setLoc(GridLoc loc) {
        super.setLoc(loc);
        x1 = 0.0;
        y1 = 0.5;
        x2 = 1.0;
        y2 = 0.5;
        x3 = 0.5;
        y3 = 0.5;
    }

    public String toString() {
        return "EWSPath";
    }
}