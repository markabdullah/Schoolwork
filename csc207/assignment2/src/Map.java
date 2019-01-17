import java.awt.*;
/**
 Represents a map. Simulations can be performed on this map.

*/
public class Map extends Frame {
    private MapPanel mapPanel; // The Panel on which the Map appears.
    private Person[] personList = new Person[10];
    private Path[][] paths = new Path[10][10]; // The grid of paths.
    private int numPersons = 0;
    private boolean running = false;    // Whether my TreasureHunters are running.  If true, no more Paths can be placed.
    private Label statusLabel;  // The following label is used to display the scores of the TreasureHunters.

    /**
     * Constructs a new a Map.
     */
    public Map() {
        buildMapPaths();
        buildMapPanel();
        spawnTreasure(5, 3);
    }

    /**
     * Builds the panel which contains the map window.
     */
    private void buildMapPanel() {
        mapPanel = new MapPanel();
        add("Center", mapPanel);

        Button runStopButton = new Button("Run");
        Button quitButton = new Button("Quit");
        Button accelButton = new Button("Accelerate");
        Button decelButton = new Button("Decelerate");
        Button accelLotsButton = new Button("Accelerate A Lot");
        Button decelLotsButton = new Button("Decelerate A Lot");

        Panel p2 = new Panel();
        p2.setLayout(new GridLayout(0, 1));
        p2.add(runStopButton);
        p2.add(accelLotsButton);
        p2.add(decelLotsButton);
        p2.add(accelButton);
        p2.add(decelButton);
        p2.add(quitButton);
        add("East", p2);

        statusLabel = new Label("Player 1: 0 --- Player 2: 0");

        Panel p3 = new Panel();
        p3.add(statusLabel);
        add("South", p3);

        pack();
        mapPanel.setBackground(new Color(152, 251, 152));
        mapPanel.addToPanel(paths);
    }

    private void buildMapPaths() {
        for (int row = 0; row < paths.length; row++) {
            for (int col = 0; col < paths[0].length; col++) {
                paths[row][col] = new EmptyPath(this);
            }
        }

        paths[0][0] = new SEPath(new GridLoc(0, 0), this);
        paths[0][1] = new EWPath(new GridLoc(0, 1), this);
        paths[0][2] = new SWPath(new GridLoc(0, 2), this);

        paths[1][0] = new NSPath(new GridLoc(1, 0), this);
        paths[1][2] = new NSPath(new GridLoc(1, 2), this);
        paths[1][5] = new SEPath(new GridLoc(1, 5), this);
        paths[1][6] = new EWPath(new GridLoc(1, 6), this);
        paths[1][7] = new SWPath(new GridLoc(1, 7), this);

        paths[2][0] = new NEPath(new GridLoc(2, 0), this);
        paths[2][1] = new EWPath(new GridLoc(2, 1), this);
        paths[2][2] = new CrossPath(new GridLoc(2, 2), this);
        paths[2][3] = new EWPath(new GridLoc(2, 3), this);
        paths[2][4] = new EWPath(new GridLoc(2, 4), this);
        paths[2][5] = new CrossPath(new GridLoc(2, 5), this);
        paths[2][6] = new SWPath(new GridLoc(2, 6), this);
        paths[2][7] = new NSPath(new GridLoc(2, 7), this);

        paths[3][1] = new SEPath(new GridLoc(3, 1), this);
        paths[3][2] = new CrossPath(new GridLoc(3, 2), this);
        paths[3][3] = new EWSPath(new GridLoc(3, 3), this);
        paths[3][4] = new SWPath(new GridLoc(3, 4), this);
        paths[3][5] = new NEPath(new GridLoc(3, 5), this);
        paths[3][6] = new NWPath(new GridLoc(3, 6), this);
        paths[3][7] = new NSPath(new GridLoc(3, 7), this);

        paths[4][1] = new NEPath(new GridLoc(4, 1), this);
        paths[4][2] = new WENPath(new GridLoc(4, 2), this);
        paths[4][3] = new SNWPath(new GridLoc(4, 3), this);
        paths[4][4] = new NEPath(new GridLoc(4, 4), this);
        paths[4][5] = new WESPath(new GridLoc(4, 5), this);
        paths[4][6] = new EWPath(new GridLoc(4, 6), this);
        paths[4][7] = new NWPath(new GridLoc(4, 7), this);

        paths[5][3] = new NEPath(new GridLoc(5, 3), this);
        paths[5][4] = new EWPath(new GridLoc(5, 4), this);
        paths[5][5] = new CrossPath(new GridLoc(5, 5), this);
        paths[5][6] = new SWPath(new GridLoc(5, 6), this);

        paths[6][5] = new NSEPath(new GridLoc(6, 5), this);
        paths[6][6] = new NSWPath(new GridLoc(6, 6), this);

        paths[7][5] = new NEPath(new GridLoc(7, 5), this);
        paths[7][6] = new NWPath(new GridLoc(7, 6), this);

        for (int row = 0; row < paths.length; row++) {
            for (int col = 0; col < paths[0].length; col++) {
                connectPath(row, col);
            }
        }

    }

    /**
     * Handle events caused by the user.
     * @param evt The event to be handled.
     * @return True if the event was handled, false otherwise.
     */
    public boolean handleEvent(Event evt) {
        Object target = evt.target;

        if (evt.id == Event.ACTION_EVENT) {
            if (target instanceof Button) {
                if ("Run".equals(evt.arg)) {
                    running = true;
                    for (int i = 0; i < numPersons; i++) {
                        personList[i].start();
                    }
                    ((Button) target).setLabel("Suspend");
                } else if ("Suspend".equals(evt.arg)) {
                    for (int i = 0; i < numPersons; i++) {
                        personList[i].suspend();
                    }
                    running = false;
                    ((Button) target).setLabel("Resume");
                } else if ("Resume".equals(evt.arg)) {
                    for (int i = 0; i < numPersons; i++) {
                        personList[i].resume();
                    }
                    running = false;
                    ((Button) target).setLabel("Suspend");
                } else if ("Accelerate".equals(evt.arg)) {
                    for (int i = 0; i < numPersons; i++) {
                        personList[i].accelerate();
                    }
                } else if ("Decelerate".equals(evt.arg)) {
                    for (int i = 0; i < numPersons; i++) {
                        personList[i].decelerate();
                    }
                } else if ("Accelerate A Lot".equals(evt.arg)) {
                    for (int i = 0; i < numPersons; i++) {
                        personList[i].accelerateALot();
                    }
                } else if ("Decelerate A Lot".equals(evt.arg)) {
                    for (int i = 0; i < numPersons; i++) {
                        personList[i].decelerateALot();
                    }
                } else if ("Quit".equals(evt.arg)) {
                    for (int i = 0; i < numPersons; i++) {
                        personList[i].stop();
                    }
                    running = false;
                    System.exit(0);
                }
                return true;
            }
        }
        // If we get this far, I couldn't handle the event
        return false;
    }

    /**
     * Register
     * @param test A boolean test to check
     * @param path1 The first path
     * @param path2 THe second path
     * @param d The direction from path1 to path2
     */
    private void registerOrUnRegister(boolean test, Path path1, Path path2, Direction d) {
        if (test && path1 != null && path1.exitOK(d)) {
            if (path2.exitOK(d.opposite())) {
                connectPaths(path1, path2, d);
            } else {
                path1.unRegister(d);
            }
        }
    }

    /**
     * Connect a path to available immediate surrounding paths given its coordinates.
     * @param row The row number of the path
     * @param col The column number of the path
     */
    private void connectPath(int row, int col) {
        Path r = paths[row][col];

        Direction north = Direction.NORTH;
        Direction south = Direction.SOUTH;
        Direction east = Direction.EAST;
        Direction west = Direction.WEST;

        if (r != null) {
            Path rN = row > 0 ? paths[row - 1][col] : null;
            Path rS = row < paths.length - 1 ? paths[row + 1][col] : null;
            Path rE = col < paths[0].length - 1 ? paths[row][col + 1] : null;
            Path rW = col > 0 ? paths[row][col - 1] : null;

            registerOrUnRegister(row > 0, rN, r, south);
            registerOrUnRegister(row < paths.length - 1, rS, r, north);
            registerOrUnRegister(col > 0, rW, r, east);
            registerOrUnRegister(col < paths[0].length - 1, rE, r, west);
        }
    }

    /**
     * Connects path1 to path2
     * @param path1 The first path
     * @param path2 The second path
     * @param d The direction of path2 from path1
     */
    private void connectPaths(Path path1, Path path2, Direction d) {
        path1.register(path2, d);
        path2.register(path1, d.opposite());
    }

    /**
     * Add a person to this map.
     * @param person The person to be added.
     * @param loc The location to add the person on the map.
     */
    public void addPerson(Person person, GridLoc loc) {
        personList[numPersons] = person;
        numPersons++;
        paths[loc.row][loc.col].enter(person.treasureHunter);
        person.treasureHunter.setPath(paths[loc.row][loc.col]);
    }

    public void updateStatusBar() {
        statusLabel.setText("Player 1: " + personList[0].getScore() +
                " --- Player 2: " + personList[1].getScore());
        statusLabel.repaint();
    }

    /**
     * Spawns Treasure on a random, valid piece of a path on the Map.
     */
    public void spawnTreasure() {
        int row, col;
        //find suitable place for treasure to respawn
        do {
            row = (int) (Math.random() * 10);
            col = (int) (Math.random() * 10);
        } while ((paths[row][col] instanceof EmptyPath));

        spawnTreasure(row, col);
    }

    private void spawnTreasure(int row, int col) {
        paths[row][col].hasTreasure = true;
        paths[row][col].repaint();
    }

}
