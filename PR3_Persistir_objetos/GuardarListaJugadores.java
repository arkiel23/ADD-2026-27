package PR3_Persistir_objetos;

import java.io.FileOutputStream;
import java.io.ObjectOutputStream;
import java.util.ArrayList;

public class GuardarListaJugadores {

    public static void main(String[] args) {

        ArrayList<Jugador> jugadores = new ArrayList<>();

        jugadores.add(new Jugador("Pedri", "Barcelona", 22, 8500000));
        jugadores.add(new Jugador("Bellingham", "Real Madrid", 21, 9000000));
        jugadores.add(new Jugador("Lamine Yamal", "Barcelona", 18, 5000000));
        jugadores.add(new Jugador("Rodri", "Manchester City", 29, 11000000));
        jugadores.add(new Jugador("Mbappe", "Real Madrid", 26, 15000000));
        jugadores.add(new Jugador("Haaland", "Manchester City", 25, 14000000));

        try (ObjectOutputStream oos =
                     new ObjectOutputStream(
                             new FileOutputStream("ListaJugadores.dat"))) {

            oos.writeObject(jugadores);

            System.out.println("Lista guardada.");

        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }
}