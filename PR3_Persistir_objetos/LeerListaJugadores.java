package PR3_Persistir_objetos;

import java.io.FileInputStream;
import java.io.ObjectInputStream;
import java.util.ArrayList;

public class LeerListaJugadores {

    public static void main(String[] args) {

        try (ObjectInputStream ois =
                     new ObjectInputStream(
                             new FileInputStream("ListaJugadores.dat"))) {

            ArrayList<Jugador> jugadores =
                    (ArrayList<Jugador>) ois.readObject();

            for (Jugador j : jugadores) {

                System.out.println(
                        "Nombre: " + j.getNombre()
                        + " | Equipo: " + j.getEquipo()
                        + " | Edad: " + j.getEdad()
                        + " | Salario: " + j.getSalario());
            }

        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }
}