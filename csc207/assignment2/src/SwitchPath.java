import java.awt.*;

/**
The SwitchPath class.  A SwitchPath object has three ends, and a controller
which determines which ends are used.  If a TreasureHunter moves on from the first end,
the switch determines which of the other two ends it leaves from.  If it moves
on from one of the other two ends, it automatically leaves by the first end.
*/
class SwitchPath extends Path {

    // My line coordinates for drawing myself.
    protected double x1, y1, x2, y2, x3, y3;

    // Info for my corner portion.
    int startAngle;

    // (end1,end2) and (end1,end3) are the two pairs.
    // end1 and end2 are the straight directions (i.e., they are
    // opposite each other), and end1 and end3 form the corner.
    private Direction end1, end2, end3;

    private Path neighbour1;  // The Path in the direction end1.
    private Path neighbour2;  // The Path in the direction end2.
    private Path neighbour3;  // The Path in the direction end3.

    // Whether I am aligned to go straight.
    private boolean goingStraight;

    public SwitchPath(Direction e1, Direction e2, Direction e3, GridLoc loc, Map T) {
        super(loc, T);
        color = Color.magenta;
        end1 = e1;
        end2 = e2;
        end3 = e3;
    }

    public boolean exitOK(Direction d) {
        return d.equals(end1) || d.equals(end2) || d.equals(end3);
    }

    // Register that r is adjacent to me from direction d.
    public void register(Path p, Direction d) {
        if (d.equals(end1)) neighbour1 = p;
        else if (d.equals(end2)) neighbour2 = p;
        else if (d.equals(end3)) neighbour3 = p;
    }

    public void unRegister(Direction d) {
        if (d.equals(end1)) neighbour1 = null;
        else if (d.equals(end2)) neighbour2 = null;
        else if (d.equals(end3)) neighbour3 = null;
    }

    // Given that d is the Direction from which a Car entered,
    // report where the Car will exit.
    // Note that if d is not end1's Direction, then it will have to
    // exit toward end1.
    public Direction exit(Direction d) {
        if (d.equals(end1) && goingStraight) return end2;
        else if (d.equals(end1) && !goingStraight) return end3;
        else if (d.equals(end2) || d.equals(end3)) return end1;
        return null;
    }

    // d is the direction that I entered from, and must be one of end1, end2 and end3.
    // Return the Path at the other end.
    public Path nextPath(Direction d) {
        if (d.equals(end1) && goingStraight) return neighbour2;
        else if (d.equals(end1) && !goingStraight) return neighbour3;
        else if (d.equals(end2) || d.equals(end3)) return neighbour1;
        return null;
    }

    // Handle a mouse click.  This will toggle the direction of the switch.
    public boolean handleEvent(Event evt) {
        if (evt.id == Event.MOUSE_DOWN && !isOccupied()) {
            goingStraight = !goingStraight;
            repaint();
            return true;
        }
        // If we get this far, I couldn't handle the event
        return false;
    }

    // Redraw myself.
    public void draw(Graphics g) {
        Rectangle b = bounds();
        int arcAngle = 90;
        Graphics2D g2 = (Graphics2D) g;
        g2.setStroke(new BasicStroke(12));

        // Draw current direction of the switch darker.
        if (goingStraight) {
            g2.setColor(Color.lightGray);
            g2.drawArc((int) (x3 * b.width), (int) (y3 * b.height),
                    b.width, b.height, startAngle, arcAngle);
            g2.setColor(color);
            g2.drawLine((int) (x1 * b.width), (int) (y1 * b.height),
                    (int) (x2 * b.width), (int) (y2 * b.height));
        } else {
            g2.setColor(Color.lightGray);
            g2.drawLine((int) (x1 * b.width), (int) (y1 * b.height),
                    (int) (x2 * b.width), (int) (y2 * b.height));
            g2.setColor(color);
            g2.drawArc((int) (x3 * b.width), (int) (y3 * b.height),
                    b.width, b.height, startAngle, arcAngle);
        }

        super.draw(g);
    }

    public String toString() {
        return "SwitchPath";
    }
}

