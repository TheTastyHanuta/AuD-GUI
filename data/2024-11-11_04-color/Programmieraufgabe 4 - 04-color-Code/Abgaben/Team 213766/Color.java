/*
 Carl Soergel, Matrikelnummer: 22367168
 Carlo Fuchs, Matrikelnummer: 21901371
 */

public class Color {

    private int rgb;
    // Statische, nicht veraenderliche Color-Objekte
    public static final Color BLACK = new Color(0, 0, 0);
    public static final Color WHITE = new Color(255, 255, 255);
    public static final Color GREY = new Color(128, 128, 128);
    public static final Color RED = new Color(255, 0, 0);
    public static final Color GREEN = new Color(0, 255, 0);
    public static final Color BLUE = new Color(0, 0, 255);

    // Ausgewaehlte Farben
    public static final Color ORANGE = new Color(255, 165, 0);
    public static final Color ROYALBLUE = new Color(65, 105, 225);
    public static final Color DARKRED = new Color(139, 0, 0);
    public static final Color FUCHSIA = new Color(255, 0, 255);

    public static void main(String[] args) {
        // Testen des Konstruktors fuer direkte Uebergabe der int-Darstellung
        Color black = new Color(0);
        System.out.println("Black RGB-Wert: " + black.getRgb());

        // Testen des Konstruktors fuer red, green und blue Werte
        Color red = new Color(255, 0, 0);
        System.out.println("Red RGB-Wert: " + red.getRgb());
        ColorVisualizer visualizerred = new ColorVisualizer(red);

        // Testen des Standard-Konstruktors fuer die Farbe Schwarz
        Color defaultColor = new Color();
        System.out.println("Default Color RGB-Wert: " + defaultColor.getRgb());
        ColorVisualizer visualizerdefault = new ColorVisualizer(defaultColor);

        // Testen der Methoden mit weiteren Farbwerte aus der Farbtabelle
        Color complementaryORANGE = ORANGE.complementaryColor();//Test Complement mit Visualisierung
        //System.out.println("Complementary ORANGE RGB-Wert: " + complementaryORANGE.getRgb());
        ColorVisualizer visualizerorange = new ColorVisualizer(ORANGE);
        ColorVisualizer visualizercomporange = new ColorVisualizer(complementaryORANGE);

        Color mixedDARKREDandWHITE = DARKRED.mixColor(WHITE); //Test MIX mit Visualisierung
        //System.out.println("RGB-Wert von Mischung aus DARKRED und WHITE: " + mixedDARKREDandWHITE.getRgb());
        ColorVisualizer visualizerDARKRED = new ColorVisualizer(DARKRED);
        ColorVisualizer visualizerWHITE = new ColorVisualizer(WHITE);
        ColorVisualizer visualizermixedDARKREDandWHITE = new ColorVisualizer(mixedDARKREDandWHITE);

        System.out.println("Fuchsia Hexadezimalwert: " + FUCHSIA.getHex()); //Test HEX
        System.out.println("RGB-Werte fuer Royalblue: " + "Red: " + ROYALBLUE.getRed() + " Green: "
                + ROYALBLUE.getGreen() + " Blue: " + ROYALBLUE.getBlue()); //noch ziemlich dirty sollte Methode sein

        Color crimson = new Color("#DC143C");
        Color darkCyan = new Color("008B9B");
        Color darkGoldenRod = new Color("B8860B");
        Color darkRed = new Color("8B0000");

        /*
        // Testen der Fehlermeldung.
        Color notAColor = new Color(-3, 257, 13);
        // Ausgabe wie erwartet:
        // Fehler: Der Farbwert darf nicht kleiner als 0 sein. Setze auf 0.
        // Fehler: Der Farbwert darf nicht groesser als 255 sein. Setze auf 255.
         */
    }

    // Konstruktor fuer die direkte Uebergabe der int-Darstellung
    public Color(int rgb) {
        this.rgb = rgb;
    }

    // Konstruktor fuer red, green und blue Werte
    public Color(int red, int green, int blue) {
        // ueberpruefen und korrigieren der Werte
        this.rgb = ((validateAndCreateRGB(red) << 16) & 0xFF0000) |
                ((validateAndCreateRGB(green) << 8) & 0x00FF00) |
                (validateAndCreateRGB(blue) & 0x0000FF);
    }

    // Standard-Konstruktor Schwarz
    public Color() {
        this.rgb = 0;
    }

    // Ueberpruefung mit Fehlermeldung der Farbkanalwerte
    private int validateAndCreateRGB(int value) {
        if (value < 0) {
            System.err.println("Fehler: Der Farbwert darf nicht kleiner als 0 sein. Setze auf 0.");
            return 0;
        } else if (value > 255) {
            System.err.println("Fehler: Der Farbwert darf nicht groesser als 255 sein. Setze auf 255.");
            return 255;
        } else {
            return value;
        }
    }

    // Getter-Methode fuer rgb
    public int getRgb() {
        return rgb;
    }

    // Getter-Methode roter Farbkanal
    public int getRed() {
        return (rgb >> 16) & 0xFF;
    }

    // Getter-Methode gruener Farbkanal
    public int getGreen() {
        return (rgb >> 8) & 0xFF;
    }

    // Getter-Methode blauer Farbkanal
    public int getBlue() {
        return rgb & 0xFF;
    }

    // Getter-Methode fuer die 6-stellige Hexadezimaldarstellung
    public String getHex() {
        // Die Methode Integer.toHexString() wandelt den int-Wert in einen Hexadezimalstring um
        String hexString = Integer.toHexString(rgb);

        // Fuelle fuehrende Nullen auf, wenn noetig (um auf 6 Stellen zu kommen)
        while (hexString.length() < 6) {
            hexString = "0" + hexString;
        }

        // Fuege den #-Praefix hinzu und konvertiere den String zu Grossbuchstaben
        return "#" + hexString.toUpperCase();
    }

    // Konstruktor fuer Uebergabe Hexadezimaldarstellung
    public Color(String hex) {
        // Entfernen des #-Praefix, falls vorhanden
        hex = hex.replace("#", "");
        // Parsen des Hexadezimalstring und speichern in rgb
        rgb = Integer.parseInt(hex, 16);
    }

    public String toString() {
        // Verwendung der getHex()-Methode, um die Hexadezimaldarstellung zu erhalten
        return getHex();
    }

    public Color complementaryColor() {
        int red = 255 - getRed();
        int green = 255 - getGreen();
        int blue = 255 - getBlue();
        return new Color(red, green, blue);
    }

    public Color mixColor(Color color) {
        int newRed = (getRed() + color.getRed()) / 2;
        int newGreen = (getGreen() + color.getGreen()) / 2;
        int newBlue = (getBlue() + color.getBlue()) / 2;
        return new Color(newRed, newGreen, newBlue);
    }

}