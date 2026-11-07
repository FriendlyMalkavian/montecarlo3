from flask import Flask, render_template, request
from montecarlo import validate_inputs, build_plot

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    img_b64 = None
    errors = []
    n_val = p_val = ch_val = ''

    if request.method == 'POST':
        n_val = request.form.get('n', '')
        p_val = request.form.get('p', '')
        ch_val = request.form.get('ch', '')

        n, p, ch, errors = validate_inputs(n_val, p_val, ch_val)

        if not errors:
            img_b64 = build_plot(n, p, ch)

    return render_template('index.html',
                           img_b64=img_b64,
                           errors=errors,
                           n_val=n_val,
                           p_val=p_val,
                           ch_val=ch_val)


if __name__ == '__main__':
    app.run(debug=True)