import java.awt.*;

/**
 *  An IslandSimulation. Simulates people hunting for treasure on an island.
 */
public class IslandSimulation extends Frame {
    private Map map = new Map();
    private Person[] people = new Person[8];

    /**
     * Main method that starts the simulation.
     */
    public static void main(String[] args) {

        IslandSimulation island = new IslandSimulation();

        island.map = new Map();
        island.map.resize(540, 400);
        island.map.move(0, 0);
        island.map.setBackground(Color.white);
        island.map.show();

        island.people[0] = new Person("Person1",1);
        island.people[1] = new Person("Person2",2);

        island.people[0].addToPath(island.map, Direction.EAST, new GridLoc(2, 2));
        island.people[0].setSpeed(620);
        island.people[1].addToPath(island.map, Direction.SOUTH, new GridLoc(1, 5));
        island.people[1].setSpeed(350);
    }
}

