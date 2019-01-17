import java.awt.*;

/**
The CrossPath class.  A CrossPath object has four ends.
*/
class CrossPath extends Path {

    // My line coordinates for drawing myself.
    private double x1, y1, x2, y2, x3, y3, x4, y4;

    // (end1,end2) and (end3,end4) are the two pairs.
    // The are, in order, always 'north', 'south', 'east', and 'west'.
    private Direction end1, end2, end3, end4;

    private Path neighbour1;  // The Path in the direction end1.
    private Path neighbour2;  // The Path in the direction end2.
    private Path neighbour3;  // The Path in the direction end3.
    private Path neighbour4;  // The Path in the direction end4.

    public boolean exitOK(Direction d) {
        return true;
    }

    /**
     * Creates a CrossPath piece of path.
     * @param loc The location of the path.
     * @param map The map for the path to be placed on.
     */
    public CrossPath(GridLoc loc, Map map) {
        super(loc, map);
        color = Color.orange;
        end1 = Direction.NORTH;
        end2 = Direction.SOUTH;
        end3 = Direction.EAST;
        end4 = Direction.WEST;
        setLoc(loc);
    }

    public void setLoc(GridLoc loc) {
        super.setLoc(loc);
        x1 = 0.0;
        y1 = 0.5;
        x2 = 1.0;
        y2 = 0.5;

        x3 = 0.5;
        y3 = 0.0;
        x4 = 0.5;
        y4 = 1.0;
    }


    public void register(Path r, Direction d) {
        if (d.equals(end1)) {
            neighbour1 = r;
        } else if (d.equals(end2)) {
            neighbour2 = r;
        } else if (d.equals(end3)) {
            neighbour3 = r;
        } else if (d.equals(end4)) {
            neighbour4 = r;
        }
    }


    public void unRegister(Direction d) {
        if (d.equals(end1)) {
            neighbour1 = null;
        } else if (d.equals(end2)) {
            neighbour2 = null;
        } else if (d.equals(end3)) {
            neighbour3 = null;
        } else if (d.equals(end4)) {
            neighbour4 = null;
        }
    }

    public Direction exit(Direction d) {
        if (d.equals(end1)) {
            return end2;
        } else if (d.equals(end2)) {
            return end1;
        } else if (d.equals(end3)) {
            return end4;
        } else if (d.equals(end4)) {
            return end3;
        }
        return null;
    }

    public Path nextPath(Direction d) {
        if (d.equals(end1)) {
            return neighbour2;
        } else if (d.equals(end2)) {
            return neighbour1;
        } else if (d.equals(end3)) {
            return neighbour4;
        } else if (d.equals(end4)) {
            return neighbour3;
        }
        return null;
    }

    public void draw(Graphics g) {
        Graphics2D g2 = (Graphics2D) g;

        g2.setStroke(new BasicStroke(12));

        g.setColor(color);
        Rectangle b = bounds();
        g.drawLine((int) (x1 * b.width), (int) (y1 * b.height),
                (int) (x2 * b.width), (int) (y2 * b.height));
        g.drawLine((int) (x3 * b.width), (int) (y3 * b.height),
                (int) (x4 * b.width), (int) (y4 * b.height));

        super.draw(g);
    }

    public String toString() {
        return "CrossPath";
    }
}