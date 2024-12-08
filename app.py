import sympy as sp
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    num_variables, num_ecuaciones = 2, 2  # Valores predeterminados
    solucion = None
    error = None

    if request.method == 'POST':
        try:
            # Obtención de datos del formulario
            num_variables = int(request.form.get('num_variables', 2))
            num_ecuaciones = int(request.form.get('num_ecuaciones', 2))

            # Recolección de coeficientes y términos independientes
            coeficientes = []
            terminos = []

            for i in range(num_ecuaciones):
                fila = []
                for j in range(num_variables):
                    key = f'coef_{i}_{j}'
                    fila.append(float(request.form.get(key, 0)))
                coeficientes.append(fila)
                terminos.append(float(request.form.get(f'const_{i}', 0)))

            # Creación de las variables simbólicas
            variables = sp.symbols(f'x1:{num_variables + 1}')

            # Construcción de las ecuaciones simbólicas
            ecuaciones = [
                sum(coef * var for coef, var in zip(fila, variables)) - termino
                for fila, termino in zip(coeficientes, terminos)
            ]

            # Resolución de las ecuaciones
            solucion = sp.solve(ecuaciones, variables)

            # Redondear resultados a 3 decimales
            solucion = {var: round(float(val), 3) for var, val in solucion.items()}

        except Exception as e:
            error = f"Error: {str(e)}"

    return render_template(
        'index.html',
        num_variables=num_variables,
        num_ecuaciones=num_ecuaciones,
        solucion=solucion,
        error=error
    )

if __name__ == '__main__':
    app.run(debug=True)
