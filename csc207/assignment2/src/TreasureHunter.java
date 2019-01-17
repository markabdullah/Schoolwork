import java.awt.*;
import java.awt.geom.Ellipse2D;

/**
 * Represents a TreasureHunter.
 */
class TreasureHunter {
    private Color color = Color.blue;
    private Path currentPath;
    private Direction direction; // The direction in which I entered the current Path.
    private int id;
    protected int score = 0;

    /**
     * Creates a TreasureHunter with the given id.
     * @param id The TreasureHunters id number.
     */
    public TreasureHunter(int id) {
        this.id = id;
    }

    /**
     * Sets the direction
     * @param direction The direction to set the TreasureHunter in.
     */
    public void setDirection(Direction direction) {
        this.direction = direction;
    }

    /**
     * Place this TreasureHunter on the given path.
     * @param path The path for the TreasureHunter to be placed on.
     */
    public void setPath(Path path) {
        currentPath = path;
    }

    /**
     * Returns The current path of the TreasureHunter.
     * @return The current path of the TreasureHunter.
     */
    public Path getPath(){
        return currentPath;
    }

    /**
     * Moves the TreasureHunter forward one piece.
     */
    public void move() {
        Direction nextDirection = currentPath.exit(direction).opposite();
        Path nextPath = currentPath.nextPath(direction);
        nextPath.enter(this);
        currentPath.leave();
        currentPath = nextPath;
        direction = nextDirection;
    }

    /**
     * Redraw the TreasureHunter.
     * @param g The graphics representation of the TreasureHunter.
     */
    public void draw(Graphics g) {
        Graphics2D g2 = (Graphics2D) g;
        Rectangle b = currentPath.bounds();

        double width = b.width;
        double height = b.height;

        Ellipse2D circle = new Ellipse2D.Double(width / 3, height / 3, width / 2, height / 2);

        g2.setColor(color);
        g2.fill(circle);
        g2.setStroke(new BasicStroke(2));
        g2.draw(circle);

        g2.setColor(Color.black);
        g2.setStroke(new BasicStroke(5));
        g2.setFont(new Font("default", Font.BOLD, 16));
        g2.drawString(Integer.toString(id), (int) width / 2, (int) height / 2);
    }

    public String toString() {
        return "TreasureHunter " + id;
    }
}

