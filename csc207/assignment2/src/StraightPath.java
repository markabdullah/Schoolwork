import java.awt.*;

/**

The StraightPath class.  A StraightPath object has two ends,
which must be opposite each other.

*/
class StraightPath extends TwoEndPath {

    // The multipliers for the endpoints of the StraightPath.
    double x1, y1, x2, y2;

    public StraightPath(Direction e1, Direction e2, GridLoc loc, Map T) {
        super(e1, e2, loc, T);
        color = Color.orange;
    }

    // Redraw myself.
    public void draw(Graphics g) {
        Graphics2D g2 = (Graphics2D) g;

        g2.setStroke(new BasicStroke(12));
        g2.setColor(color);
        Rectangle b = bounds();
        g2.drawLine((int) (x1 * b.width), (int) (y1 * b.height),
                (int) (x2 * b.width), (int) (y2 * b.height));

        super.draw(g2);
    }

    public String toString() {
        return "StraightPath";
    }

    ;
}

