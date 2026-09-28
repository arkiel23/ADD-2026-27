package PR3_Persistir_objetos;

import java.io.Serializable;

public class Jugador implements Serializable {

    private String nombre;
    private String equipo;
    private int edad;
    private double salario;

    public Jugador() {
        nombre = "";
        equipo = "";
        edad = 0;
        salario = 0;
    }

    public Jugador(String nombre, String equipo, int edad, double salario) {
        this.nombre = nombre;
        this.equipo = equipo;
        this.edad = edad;
        this.salario = salario;
    }

    public String getNombre() {
        return nombre;
    }

    public String getEquipo() {
        return equipo;
    }

    public int getEdad() {
        return edad;
    }

    public double getSalario() {
        return salario;
    }
}