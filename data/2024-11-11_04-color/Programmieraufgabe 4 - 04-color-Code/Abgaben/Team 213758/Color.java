//Nabaa Al-Bayaty Matrikelnummer 23387859 und Gia-Vy Hoang Matrikelnummer:23412069

public class Color {
    private int rgb;
    private int red;
    private int green;
    private int blue;
    private int black;

    public static final Color BLACK = new Color(0, 0, 0);
    public static final Color WHITE = new Color(255, 255, 255);
    public static final Color GRAY = new Color(128, 128, 128);
    public static final Color RED = new Color(255, 0, 0);
    public static final Color GREEN = new Color(0, 255, 0);
    public static final Color BLUE = new Color(0, 0, 255);

    public Color(int rgb) {
        this.rgb = rgb;
    }


    public Color(int red, int green, int blue) {
        if ((red >= 0) && (red <= 255)) {
            this.red = red;
        } else {
            System.err.println("An error occured!");
            if (red < 0) {
                this.red = 0;
            }
            if (red > 255) {
                this.red = 255;
            }
        }

        if ((green >= 0) && (red <= 255)) {
            this.green = green;
        } else {
            System.err.println("An error occured!");
            if (green < 0) {
                this.green = 0;
            }
            if (green > 255) {
                this.green = 255;
            }
        }

        if ((blue >= 0) && (blue <= 255)) {
            this.blue = blue;
        } else {
            System.err.println("An error occured!");
            if (blue < 0) {
                this.green = 0;
            }
            if (blue > 255) {
                this.blue = 255;
            }
        }

        rgb = (red << 16) | (green << 8) | blue;
    }

    public Color() {
        this.rgb = 0;
    }

    public int getRgb() {
        return rgb;
    }

    public int getRed() {
        return (rgb >> 16) & 255;
    }

    public int getGreen() {
        return (rgb >> 8) & 255;
    }

    public int getBlue() {
        return rgb & 255;
    }

    public String getHex() {
        int rgb = getRgb();
        String hexString = Integer.toHexString(rgb).toUpperCase();

        return "#" + ("000000" + hexString).substring(hexString.length());
    }

    public Color(String hex) {
        hex = hex.replace("#", "");
        this.rgb = Integer.parseInt(hex, 16);
    }

    @Override
    public String toString() {
        return getHex();
    }

    public Color complementaryColor() {
        int redComp = 255 - getRed();
        int greenComp = 255 - getGreen();
        int blueComp = 255 - getBlue();

        return new Color(redComp, greenComp, blueComp);
    }

    public Color mixColor(Color color1, Color color2) {
        int rNeu = (color1.getRed() + color2.getRed()) / 2;
        int gNeu = (getGreen() + color2.getGreen()) / 2;
        int bNeu = (getBlue() + color2.getBlue()) / 2;

        return new Color(rNeu, gNeu, bNeu);
    }


    public static void main(String[] args) {
        Color color1 = new Color(255, 0, 0);
        Color color2 = new Color(434850);
        Color color3 = new Color();
        Color color4 = new Color("#8B0000");
        Color peachPuff = new Color(255, 218, 185);
        Color hotPink = new Color(255, 105, 180);
        Color lightBlue = new Color(173, 216, 230);
        Color rebeccaPurple = new Color("#663399");
        Color lavender = new Color("#E6E6FA");
        Color darkGreen = new Color("#006400");

        System.out.println("Color1: " + color1.getRgb() + " Red: " + color1.getRed() + " Green: " + color1.getGreen() + " Blue: " + color1.getBlue());
        System.out.println("Color2: " + color2.getRgb() + " Red: " + color2.getRed() + " Green: " + color2.getGreen() + " Blue: " + color2.getBlue());
        System.out.println("Color3: " + color3.getRgb() + " Red: " + color3.getRed() + " Green: " + color3.getGreen() + " Blue: " + color3.getBlue());
        System.out.println("Color4: " + color4.getRgb() + " Red: " + color4.getRed() + " Green: " + color4.getGreen() + " Blue: " + color4.getBlue());

        System.out.println("Color1 Hex: " + color1.getHex());
        System.out.println("Color2 Hex: " + color2.getHex());
        System.out.println("Color3 Hex: " + color3.getHex());
        System.out.println("Color4 Hex: " + color4.getHex());

        Color mixedColor = color1.mixColor(color1, color2);
        System.out.println("Mixed Color: " + mixedColor.getHex());

        Color complementaryColor = color1.complementaryColor();
        System.out.println("Complementary Code: " + complementaryColor.getHex());

        System.out.println("Black Hex: " + Color.BLACK.getHex());
        System.out.println("Gray Hex: " + Color.GRAY.getHex());
        System.out.println("Green Hex: " + Color.GREEN.getHex());
        System.out.println("White Hex: " + Color.WHITE.getHex());
        System.out.println("Red Hex: " + Color.RED.getHex());
        System.out.println("Blue Hex: " + Color.BLUE.getHex());

        //Tests ob alle Methoden funktionieren

        ColorVisualizer visualizer = new ColorVisualizer(complementaryColor);
        visualizer.getContentPane();

        ColorVisualizer visualizer2 = new ColorVisualizer(peachPuff);
        visualizer2.getContentPane();

        ColorVisualizer visualizer3 = new ColorVisualizer(mixedColor);
        visualizer3.getContentPane();

        ColorVisualizer visualizer4 = new ColorVisualizer(color1);
        visualizer4.getContentPane();

        ColorVisualizer visualizer5 = new ColorVisualizer(WHITE);
        visualizer5.getContentPane();

        // Test Aufgabe 13:
        ColorVisualizer visualizer6 = new ColorVisualizer(hotPink);
        visualizer6.getContentPane();

        ColorVisualizer visualizer7 = new ColorVisualizer(lightBlue);
        visualizer7.getContentPane();

        ColorVisualizer visualizer8 = new ColorVisualizer(rebeccaPurple);
        visualizer8.getContentPane();

        ColorVisualizer visualizer9 = new ColorVisualizer(lavender);
        visualizer9.getContentPane();

        Color mixedColor2 = lavender.mixColor(lavender, rebeccaPurple);
        ColorVisualizer visualizer10 = new ColorVisualizer(mixedColor2);
        visualizer10.getContentPane();

        Color complementaryColor2 = hotPink.complementaryColor();
        ColorVisualizer visualizer11 = new ColorVisualizer(complementaryColor2);
        visualizer11.getContentPane();

        ColorVisualizer visualizer12 = new ColorVisualizer(darkGreen);
        visualizer12.getContentPane();

        Color mixedColor3 = darkGreen.mixColor(darkGreen, WHITE);
        ColorVisualizer visualizer13 = new ColorVisualizer(mixedColor3);
        visualizer13.getContentPane();

        Color mixedcolor4 = darkGreen.mixColor(darkGreen, BLACK);
        ColorVisualizer visualizer14 = new ColorVisualizer(mixedcolor4);
        visualizer14.getContentPane();

    }
}
