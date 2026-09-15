import java.io.File;

public class Explorador_de_directorios {

    static int totalElementos = 0;
    static long sumaTamanios = 0;

    public static void main(String[] args) {

        if (args.length == 0) {
            System.out.println("Debes indicar una ruta como parámetro al ejecutar el programa.");
            return;
        }

        File raiz = new File(args[0]);

        if (!raiz.exists() || !raiz.isDirectory()) {
            System.out.println("Error: La ruta no existe o no es un directorio válido.");
            return;
        }

        System.out.println("Ruta válida: " + raiz.getAbsolutePath());
        System.out.println("---------------------------------------------");

        explorar(raiz);

        System.out.println("\n--- RESUMEN ---");
        System.out.println("Total de elementos: " + totalElementos);
        System.out.println("Suma de tamaños (archivos): " + sumaTamanios + " bytes");
    }

    static void explorar(File carpeta) {

        File[] elementos = carpeta.listFiles();

        if (elementos == null) {
            return;
        }

        for (File i : elementos) {

            String tipo, escribible;
            long tamano = 0;

            if (i.isDirectory()) {
                tipo = "Carpeta";
                explorar(i); 
            } else {
                tipo = "Archivo";
            }

            if (i.isFile()) {
                tamano = i.length();
            }

            escribible = i.canWrite() ? "Sí" : "No";

            System.out.println("Nombre: " + i.getName() + " | Tipo: " + tipo + " | Tamaño: " + tamano + " bytes | Escritura: " + escribible);

            totalElementos++;
            sumaTamanios += tamano;
        }
    }
}