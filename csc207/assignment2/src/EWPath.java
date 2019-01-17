/**

The EWPath class.  An EWPath object has two ends,
which must be opposite each other.

*/
class EWPath extends StraightPath {

    public EWPath(GridLoc loc, Map T) {
        super(Direction.EAST, Direction.WEST, loc, T);
        setLoc(loc);
    }

    public void setLoc(GridLoc loc) {
        super.setLoc(loc);
        x1 = 0.0;
        y1 = 0.5;
        x2 = 1.0;
        y2 = 0.5;
    }

    public String toString() {
        return "EWPath";
    }
}