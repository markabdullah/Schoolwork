/**

The NEPath class.  A NEPath object has ends at the north and east.

*/
class NEPath extends CornerPath {

    public NEPath(GridLoc loc, Map T) {
        super(Direction.NORTH, Direction.EAST, loc, T);
        setLoc(loc);
        startAngle = 180;
    }

    public void setLoc(GridLoc loc) {
        super.setLoc(loc);
        x1 = 0.5;
        y1 = -0.5;
    }

    public String toString() {
        return "NEPath";
    }
}

