/**
The EmptyPath class.  This is a place on the Map which does not have an actual
piece of path.
*/
class EmptyPath extends Path {

    public EmptyPath(Map T) {
        super(T);
    }

    public boolean exitOK(Direction d) {
        return false;
    }

    public void register(Path r, Direction d) {
    }

    public void unRegister(Direction d) {
    }

    public Direction exit(Direction d) {
        return null;
    }

    public Path nextPath(Direction d) {
        return null;
    }

}

