import java.awt.*;
import java.awt.geom.Ellipse2D;

/**
 * The Path class. Represents a piece of path used to create a map.
 */
abstract class Path extends Canvas {

    private TreasureHunter currentTH; // currentTreasureHunter
    private boolean isOccupied = false;
    private GridLoc location;
    private Map theMap;
    protected Color color;
    protected boolean hasTreasure;

    /**
     * Creates a path piece.
     * @param loc The location of the path
     * @param map The math this piece of path is to be placed on.
     */
    public Path(GridLoc loc, Map map) {
        location = loc;
        theMap = map;
    }

    /**
     * Creates a path piece.
     * @param map The math this piece of path is to be placed on.
     */
    public Path(Map map) {
        theMap = map;
    }

    public boolean isOccupied() {
        return isOccupied;
    }

    public void setLoc(GridLoc loc) {
        location = loc;
    }

    public GridLoc getLoc() {
        return location;
    }

    // Redraw myself.
    public void draw(Graphics g) {
        Graphics2D g2 = (Graphics2D) g;

        Rectangle b = bounds();
        g2.setStroke(new BasicStroke(1));
        g2.setColor(Color.lightGray);
        g2.drawRect(0, 0, b.width - 1, b.height - 1);
        g2.setStroke(new BasicStroke(12));

        if (isOccupied) {
            currentTH.draw(g2);
        }

        if (hasTreasure) {
            Ellipse2D circle = new Ellipse2D.Double(b.width / 3, b.height / 3, b.width / 2, b.height / 2);
            g2.setColor(Color.YELLOW);
            g2.fill(circle);
        }
    }

    /**
     * Register that a TreasureHunter is entering this path.
     * @param newTreasureHunter The TreasureHunter entering the path.
     */
    public void enter(TreasureHunter newTreasureHunter) {
        isOccupied = true;
        currentTH = newTreasureHunter;
        repaint();
        if (hasTreasure) {
            currentTH.score++;
            theMap.updateStatusBar();
            hasTreasure = false;
            theMap.spawnTreasure();
        }
    }

    /**
     * Register that a person has left this path.
     */
    public void leave() {
        repaint();
        isOccupied = false;
    }

    // Update my display.
    public void paint(Graphics g) {
        draw(g);
    }

    /**
     * Return true if d is a valid direction for me.
     */
    public abstract boolean exitOK(Direction d);

    /**
     * Register that Path path is in Direction d.
     * @param path The path to be registered to this.
     * @param d the Direction that path is in from this.
     */
    public abstract void register(Path path, Direction d);

    /**
     * Register that there is no Path in Direction d.
     * @param d The direction to unregister any paths from.
     */
    public abstract void unRegister(Direction d);

    /**
     * Given the direction a TreasureHunter has entered, return the direction it can exit in.
     * @param d The direction entered onto the path.
     * @return The direction which the TreasureHunter can exit.
     */
    public abstract Direction exit(Direction d);

    /**
     * Given the direction in which a TreasrueHunter entered this path, return the path it will go to next.
     * @param d The direction entered onto the path.
     * @return The path in the direction d from this path.
     */
    public abstract Path nextPath(Direction d);

    // Return myself as a string.
    public String toString() {
        return "Path";
    }

}

