import streamlit as st
from sympy import symbols, Function, dsolve, Eq, latex, sympify, lambdify, Derivative
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

st.set_page_config(page_title="ECDI", layout="wide", page_icon="👨‍🔧")

st.title("👨‍🔧 SOLUCIONADOR DE ECUACIONES DIFERENCIALES")
st.markdown("Esta herramienta detecta el orden de tu ecuación.")
with st.expander("📖 Guía de como escribir una ecuación"):
    st.markdown("""
    Para que el motor matemático entienda tu ecuación, usa las siguientes reglas:
    
    *   **Función Principal:** Siempre escribe la función como **`y(x)`**.
    *   **Derivadas:** 
        *   $y'$ → `diff(y(x), x)`
        *   $y''$ → `diff(y(x), x, 2)`
        *   $y^{(n)}$ → `diff(y(x), x, n)`
    *   **Operaciones:**
        *   Multiplicación: Usa siempre `*` (ejemplo: `5*y(x)` en lugar de `5y`).
        *   Potencias: Usa `**` (ejemplo: `x**2`).
    *   **Funciones Comunes:**
        *   Exponencial: `exp(x)`
        *   Trigonométricas: `sin(x)`, `cos(x)`, `tan(x)`
        *   Logaritmo: `log(x)` (es el logaritmo natural).
    
    **Ejemplo de una ecuación:**
    `diff(y(x), x, 2) + 3*diff(y(x), x) + 2*y(x) - sin(x)`
    """)


st.subheader("1. Definición de la Ecuación")
user_input = st.text_input(
    "Escribe la expresión, RECUERDA IGU8ALARLA A 0:", 
    value="diff(y(x), x, 2) + 5*diff(y(x), x) + 6*y(x)",
    help="Usa diff(y(x), x, n) para derivadas. Ejemplo: y'' + y = 0 es diff(y(x), x, 2) + y(x)"
)
x = symbols('x')
y = Function('y')

try:
   
    expr_tmp = sympify(user_input)    

    derivadas = expr_tmp.atoms(Derivative)
    orden_max = 0
    for d in derivadas:
        if d.expr == y(x):            
            orden_max = max(orden_max, len(d.variables))
    
    
    st.sidebar.header("📍 Condiciones Iniciales")
    st.sidebar.write(f"Orden detectado: **{orden_max}**")
    
    ics_values = []
    if orden_max > 0:
        for i in range(orden_max):            
            label = f"y{'’'*i}(0)" if i > 0 else "y(0)"
            val = st.sidebar.number_input(f"Valor para {label}:", value=0.0, key=f"dyn_ic_{i}")
            ics_values.append(val)
    
   
    ecuacion = Eq(expr_tmp, 0)
    st.write("### Ecuación Interpretada:")
    st.latex(latex(ecuacion))

  
    if st.button("RESOLVER Y GRAFICAR"):
        st.divider()
        
    
        condiciones_dict = {}
        for i, val in enumerate(ics_values):
            if i == 0:
                condiciones_dict[y(0)] = val
            else:
                condiciones_dict[y(x).diff(x, i).subs(x, 0)] = val

        with st.spinner("Calculando solución "):
            solucion = dsolve(ecuacion, y(x), ics=condiciones_dict)
            
            col_sol, col_plt = st.columns(2)
            
            with col_sol:
                st.success("✅ Solución Analítica")
                st.latex(latex(solucion))
            
            with col_plt:
                st.success("📈 Comportamiento Gráfico")
                try:                    
                    f_num = lambdify(x, solucion.rhs, modules=['numpy'])
                    x_vals = np.linspace(0, 10, 500)
                    y_vals = f_num(x_vals)
                    
                    if isinstance(y_vals, (int, float, np.float64)):
                        y_vals = np.full_like(x_vals, y_vals)

                    fig, ax = plt.subplots()
                    ax.plot(x_vals, y_vals, color='#D32F2F', lw=2)
                    ax.set_xlabel("x")
                    ax.set_ylabel("y(x)")
                    ax.grid(True, alpha=0.3, linestyle='--')
                    st.pyplot(fig)
                except Exception:
                    st.warning("La gráfica no pudo generarse (posiblemente por valores complejos o falta de condiciones).")

except Exception as e:
    st.error(f"Error al procesar la ecuación: {e}")
    st.info("Asegúrate de usar la sintaxis correcta, por ejemplo: `diff(y(x), x, 2)`")

st.divider()
st.subheader("👥 Equipo de Trabajo")

fila1_col1, fila1_col2, fila1_col3 = st.columns(3)

with fila1_col1:
    st.image("imagenes/migue.jpeg", use_container_width=True)
    st.markdown("<center><b>Miguel Angel Sotelo Pinto</b><br>Ing. Mecánica</center>", unsafe_allow_html=True)

with fila1_col2:
    st.image("imagenes/dilan.jpeg", use_container_width=True)
    st.markdown("<center><b>Dilan Orlando Arguello Cartagena</b><br>Ing. Mecánica</center>", unsafe_allow_html=True)

with fila1_col3:
    st.image("imagenes/edwin.jpeg", use_container_width=True)
    st.markdown("<center><b>Edwin Alfredo Blanco Puentes</b><br>Ing. Electrónica</center>", unsafe_allow_html=True)

st.write("") # Espacio vertical de separación entre filas

fila2_col1, fila2_col2, fila2_col3 = st.columns(3)

with fila2_col1:
    st.image("imagenes/Lisseth.jpeg", use_container_width=True)
    st.markdown("<center><b>Lisseth Maryuri Peña Acosta</b><br>Ing. Industrial</center>", unsafe_allow_html=True)

with fila2_col2:
    st.image("imagenes/brandon.jpeg", use_container_width=True)
    st.markdown("<center><b>Brandon Stiben Pardo Sánchez</b><br>Ing. Mecánica</center>", unsafe_allow_html=True)

with fila2_col3:
    st.image("imagenes/brayan.jpeg", use_container_width=True)
    st.markdown("<center><b>Brayan Steven Silva Hernández</b><br>Ing. Mecánica</center>", unsafe_allow_html=True)
