package PR3_Persistir_objetos;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectOutputStream;

public class GeneradorJugadores {

    public static void main(String[] args) {

        String[] nombres = {
            "Pedri",
            "Bellingham",
            "Lamine Yamal",
            "Rodri",
            "Mbappe",
            "Haaland"
        };

        String[] equipos = {
            "Barcelona",
            "Real Madrid",
            "Barcelona",
            "Manchester City",
            "Real Madrid",
            "Manchester City"
        };

        int[] edades = {22, 21, 18, 29, 26, 25};

        double[] salarios = {
            8500000,
            9000000,
            5000000,
            11000000,
            15000000,
            14000000
        };

        File fichero = new File("Jugadores.dat");

        try (ObjectOutputStream oos =
                     new ObjectOutputStream(
                             new FileOutputStream(fichero))) {

            for (int i = 0; i < nombres.length; i++) {

                Jugador jugador =
                        new Jugador(
                                nombres[i],
                                equipos[i],
                                edades[i],
                                salarios[i]);

                oos.writeObject(jugador);
            }

            System.out.println("Jugadores guardados correctamente.");

        } catch (IOException e) {
            System.err.println("Error: " + e.getMessage());
        }
    }
}