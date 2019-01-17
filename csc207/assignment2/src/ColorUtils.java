import java.awt.Color;

// Some utilities to make color management easier.
// ----------------------------------------------------------------------
public class ColorUtils {

    // Return a color similar to color, but brighter by amount f.  (The
    // closer f is to 0, the larger the difference.)
    // ------------------------------------------------------------------
    static Color brighter(Color c, double f) {
        return new Color(Math.min((int) (c.getRed() * (1 / f)), 255),
                Math.min((int) (c.getGreen() * (1 / f)), 255),
                Math.min((int) (c.getBlue() * (1 / f)), 255));
    }

    // Return a color similar to color, but darker by amount f.  (The
    // closer f is to 0, the larger the difference.)
    // ------------------------------------------------------------------
    static Color darker(Color c, double f) {
        return new Color(Math.max((int) (c.getRed() * f), 0),
                Math.max((int) (c.getGreen() * f), 0),
                Math.max((int) (c.getBlue() * f), 0));
    }
}

