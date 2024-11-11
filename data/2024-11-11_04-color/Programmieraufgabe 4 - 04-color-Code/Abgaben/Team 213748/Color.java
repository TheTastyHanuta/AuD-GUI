//Author, Student-number: Seyit Uzun, 23394725; Koray Hacibayramoglu, 23409691

public class Color {

    private int rgb;

    // Constructor for the direct transfer of the int representation of the color
    public Color(int rgb) {
        this.rgb = rgb;
    }

    // Constructor for passing the color values red, green and blue
    public Color(int red, int green, int blue) {
        if (!isValidColorValue(red) || !isValidColorValue(green) || !isValidColorValue(blue)) {
            System.err.println("Invalid color values! Values are set to interval limits.");
            red = clampColorValue(red);
            green = clampColorValue(green);
            blue = clampColorValue(blue);
        }
        this.rgb = (red << 16) | (green << 8) | blue;
    }

    // Default constructor for the color black
    public Color() {
        this.rgb = 0;
    }

    // Get-methode for rgb
    public int getRgb() {
        return rgb;
    }

    // Get-method for the color channels
    public int getRed() {
        return (rgb >> 16) & 0xFF;
    }

    public int getGreen() {
        return (rgb >> 8) & 0xFF;
    }

    public int getBlue() {
        return rgb & 0xFF;
    }

    // Method for converting to hexadecimal representation
    public String getHex() {
        return String.format("#%06X", rgb);
    }

    // Constructor for the hexadecimal representation of the color
    public Color(String hex) {
        hex = hex.replace("#", "");
        this.rgb = Integer.parseInt(hex, 16);
    }

    // Overwriting the toString() method
    @Override
    public String toString() {
        return getHex();
    }

    // Method for calculating the complementary color
    public Color complementaryColor() {
        int red = 255 - getRed();
        int green = 255 - getGreen();
        int blue = 255 - getBlue();
        return new Color(red, green, blue);
    }

    // Method for mixing colors
    public Color mixColor(Color color) {
        int red = (getRed() + color.getRed()) / 2;
        int green = (getGreen() + color.getGreen()) / 2;
        int blue = (getBlue() + color.getBlue()) / 2;
        return new Color(red, green, blue);
    }

    // Auxiliary method for checking valid color values
    private boolean isValidColorValue(int value) {
        return value >= 0 && value <= 255;
    }

    // Auxiliary method for limiting color values to the interval [0, 255]
    private int clampColorValue(int value) {
        return Math.max(0, Math.min(value, 255));
    }


    // Static constants for frequently used colors
    public static final Color BLACK = new Color(0, 0, 0);
    public static final Color WHITE = new Color(255, 255, 255);
    public static final Color GRAY = new Color(128, 128, 128);
    public static final Color RED = new Color(255, 0, 0);
    public static final Color GREEN = new Color(0, 255, 0);
    public static final Color BLUE = new Color(0, 0, 255);

    public static void main(String[] args) {
        Color turquoise = new Color("#40E0D0"); // Turquoise
        Color red = Color.RED;
        Color lightGreen = new Color("#90EE90"); // Light Green
        Color green = Color.GREEN;
        Color darkGreen = new Color("#006400"); // Dark Green
        Color peachPuff = new Color("#FFDAB9"); // PeachPuff
        Color blueViolet = new Color("#8A2BE2");
        Color whiteSmoke = new Color("#F5F5F5");
        Color powderBlue = new Color("#B0E0E6");
        Color gold = new Color("#FFD700");

        new ColorVisualizer(turquoise);
        new ColorVisualizer(red);
        new ColorVisualizer(lightGreen);
        new ColorVisualizer(green);
        new ColorVisualizer(darkGreen);
        new ColorVisualizer(peachPuff);
        new ColorVisualizer(blueViolet);
        new ColorVisualizer(whiteSmoke);
        new ColorVisualizer(powderBlue);
        new ColorVisualizer(gold);
    }
}


