import java.awt.*;
/**

The TwoEndPath class.  A TwoEndPath object has two ends,
which may or may be not be opposite each other.

*/

class TwoEndPath extends Path {

    private Direction end1, end2;
    private Path neighbour1;  // The Path in the direction end1.
    private Path neighbour2;  // The Path in the direction end2.

    public boolean exitOK(Direction d) {
        return d.equals(end1) || d.equals(end2);
    }

    public TwoEndPath(Direction e1, Direction e2, GridLoc loc, Map T) {
        super(loc, T);
        color = Color.orange;
        end1 = e1;
        end2 = e2;
    }

    public void register(Path r, Direction d) {
        if (d.equals(end1)) neighbour1 = r;
        else if (d.equals(end2)) neighbour2 = r;
    }

    public void unRegister(Direction d) {
        if (d.equals(end1)) neighbour1 = null;
        else if (d.equals(end2)) neighbour2 = null;
    }

    public Direction exit(Direction d) {
        if (d.equals(end1)) return end2;
        else if (d.equals(end2)) return end1;
        return null;
    }

    public Path nextPath(Direction d) {
        if (d.equals(end1)) return neighbour2;
        else if (d.equals(end2)) return neighbour1;
        return null;
    }

    public String toString() {
        return "TwoEndPath";
    }
}

