/**

The Person class.

A Person is used to represent a player in the IslandSimulation.
 Each turn, a Person will move forward on the Map.

*/
public class Person extends Thread {

    private int delay;          // The amount of time between each of my turns.
    protected TreasureHunter treasureHunter;      // The TreasureHunter this person represents.

    /**
     * Creates a Person.
     * @param threadName The name to represent this Person.
     * @param id This Persons id number.
     */
    public Person(String threadName, int id) {
        super(threadName);
        treasureHunter = new TreasureHunter(id);
    }

    /**
     * Set this persons speed. The lower the delay, the higher the speed.
     * @param d Delay.
     */
    public void setSpeed(int d) {
        delay = d;
    }

    public int getScore() {
        return treasureHunter.score;
    }

    public void setScore(int score) {
        treasureHunter.score = score;
    }

    /**
     * Adds this Person to a Map object.
     * @param map Map to be put on.
     * @param dir Direction to be placed facing.
     * @param loc Location on the map to be placed in.
     */
    public void addToPath(Map map, Direction dir, GridLoc loc) {
        map.addPerson(this, loc);
        treasureHunter.setDirection(dir);
    }

    // Halve my delay.
    public void accelerateALot() {
        delay /= 2;
    }

    // Double my delay.
    public void decelerateALot() {
        delay *= 2;
    }

    // Speed up by a factor of 20ms.
    public void accelerate() {
        delay -= 20;
    }

    // Slow down by a factor of 20ms.
    public void decelerate() {
        delay += 20;
    }


    public void run() {
        while (true) {
            treasureHunter.move();

            // Sleep for 1 second.
            try {
                sleep(delay);
            } catch (InterruptedException e) {
            }
        }
    }

}

