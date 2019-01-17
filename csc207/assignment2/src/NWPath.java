/**

The NWPath class.  A NWPath object has ends at the north and west.

*/
class NWPath extends CornerPath {

    public NWPath(GridLoc loc, Map T) {
        super(Direction.NORTH, Direction.WEST, loc, T);
        setLoc(loc);
        startAngle = 270;
    }

    public void setLoc(GridLoc loc) {
        super.setLoc(loc);
        x1 = -0.5;
        y1 = -0.5;
    }

    public String toString() {
        return "NWPath";
    }
}

