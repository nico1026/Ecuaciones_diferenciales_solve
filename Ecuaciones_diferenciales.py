import streamlit as st
from sympy import symbols, Function, dsolve, Eq, exp, sin, cos, latex, sympify, laplace_transform, inverse_laplace_transform

st.set_page_config(page_title="Ecuaciones diferenciales", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌌 ¿QUIERES SOLUCIONAR ECUACIONES DIFERENCIALES?")
st.write("Resuelve ecuaciones analíticamente, por Laplace o mediante métodos avanzados.")
# ---------------------------------------------------------------------
st.sidebar.header("🛠️ Paametros")
metodo_res = st.sidebar.selectbox("Método de Resolución", 
    ["Automático (dsolve)", "Transformada de Laplace", "Variables Separables"])

with st.sidebar.expander("📍 Condiciones Iniciales", expanded=True):
    aplicar_ics = st.checkbox("¿Usar condiciones iniciales?")
    val_y0 = st.number_input("y(0) =", value=0.0)
    val_yp0 = st.number_input("y'(0) =", value=0.0)

# --------------------------------------------------------------
st.subheader("1. Define tu Ecuación")
col_input, col_help = st.columns([2, 1])

with col_input:
    user_expr = st.text_input(
        "Escribe la expresión igualada a cero:", 
        value="diff(y(x), x, 2) + 3*diff(y(x), x) + 2*y(x) - exp(x)",
        help="Usa diff(y(x), x) para y'. Ejemplo: y'' + y = 0 -> diff(y(x), x, 2) + y(x)"
    )

with col_help:
    st.info("""
    **Sintaxis rápida:**
    - `diff(y(x), x)` → $y'$
    - `diff(y(x), x, 2)` → $y''$
    - `exp(x)` → $e^x$
    - `sin(x)`, `cos(x)`
    """)

# ------ solcuoioon matematica 
x = symbols('x')
y = Function('y')

try:
    lhs = sympify(user_expr)
    ecuacion = Eq(lhs, 0)

    st.divider()
    
    st.write("### Ecuación analisasadda:")
    st.latex(latex(ecuacion))
    if st.button("🚀 RESOLVER ECUACIÓN"):
        st.subheader("2. Resultado de la Solución")       
        ics = None
        if aplicar_ics:            
            ics = {y(0): val_y0, y(x).diff(x).subs(x, 0): val_yp0}        
        with st.spinner('Calculanndo...'):
            if metodo_res == "Automático (dsolve)":
                solucion = dsolve(ecuacion, y(x), ics=ics)
                
            elif metodo_res == "Transformada de Laplace":
                
                try:
                    solucion = dsolve(ecuacion, y(x), ics=ics, hint='lie_group') 
                except:
                    solucion = dsolve(ecuacion, y(x), ics=ics)

            st.success("¡Solución encontrada con éxito!")
            st.latex(latex(solucion))
            
            #### faltan las graficas 
            st.session_state['last_sol'] = solucion

except Exception as e:
    st.error(f"⚠️ Error en la expresión: {e}")
    st.warning("Recuerdaasd de escribir correctamente la sintaxxis de SymPy (ej. usar '*' para multiplicar)")

st.divider()
