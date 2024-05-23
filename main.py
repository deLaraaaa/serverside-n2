from flask import Flask, render_template, request, send_file, jsonify
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import time
from DataBase import *

app = Flask(__name__)


def run_fisher_yates():
    start_time = time.time()
    fisher_yates(50001)  # Assuming generating 50,000 random numbers
    end_time = time.time()
    return end_time - start_time


def run_merge_sort(numbers):
    start_time = time.time()
    numbers = fetch_numbers_from_database()
    merge_sort(numbers)
    end_time = time.time()
    return end_time - start_time


@app.route('/create_database')
def create_database_route():
    create_database()  # Call create_database from DataBase.py
    return "Database created successfully."


@app.route('/insert')
def insert():
    try:
        executions = []
        for i in range(3):
            random_numbers = fisher_yates(50000)
            execution_time_fisher_yates = run_fisher_yates()

            descricao_fisher_yates = "Vetor de 50.000 numeros randomizados usando o algoritmo Fisher-Yates"
            insert_database(descricao_fisher_yates, random_numbers)

            executions.append({
                'descricao_fisher_yates': descricao_fisher_yates,
                'execution_time_fisher_yates': execution_time_fisher_yates,
                'numeros_aleatorios_fisher_yates': random_numbers
            })
        return jsonify(executions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/sorted')
def sorted():
    try:
        executions = []

        chunks_of_numbers = fetch_numbers_from_database()

        for i, chunk in enumerate(chunks_of_numbers):
            execution_time_merge_sort = run_merge_sort(chunk)

            executions.append({
                'descricao_merge_sort': f"Vetor de 50.000 numeros ordenados usando o algoritmo Merge-Sort (Part {i+1})",
                'execution_time_merge_sort': execution_time_merge_sort,
                'numeros_ordenados_merge_sort': ", ".join(map(str, merge_sort(chunk)))
            })
        return jsonify(executions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/scatter', methods=['POST'])
def scatter():
    x = request.form['x']
    y = request.form['y']

    # Split input strings to lists
    x_values = x.split(',')
    y_values = list(map(float, y.split(',')))

    # Generate the bar plot
    plt.scatter(x_values, y_values)
    plt.xlabel('X Nomes')
    plt.ylabel('Y Valores')

    # Save plot to a bytes object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode plot bytes to base64 string
    plot_url = base64.b64encode(img.getvalue()).decode()

    # Close the plot to release resources
    plt.close()

    return render_template('scatter.html', plot_url=plot_url, x=x, y=y)


@app.route('/download-scatter', methods=['POST'])
def downloadScatter():
    x = request.form['x']
    y = request.form['y']

    # Split input strings to lists
    x_values = x.split(',')
    y_values = [float(val) for val in y.split(',')]

    # Generate the bar plot
    plt.scatter(x_values, y_values)
    plt.xlabel('X Nomes')
    plt.ylabel('Y Valores')

    # Save plot to a temporary file
    temp_file_path = "scatter_graph.png"
    plt.savefig(temp_file_path)

    # Close the plot to release resources
    plt.close()

    # Return the plot file in the response
    return send_file(temp_file_path, mimetype='image/png', as_attachment=True)


@app.route('/line', methods=['POST'])
def line():
    x = request.form['x']
    y = request.form['y']

    # Split input strings to lists
    x_values = x.split(',')
    y_values = list(map(float, y.split(',')))

    # Generate the line chart
    plt.plot(x_values, y_values)
    plt.xlabel('X Nomes')
    plt.ylabel('Y Valores')

    # Save plot to a bytes object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode plot bytes to base64 string
    plot_url = base64.b64encode(img.getvalue()).decode()

    # Close the plot to release resources
    plt.close()

    return render_template('line.html', plot_url=plot_url, x=x, y=y)


@app.route('/download-line', methods=['POST'])
def downloadLine():
    x = request.form['x']
    y = request.form['y']

    # Split input strings to lists
    x_values = x.split(',')
    y_values = [float(val) for val in y.split(',')]

    # Generate the line chart
    plt.plot(x_values, y_values)
    plt.xlabel('X Nomes')
    plt.ylabel('Y Valores')

    # Save plot to a temporary file
    temp_file_path = "line_graph.png"
    plt.savefig(temp_file_path)

    # Close the plot to release resources
    plt.close()

    # Return the plot file in the response
    return send_file(temp_file_path, mimetype='image/png', as_attachment=True)


@app.route('/bar', methods=['POST'])
def bar():
    x = request.form['x']
    y = request.form['y']

    # Split input strings to lists
    x_values = x.split(',')
    y_values = list(map(float, y.split(',')))

    # Generate the bar plot
    plt.bar(x_values, y_values)
    plt.xlabel('X Nomes')
    plt.ylabel('Y Valores')

    # Save plot to a bytes object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode plot bytes to base64 string
    plot_url = base64.b64encode(img.getvalue()).decode()

    # Close the plot to release resources
    plt.close()

    return render_template('bar.html', plot_url=plot_url, x=x, y=y)


@app.route('/download-bar', methods=['POST'])
def downloadBar():
    x = request.form['x']
    y = request.form['y']

    # Split input strings to lists
    x_values = x.split(',')
    y_values = [float(val) for val in y.split(',')]

    # Generate the bar plot
    plt.bar(x_values, y_values)
    plt.xlabel('X Nomes')
    plt.ylabel('Y Valores')

    # Save plot to a temporary file
    temp_file_path = "bar_graph.png"
    plt.savefig(temp_file_path)

    # Close the plot to release resources
    plt.close()

    # Return the plot file in the response
    return send_file(temp_file_path, mimetype='image/png', as_attachment=True)


@app.route('/bubble', methods=['POST'])
def bubble():
    x = request.form['x']
    y = request.form['y']
    sizes = request.form['y']

    # Split input strings to lists
    x_values = x.split(',')
    y_values = list(map(float, y.split(',')))
    sizes_values = list(map(float, sizes.split(',')))

    # Generate the bubble chart
    plt.scatter(x_values, y_values, s=sizes_values)
    plt.xlabel('X Nomes')
    plt.ylabel('Y Valores')

    # Save plot to a bytes object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode plot bytes to base64 string
    plot_url = base64.b64encode(img.getvalue()).decode()

    # Close the plot to release resources
    plt.close()

    return render_template('bubble.html', plot_url=plot_url, x=x, y=y, sizes=sizes)


@app.route('/download-bubble', methods=['POST'])
def downloadBubble():
    x = request.form['x']
    y = request.form['y']
    sizes = request.form['y']

    # Split input strings to lists
    x_values = x.split(',')
    y_values = [float(val) for val in y.split(',')]
    sizes_values = [float(val) for val in sizes.split(',')]

    # Generate the bubble chart
    plt.scatter(x_values, y_values, s=sizes_values)
    plt.xlabel('X Nomes')
    plt.ylabel('Y Valores')

    # Save plot to a temporary file
    temp_file_path = "bubble_graph.png"
    plt.savefig(temp_file_path)

    # Close the plot to release resources
    plt.close()

    # Return the plot file in the response
    return send_file(temp_file_path, mimetype='image/png', as_attachment=True)


@app.route('/dot', methods=['POST'])
def dot():
    x = request.form['x']
    y = request.form['y']

    # Split input strings to lists
    x_values = x.split(',')
    y_values = list(map(float, y.split(',')))

    # Convert x values to range(len(x_values)) for plotting
    x_indexes = range(len(x_values))

    # Generate the bar plot using individual lines
    for i, (x_val, y_val) in enumerate(zip(x_indexes, y_values)):
        plt.plot([x_val, x_val], [0, y_val], linestyle='dotted', linewidth=7)  # Plot dotted lines

    plt.xticks(x_indexes, x_values)  # Set x-axis labels

    plt.xlabel('X Nomes')
    plt.ylabel('Y Valores')

    # Save plot to a bytes object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode plot bytes to base64 string
    plot_url = base64.b64encode(img.getvalue()).decode()

    # Close the plot to release resources
    plt.close()

    return render_template('dot.html', plot_url=plot_url, x=x, y=y)


@app.route('/download-dot', methods=['POST'])
def download_dot():
    x = request.form['x']
    y = request.form['y']

    # Split input strings to lists
    x_values = x.split(',')
    y_values = list(map(float, y.split(',')))

    # Convert x values to range(len(x_values)) for plotting
    x_indexes = range(len(x_values))

    # Generate the bar plot using individual lines
    for i, (x_val, y_val) in enumerate(zip(x_indexes, y_values)):
        plt.plot([x_val, x_val], [0, y_val], linestyle='dotted', linewidth=10)

    # Save plot to a temporary file
    temp_file_path = "dot_plot.png"
    plt.savefig(temp_file_path)

    # Close the plot to release resources
    plt.close()

    # Return the plot file in the response
    return send_file(temp_file_path, mimetype='image/png', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
