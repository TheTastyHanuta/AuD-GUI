import java.util.HashMap;
//Name: Till Bessermann, Matrikelnummer: 23303124
//Name: Hamza Jaouadi, Matrikelnummer: 23414609

public class Color {

    //Variablendeklaration
    private int rgb;
    public static final Color GRAY = new Color(128, 128, 128);
    public static final Color WHITE = new Color(255, 255, 255);
    public static final Color BLACK = new Color(0, 0, 0);
    public static final Color RED = new Color (255, 0,0);
    public static final Color BLUE = new Color (0, 0, 255);
    public static final Color GREEN = new Color (0, 255, 0);
    public Color (int rgb) {

        this.rgb = rgb;
    }

    //Konstruktor mit drei ?bergabeparametern
    public Color (int red, int green, int blue) {

        if (0 > red) {
            System.out.println("Error! Value out of bounds!");
            red = 0;
        } else if (255 < red) {
            System.out.println("Error! Value out of bounds!");
            red = 255;
        } else if (0 > green) {
            System.out.println("Error! Value out of bounds!");
            green = 0;
        } else if (255 < green) {
            System.out.println("Error! Value out of bounds!");
            green = 255;
        } else if (0 > blue) {
            System.out.println("Error! Value out of bounds!");
            blue = 0;
        } else if (255 < blue) {
            System.out.println("Error! Value out of bounds!");
            blue = 255;
        }

        this.rgb = (red << 16) | (green << 8) | blue;
    }

    //Konstruktor ohne ?bergabeparameter
    public Color () {

        this.rgb = 0;
    }

    //Konstruktor mit String als ?bergabeparameter
    public Color (String hex) {

        String hexa = hex.substring(1);
        this.rgb = Integer.parseInt(hexa, 16);
        System.out.println(rgb);
    }

    public int getRgb() {

       return rgb;
    }

    public int getRed() {

        int red = rgb >> 16 ;
        return red;
    }

    public int getGreen() {

        int green = rgb >> 8 & 0xFF;
        return green;                         //nur die unteren 8 bits werden beruecksichtigt, die oberen werden zu 0
    }

    public int getBlue() {

        int blue = rgb & 0xFF;
        return blue;
    }

    public String getHex() {

        return "#" + String.format("%06X", rgb);
    }

    @Override
    public String toString() {

        return getHex();
    }

    //Methode f?r die Komplementaerfarbe
    public Color complementaryColor () {

        Color complementColor = new Color(255 - getRed(), 255 - getGreen(), 255 - getBlue());
        return complementColor;
    }

    //Methode zum Farbenmischen
    public Color mixColor (Color color) {

        int rneu = (this.getRed() + color.getRed()) / 2;
        int gneu = (this.getGreen() + color.getGreen()) / 2;
        int bneu = (this.getBlue() + color.getBlue()) / 2;
        Color mixedColor = new Color(rneu, gneu, bneu);
        return mixedColor;
    }

    public static void main(String[] args) {

        //Farbobjekte
        Color deepSkyBlue = new Color("#00BFFF");
        Color orangeRed = new Color("#FF4500");
        Color turquoise = new Color("#40E0D0");
        Color olive = new Color("#808000");
        Color peachPuff = new Color("#FFDAB9");
        Color orange = new Color("#FFA500");

        //Datenausgabe der Farben
        System.out.println("Red rate of DeepSkyBlue: " + deepSkyBlue.getRed());
        System.out.println("Green rate of DeepSkyBlue: " + deepSkyBlue.getGreen());
        System.out.println("Blue rate of DeepSkyBlue: " + deepSkyBlue.getBlue());
        System.out.println("Hexadecimal of DeepSkyBlue: " + deepSkyBlue.getHex());
        System.out.println("Hexadecimal of PeachPuff: " + peachPuff.getHex());

        //Visualisierungsobjekte
        ColorVisualizer deepSkyBlueVisual = new ColorVisualizer(deepSkyBlue);
        ColorVisualizer orangeRedVisual = new ColorVisualizer(orangeRed);
        ColorVisualizer turquoiseVisual = new ColorVisualizer(turquoise);

        //Visualisierung der Komplementaerfarbe
        ColorVisualizer deepSkyBlueComplement = new ColorVisualizer(deepSkyBlue.complementaryColor());
        ColorVisualizer orangeRedComplement = new ColorVisualizer(orangeRed.complementaryColor());

        //Visualisierung der Mischfarbe
        ColorVisualizer deepSkyBlueMixed = new ColorVisualizer(deepSkyBlue.mixColor(WHITE));
        ColorVisualizer oliveMixed = new ColorVisualizer(olive.mixColor(GRAY));
    }
}
