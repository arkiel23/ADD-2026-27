package PR3_Persistir_objetos;

import java.io.EOFException;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.ObjectInputStream;

public class LectorJugadores {

    public static void main(String[] args) {

        File fichero = new File("Jugadores.dat");

        try (ObjectInputStream ois =
                     new ObjectInputStream(
                             new FileInputStream(fichero))) {

            while (true) {

                Jugador j = (Jugador) ois.readObject();

                System.out.println(
                        "Nombre: " + j.getNombre()
                        + " | Equipo: " + j.getEquipo()
                        + " | Edad: " + j.getEdad()
                        + " | Salario: " + j.getSalario());
            }

        } catch (EOFException e) {

            System.out.println("Fin del archivo");

        } catch (IOException | ClassNotFoundException e) {

            System.err.println("Error: " + e.getMessage());
        }
    }
}