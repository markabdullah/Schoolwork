import java.util.HashMap;

public enum Direction {
    NORTH,
    EAST,
    SOUTH,
    WEST;

    private static final HashMap<Direction, Direction> oppositeMap = createMap();
    private static HashMap<Direction, Direction> createMap(){
        HashMap<Direction, Direction> map = new HashMap<>();
        map.put(NORTH, SOUTH);
        map.put(SOUTH, NORTH);
        map.put(EAST, WEST);
        map.put(WEST, EAST);
        return map;
    }

    public Direction opposite(){
        return oppositeMap.get(this);
    }
}