//Annika Boehme 23361825, Lukas Aumann 23323010

public class Color {
    //The RGB values are stored in a single int value.
    private int rgb;

    //Public static constant Color objects
    public static final Color BLACK = new Color(0, 0, 0);
    public static final Color WHITE = new Color(255, 255, 255);
    public static final Color GRAY = new Color(128, 128, 128);
    public static final Color RED = new Color(255, 0, 0);
    public static final Color GREEN = new Color(0, 255, 0);
    public static final Color BLUE = new Color(0, 0, 255);

    //Constructor which includes the RGB value.
    public Color(int rgbValue) {
        this.rgb = rgbValue;
    }

    //Constructs a Color object with specified red, green, and blue values.
    public Color(int red, int green, int blue) {

        // Validate and set red, green, and blue values. If the values are outside of the 0-255 range, they are clamped to the nearest valid value and an error message is printed.
        if (red < 0) {
            red = 0;
            System.err.println("The number You have put in for red was to low\nRed has been set to 0");
        } else if (red > 255) {
            red = 255;
            System.err.println("The number You have put in for red was to high\nRed has been set to 255");
        }
        if (green < 0) {
            green = 0;
            System.err.println("The number You have put in for green was to low\nGreen has been set to 0");
        } else if (green > 255) {
            green = 255;
            System.err.println("The number You have put in for green was to high\nGreen has been set to 255");
        }
        if (blue < 0) {
            blue = 0;
            System.err.println("The number You have put in for blue was to low\nblue has been set to 0");
        } else if (blue > 255) {
            blue = 255;
            System.err.println("The number You have put in for blue was to high\nblue has been set to 255");
        }
        //Combine the RGB values into a single integer.
        this.rgb = (red << 16) | (green << 8) | blue;
    }

    //Default constructor that creates a black color.
    public Color() {
        this.rgb = 0; //Black.
    }

    //Getter-Methode for the RGB value.
    public int getRgb() {
        return this.rgb;
    }

    //Getter-Methode for the red color channel.
    public int getRed() {
        return (this.rgb >> 16) & 0xFF; //Shifts the red bits to the right and isolates the last 8 bits.
    }

    //Getter-Methode for the green color channel.
    public int getGreen() {
        return (this.rgb >> 8) & 0xFF; //Shifts the green bits to the right and isolates the last 8 bits.
    }

    //Getter-Methode for the blue color channel.
    public int getBlue() {
        return this.rgb & 0xFF; //Isolates the last 8 bits.
    }

    //Getter-Methode for the hex value.
    public String getHex() {
        //Extracting the red, green, and blue values.
        int red = getRed();
        int green = getGreen();
        int blue = getBlue();

        //Converting the values to hexadecimal.
        String hexRed = Integer.toHexString(red);
        String hexGreen = Integer.toHexString(green);
        String hexBlue = Integer.toHexString(blue);

        //Ensuring each component is two digits.
        hexRed = hexRed.length() == 1 ? "0" + hexRed : hexRed;
        hexGreen = hexGreen.length() == 1 ? "0" + hexGreen : hexGreen;
        hexBlue = hexBlue.length() == 1 ? "0" + hexBlue : hexBlue;

        //Returning the hex string.
        return "#" + hexRed.toUpperCase() + hexGreen.toUpperCase() + hexBlue.toUpperCase();
    }

    //Additional constructor that accepts a hex string with a '#' prefix.
    public Color(String hex) {
        hex = hex.replace("#", ""); //Remove the '#' prefix.
        this.rgb = Integer.parseInt(hex, 16); //Convert hex string to an integer.
    }

    //Method to create the complementary color.
    public Color complementaryColor() {

        //Calculate the complementary colors for each color channel
        int compRed = 255 - this.getRed();
        int compGreen = 255 - this.getGreen();
        int compBlue = 255 - this.getBlue();

        //Create and return a new Color object with the complementary values
        return new Color(compRed, compGreen, compBlue);
    }

    //Method to mix two colors.
    public Color mixColor(Color otherColor) {

        // Mitteln der Farbkan?le der aktuellen und der ?bergebenen Farbe
        int mixedRed = (this.getRed() + otherColor.getRed()) / 2;
        int mixedGreen = (this.getGreen() + otherColor.getGreen()) / 2;
        int mixedBlue = (this.getBlue() + otherColor.getBlue()) / 2;

        //Return a new Color object with the mixed values.
        return new Color(mixedRed, mixedGreen, mixedBlue);
    }

    //Overriding the toString method.
    @Override
    public String toString() {
        return getHex();
    }


    //Implementation of the main method.
    public static void main(String[] args) {

        //Test cases for the constructors.
        Color black = new Color(); //Black.
        Color white = new Color(255, 255, 255); //White.
        Color red = new Color(255, 0, 0); //Red.
        Color green = new Color(0, 255, 0); //Green.
        Color blue = new Color(0, 0, 255); //Blue.
        //Color invalidColor = new Color(-1, 256, 500); //Invalid color.

        //Output of the constructor test cases.
        System.out.println("Black (rgb): " + black.getRgb()); //Output: 0.
        System.out.println("White (rgb): " + white.getRgb()); //Output: 16777215.
        System.out.println("Red (rgb): " + red.getRgb()); //Output: 16711680.
        System.out.println("Green (rgb): " + green.getRgb()); //Output: 65280.
        System.out.println("Blue (rgb): " + blue.getRgb()); //Output: 255.
        //System.out.println("Invalid Color (rgb): " + invalidColor.getRgb()); //Output: Correction and error messages in stderr.

        //PeachPuff as a hexadecimal value.
        //int peachPuffRgb = 0xFFDAB9;
        //Color peachPuff = new Color(peachPuffRgb);
        Color peachPuff = new Color(0xFFDAB9); //Customization for the ColorVisualizer.
        //Output of the hexadecimal value of PeachPuff.
        System.out.println("PeachPuff Hex-Value: " + peachPuff.getHex());

        //Visualizing the colors with the ColorVisualizer class.
        ColorVisualizer visualizerBlack = new ColorVisualizer(black);
        ColorVisualizer visualizerWhite = new ColorVisualizer(white);
        ColorVisualizer visualizerRed = new ColorVisualizer(red);
        ColorVisualizer visualizerGreen = new ColorVisualizer(green);
        ColorVisualizer visualizerBlue = new ColorVisualizer(blue);
        ColorVisualizer visualizerPeachPuff = new ColorVisualizer(peachPuff);

        //Additional test colors.
        Color cyan = new Color("#00FFFF"); // Cyan.
        Color aqua = new Color("#7FFFD4"); // Aqua.
        Color gold = new Color("#FFD700"); // Gold.
        Color magenta = new Color("#FF00FF"); // Magenta.

        //Complementary color.
        String colorHex = "#006400";
        Color color = new Color(colorHex);

        //Call, output and visualizing the complementaryColor method.
        Color complementary = color.complementaryColor();
        System.out.println("The complementary color of" + colorHex + " is " + complementary.getHex());
        ColorVisualizer visualizerComplementary = new ColorVisualizer(complementary);

        //Testing complementaryColor method.
        Color complementaryCyan = cyan.complementaryColor();
        Color complementaryAqua = aqua.complementaryColor();
        Color complementaryGold = gold.complementaryColor();
        Color complementaryMagenta = magenta.complementaryColor();
        System.out.println("Cyan Complementary color (rgb): " + complementaryCyan.getRgb());
        System.out.println("Aqua Complementary color (rgb): " + complementaryAqua.getRgb());
        System.out.println("Gold Complementary color (rgb): " + complementaryGold.getRgb());
        System.out.println("Magenta Complementary color (rgb): " + complementaryMagenta.getRgb());

        //Testing mixColor method.
        Color mixedColor1 = cyan.mixColor(aqua);
        Color mixedColor2 = gold.mixColor(magenta);

        System.out.println("Mixed-Color 1 (rgb): " + mixedColor1.getRgb());
        System.out.println("Mixed-Color 2 (rgb): " + mixedColor2.getRgb());

        //Test cases for the complementaryColor method.
        Color colorFromHex = new Color("#FFA000");
        //Output of the complementaryColor method.
        System.out.println("RGB-Value of color #FFA000: " + colorFromHex.getRgb());
        System.out.println("Hex-Value of color #FFA000: " + colorFromHex.getHex());
        //Visualizing the complementary color.
        ColorVisualizer visualizer = new ColorVisualizer(colorFromHex);

        //Testing of the toString method.
        //Color color = new Color("#FFA000");
        //System.out.println("The toString() method returns: " + color.toString());

        //Testing of the mixColor method.
        Color color1 = new Color(255, 0, 0); //Red.
        Color color2 = new Color(0, 0, 255); //Blue.
        Color mixedColor = color1.mixColor(color2); //Purple.
        System.out.println("Mixed Color (rgb): " + mixedColor.getRgb() + ", Hex: " + mixedColor.getHex());
        //Visualizing the mixed color.
        ColorVisualizer visualizerMixed = new ColorVisualizer(mixedColor);
    }

}
