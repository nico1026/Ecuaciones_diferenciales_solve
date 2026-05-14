import streamlit as st
from sympy import symbols, Function, dsolve, Eq, latex, sympify, lambdify, Degree
import numpy as np
import matplotlib.pyplot as plt


st.set_page_config(page_title="ecdi solve", layout="wide", page_icon="👨‍🔧")

st.title("👨‍🔧 Solucionador de Ecuaciones diferenciales")
st.markdown("Esta herramienta detectara el orden de tu ecuación.")

# 1. ENTRADA DE LA ECUACIÓN (Primero para saber el orden)
st.subheader("1. Definición de la Ecuación")
user_input = st.text_input(
    "Escribe la expresión (LHS = 0):", 
    value="diff(y(x), x, 2) + 5*diff(y(x), x) + 6*y(x)",
    help="Usa diff(y(x), x, n) para derivadas."
)

# Definición de símbolos base
x = symbols('x')
y = Function('y')

try:
    # Pre-análisis de la ecuación para detectar el orden
    expr_tmp = sympify(user_input)
    # Buscamos el orden máximo de derivación de y(x)
    derivadas = expr_tmp.atoms(Function)
    orden_max = 0
    for d in expr_tmp.atoms(symbols('Derivative')): # Busca términos de tipo derivada
        if d.expr == y(x):
            orden_max = max(orden_max, d.derivative_count)
    
    # 2. GENERACIÓN DINÁMICA DE INPUTS EN EL SIDEBAR
    st.sidebar.header("📍 Condiciones Iniciales")
    st.sidebar.write(f"Orden detectado: **{orden_max}**")
    
    ics_values = []
    if orden_max > 0:
        for i in range(orden_max):
            label = f"y{'’'*i}(0)" if i > 0 else "y(0)"
            val = st.sidebar.number_input(f"Valor para {label}:", value=0.0, key=f"dyn_ic_{i}")
            ics_values.append(val)
    
    # 3. PROCESAMIENTO Y RESOLUCIÓN
    ecuacion = Eq(expr_tmp, 0)
    st.write("### Ecuación Interpretada:")
    st.latex(latex(ecuacion))

    if st.button("🚀 RESOLVER Y GRAFICAR"):
        st.divider()
        
        # Construir el diccionario de condiciones iniciales
        condiciones_dict = {}
        for i, val in enumerate(ics_values):
            if i == 0:
                condiciones_dict[y(0)] = val
            else:
                condiciones_dict[y(x).diff(x, i).subs(x, 0)] = val

        with st.spinner("Calculando..."):
            solucion = dsolve(ecuacion, y(x), ics=condiciones_dict)
            
            col_sol, col_plt = st.columns(2)
            
            with col_sol:
                st.success("✅ Solución Analítica")
                st.latex(latex(solucion))
            
            with col_plt:
                st.success("📈 Comportamiento")
                try:
                    f_num = lambdify(x, solucion.rhs, modules=['numpy'])
                    x_vals = np.linspace(0, 10, 500)
                    y_vals = f_num(x_vals)
                    
                    if isinstance(y_vals, (int, float, np.float64)):
                        y_vals = np.full_like(x_vals, y_vals)

                    fig, ax = plt.subplots()
                    ax.plot(x_vals, y_vals, color='red', lw=2)
                    ax.set_xlabel("x")
                    ax.set_ylabel("y(x)")
                    ax.grid(True, alpha=0.3)
                    st.pyplot(fig)
                except Exception as e:
                    st.warning("La gráfica no pudo generarse (posibles valores complejos o infinitos).")

except Exception as e:
    st.error(f"Error al procesar la ecuación: {e}")
    st.info("Revisa que la sintaxis sea correcta: `diff(y(x), x, n)`")

st.divider()
st.caption("Miguel sotelo pinto | Ing. Mecánica ")

