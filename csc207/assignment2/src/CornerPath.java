import java.awt.*;

/**

The CornerPath class.  A CornerPath object has two ends,
which must be not be opposite each other.

*/

class CornerPath extends TwoEndPath {

    // The multipliers for the width and height.
    double x1, y1;
    int startAngle, arcAngle = 90;

    public CornerPath(Direction e1, Direction e2, GridLoc loc, Map T) {
        super(e1, e2, loc, T);
    }

    // Redraw myself.
    public void draw(Graphics g) {
        Graphics2D g2 = (Graphics2D) g;
        g2.setStroke(new BasicStroke(12));
        g2.setColor(color);
        Rectangle b = bounds();
        g2.drawArc((int) (x1 * b.width), (int) (y1 * b.height), b.width, b.height, startAngle, arcAngle);
        super.draw(g);
    }

    public String toString() {
        return "CornerPath";
    }
}

