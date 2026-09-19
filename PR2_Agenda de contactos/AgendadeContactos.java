import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.util.Scanner;

public class AgendadeContactos {
    public static void main(String[] args) {

        Scanner teclado = new Scanner(System.in);

        int opcion = 0;

        while (opcion != 4) {

            System.out.println("----- AGENDA -----");
            System.out.println("1. Anadir contacto");
            System.out.println("2. Listar contactos");
            System.out.println("3. Buscar contacto");
            System.out.println("4. Salir");

            System.out.print("Elige una opcion: ");
            opcion = teclado.nextInt();
            teclado.nextLine();

            if (opcion == 1) {

                System.out.print("Nombre: ");
                String nombre = teclado.nextLine();

                System.out.print("Telefono: ");
                String telefono = teclado.nextLine();

                System.out.print("Correo: ");
                String correo = teclado.nextLine();

                try {

                    FileWriter fw = new FileWriter("contactos.txt", true);

                    fw.write(nombre + ";" + telefono + ";" + correo + "\n");

                    fw.close();

                    System.out.println("Contacto anadido");

                } catch (Exception e) {

                    System.out.println("Error al escribir en el archivo: " + e.getMessage());

                }
            }

            else if (opcion == 2) {

                try {

                    BufferedReader br = new BufferedReader(new FileReader("contactos.txt"));

                    String linea;

                    while ((linea = br.readLine()) != null) {

                        String[] datos = linea.split(";");

                        System.out.println("[+] Nombre: " + datos[0]);
                        System.out.println("[+] Telefono: " + datos[1]);
                        System.out.println("[+] Correo: " + datos[2]);

                        System.out.println("--------------------");
                    }

                    br.close();

                } catch (Exception e) {

                    System.out.println("El archivo todavia no existe");

                }
            }

            else if (opcion == 3) {

                System.out.print("Escribe el nombre que quieres buscar: ");
                String buscar = teclado.nextLine();

                boolean encontrado = false;

                try {

                    BufferedReader br = new BufferedReader(new FileReader("contactos.txt"));

                    String linea;

                    while ((linea = br.readLine()) != null) {

                        String[] datos = linea.split(";");

                        if (datos[0].equalsIgnoreCase(buscar)) {

                            System.out.println("Contacto encontrado:");
                            System.out.println("[+] Nombre: " + datos[0]);
                            System.out.println("[+] Telefono: " + datos[1]);
                            System.out.println("[+] Correo: " + datos[2]);

                            encontrado = true;
                        }
                    }

                    br.close();

                    if (encontrado == false) {
                        System.out.println("No se ha encontrado el contacto");
                    }

                } catch (Exception e) {

                    System.out.println("El archivo todavia no existe");

                }
            }

            else if (opcion == 4) {

                System.out.println("Programa finalizado");

            }

            else {

                System.out.println("Opcion incorrecta");

            }
        }
    }
}