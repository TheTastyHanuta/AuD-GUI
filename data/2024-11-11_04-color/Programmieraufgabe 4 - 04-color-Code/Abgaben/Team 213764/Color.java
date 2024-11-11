//Author: Muhammad Ridwan Bagindo, 23363816
//Author: Pascal-Andre Stifter, 23117434

public class Color {
    private int rgb;    //Konstruktor fuer die int-Darstellung der Farbe

    public Color(int rgb) {     //Konstruktor mit den Farbkanaele
        this.rgb = rgb;
    }

    public Color(int red, int green, int blue) {
        if (!isValidColorValue(red) || !isValidColorValue(green) || !isValidColorValue(blue)) {
            System.err.println("Invalid values detected. Readjusting values to existing parameters [0, 255]!");

            red = correctColorValue(red);
            green = correctColorValue(green);
            blue = correctColorValue(blue);
        }

        this.rgb = (red << 16) | (green << 8) | blue;
    }

    private boolean isValidColorValue(int value) {  //ueberprueft ob der Farbwert im Intervall liegt
        return value >= 0 && value <= 255;
    }

    private int correctColorValue(int value) {  //korrigiert ein ungueltiges Farbintervall eine der Intervallgrenzen[0,255]
        return Math.min(Math.max(value, 0), 255);
    }

    public Color() {    //Standard-Konstruktor fuer die Farbe Schwarz
        this.rgb = 0;
    }

    public int getRgb() {   //oeffentliche Methode um rgb auszulesen
        return rgb;
    }

    //oeffentliche Getter fuer die Farbkanaele
    public int getRed() {
        return (rgb >> 16) & 0xFF;
    }

    public int getGreen() {
        return (rgb >> 8) & 0xFF;
    }

    public int getBlue() {
        return rgb & 0xFF;
    }

    public String getHex() {    //oeffentliche Methode um die Hexadezimaldarstellung zu lesen
        String hex = Integer.toHexString(rgb).toUpperCase();

        while (hex.length() < 6) {
            hex = "0" + hex;
        }

        return "#" + hex;
    }

    public Color(String hex) {  //Konstruktor uebernimmt die Hexadezimaldarstellung der Farbe als String mit #
        if (hex.startsWith("#")) {
            hex = hex.substring(1); // entfernt das Praefix
        }

        this.rgb = Integer.parseInt(hex, 16);   // speichert die Hexadezimalzahl im rgb
    }

    @Override   //ueberschreibung der toString()-Methode
    public String toString() {
        return getHex();
    }

    public Color complementaryColor() { //oeffentliche Methode um Komplementaerfarben zu berechnen
        int Red = 255 - getRed();
        int Green = 255 - getGreen();
        int Blue = 255 - getBlue();

        return new Color(Red, Green, Blue);
    }

    public Color mixColor(Color color) {    //oeffentliche Methode zum Mischen der Farben
        int mixRed = (getRed() + color.getRed()) / 2;
        int mixGreen = (getGreen() + color.getGreen()) / 2;
        int mixBlue = (getBlue() + color.getBlue()) / 2;

        return new Color(mixRed, mixGreen, mixBlue);
    }

    //Definition der haeufig verwendeten Farben
    public static final Color BLACK = new Color(0, 0, 0);
    public static final Color WHITE = new Color(255, 255, 255);
    public static final Color GRAY = new Color(128, 128, 128);
    public static final Color RED = new Color(255, 0, 0);
    public static final Color GREEN = new Color(0, 255, 0);
    public static final Color BLUE = new Color(0, 0, 255);

    //Main zum Testen
    public static void main(String[] args) {
        //Test des RGB Konstruktors
        Color color1 = new Color(8421504);
        System.out.println("RGB value: " + color1.getRgb());

        //Test des RGB Konstruktors zum Vergleichen mit den korrigierten
        Color color2 = new Color(255, 0, 255);
        System.out.println("Border RGB value: " + color2.getRgb());

        //Test des Standard-Konstruktors
        Color color3 = new Color();
        System.out.println("Black RGB value: " + color3.getRgb());

        //Test des Konstruktors mit ungueltigen RGB-Werten
        Color color4 = new Color(300, -50, 1200);
        System.out.println("Adjusted RBG value: " + color4.getRgb());

        /*
        //Test fuer den Visualizer
        new ColorVisualizer(BLACK);
        new ColorVisualizer(WHITE);
        new ColorVisualizer(GRAY);
        new ColorVisualizer(RED);
        new ColorVisualizer(GREEN);
        new ColorVisualizer(BLUE);
         */

        //weitere Farben zum Testen
        Color aliceBlue = new Color("#F0F8FF");
        Color chartreuse = new Color("#7FFF00");
        Color cadetBlue = new Color("#5F9EA0");
        Color hotPink = new Color("#FF69B4");
        Color navajoWhite = new Color("#778899");
        Color lightSlateGray = new Color("#FFDEAD");

        //Tests mit zusaetzlichen Farben aus der Farbtabelle
        System.out.println("-------------");
        System.out.println("Alice Blue");
        System.out.println("RGB value: " + aliceBlue.getRgb());
        System.out.println("Individual RGB values: " + aliceBlue.getRed() + " " + aliceBlue.getGreen() + " " + aliceBlue.getBlue());
        System.out.println("Hex value: " + aliceBlue.getHex());

        // Test der Komplementaerfarbe
        Color compAliceBlue = aliceBlue.complementaryColor();
        System.out.println("\nComplementary color");
        System.out.println("RGB value: " + compAliceBlue.getRgb());
        System.out.println("Individual RGB values: " + compAliceBlue.getRed() + " " + compAliceBlue.getGreen() + " " + compAliceBlue.getBlue());
        System.out.println("Hex value: " + compAliceBlue.getHex());

        System.out.println("-------------");
        System.out.println("Chartreuse");
        System.out.println("RGB value: " + chartreuse.getRgb());
        System.out.println("Individual RGB values: " + chartreuse.getRed() + " " + chartreuse.getGreen() + " " + chartreuse.getBlue());
        System.out.println("Hex value: " + chartreuse.getHex());

        Color compChartreuse = chartreuse.complementaryColor();
        System.out.println("\nComplementary color");
        System.out.println("RGB value: " + compChartreuse.getRgb());
        System.out.println("Individual RGB values: " + compChartreuse.getRed() + " " + compChartreuse.getGreen() + " " + compChartreuse.getBlue());
        System.out.println("Hex value: " + compChartreuse.getHex());

        System.out.println("-------------");
        System.out.println("Cadet Blue");
        System.out.println("RGB value: " + cadetBlue.getRgb());
        System.out.println("Individual RGB values: " + cadetBlue.getRed() + " " + cadetBlue.getGreen() + " " + cadetBlue.getBlue());
        System.out.println("Hex value: " + cadetBlue.getHex());

        Color compCadetBlue = cadetBlue.complementaryColor();
        System.out.println("\nComplementary color");
        System.out.println("RGB value: " + compCadetBlue.getRgb());
        System.out.println("Individual RGB values: " + compCadetBlue.getRed() + " " + compCadetBlue.getGreen() + " " + compCadetBlue.getBlue());
        System.out.println("Hex value: " + compCadetBlue.getHex());

        System.out.println("-------------");
        System.out.println("Hot Pink");
        System.out.println("RGB value: " + hotPink.getRgb());
        System.out.println("Individual RGB values: " + hotPink.getRed() + " " + hotPink.getGreen() + " " + hotPink.getBlue());
        System.out.println("Hex value: " + hotPink.getHex());

        Color compHotPink = hotPink.complementaryColor();
        System.out.println("\nComplementary color");
        System.out.println("RGB value: " + compHotPink.getRgb());
        System.out.println("Individual RGB values: " + compHotPink.getRed() + " " + compHotPink.getGreen() + " " + compHotPink.getBlue());
        System.out.println("Hex value: " + compHotPink.getHex());

        System.out.println("-------------");
        System.out.println("Navajo White");
        System.out.println("RGB value: " + navajoWhite.getRgb());
        System.out.println("Individual RGB values: " + navajoWhite.getRed() + " " + navajoWhite.getGreen() + " " + navajoWhite.getBlue());
        System.out.println("Hex value: " + navajoWhite.getHex());

        Color compNavajoWhite = navajoWhite.complementaryColor();
        System.out.println("\nComplementary color");
        System.out.println("RGB value: " + compNavajoWhite.getRgb());
        System.out.println("Individual RGB values: " + compNavajoWhite.getRed() + " " + compNavajoWhite.getGreen() + " " + compNavajoWhite.getBlue());
        System.out.println("Hex value: " + compNavajoWhite.getHex());

        System.out.println("-------------");
        System.out.println("Light Slate Gray");
        System.out.println("RGB value: " + lightSlateGray.getRgb());
        System.out.println("Individual RGB values: " + lightSlateGray.getRed() + " " + lightSlateGray.getGreen() + " " + lightSlateGray.getBlue());
        System.out.println("Hex value: " + lightSlateGray.getHex());

        Color compLightSlateGray = lightSlateGray.complementaryColor();
        System.out.println("\nComplementary color");
        System.out.println("RGB value: " + compLightSlateGray.getRgb());
        System.out.println("Individual RGB values: " + compLightSlateGray.getRed() + " " + compLightSlateGray.getGreen() + " " + compLightSlateGray.getBlue());
        System.out.println("Hex value: " + compLightSlateGray.getHex());

        //Test des Mischens von Farben
        Color mixedColor = aliceBlue.mixColor(chartreuse);

        System.out.println("-------------");
        System.out.println("Alice Blue + Chartreuse");
        System.out.println("RGB value: " + mixedColor.getRgb());
        System.out.println("Individual RBG values: " + mixedColor.getRed() + " " + mixedColor.getGreen() + " " + mixedColor.getBlue());
        System.out.println("Hex value: " + mixedColor.getHex());
    }

}
