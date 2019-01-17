/**

The SNWPath class.  An SNWPath object has three ends.

*/
class SNWPath extends SwitchPath {

    public SNWPath(GridLoc loc, Map T) {
        super(Direction.SOUTH, Direction.NORTH, Direction.WEST, loc, T);
        setLoc(loc);
        startAngle = 0;
    }

    public void setLoc(GridLoc loc) {
        super.setLoc(loc);
        x1 = 0.5;
        y1 = 0.0;
        x2 = 0.5;
        y2 = 1.0;
        x3 = -0.5;
        y3 = 0.5;
    }

    public String toString() {
        return "SNWPath";
    }
}

