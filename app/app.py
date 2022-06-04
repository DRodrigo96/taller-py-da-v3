

# app.py
# ==================================================
# requirements
from flask import Flask, render_template, request
import joblib
import pandas as pd
# common
import os
import traceback
# used defined
from modules.utils import km_bpoints
from modules.utils import BinEncoder
from modules.utils import getMainPoints
# --------------------------------------------------

# => parameters
with open(r'./items/final_model.pkl', 'rb') as bm:
    BEST_MODEL = joblib.load(bm)
with open(r'./items/model_cols.pkl', 'rb') as mc:
    MODEL_COLS = joblib.load(mc)

MAIN_P_PKL_PATH = './items/main_p.pkl'
DISTRITOS_CATEGORY_PKL_PATH = './items/distritos_category.pkl'
LL = ['latitud', 'longitud']

# => flask app
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('home.html')

@app.route('/predict', methods=['GET', 'POST'])
def home():
    try:
        # >> user input
        new_data = [
            request.form['PROVINCIA_'],
            int(request.form['IDDIST']),
            float(request.form['area_constr_m2']),
            float(request.form['area_total_m2']),
            int(request.form['nro_espacios']),
            int(request.form['antiguedad']),
            request.form['estado_de_inmueble_'],
            float(request.form['latitud']),
            float(request.form['longitud'])
        ]
        
        # >> backend transformations
        new_data_row = pd.DataFrame([new_data], columns=MODEL_COLS).set_index('IDDIST')
        new_data_row = getMainPoints(new_data_row, pkl_path=MAIN_P_PKL_PATH).reset_index()
        new_data_row['mp_m'] = km_bpoints(new_data_row, 'mp_m')
        new_data_row['mp_c'] = km_bpoints(new_data_row, 'mp_c')
        new_data_row['IDDIST'] = BinEncoder(new_data_row['IDDIST'], pkl_path=DISTRITOS_CATEGORY_PKL_PATH)
        new_data_row = new_data_row.drop(LL, axis=1)
        
        # >> model prediction
        result = int(BEST_MODEL.predict(new_data_row)[0])
    
    except:
        traceback.print_exc()
        result = 'ERROR'
    
    # > output window
    return render_template('results.html', data=result)

# => execute application
if __name__ == '__main__':
    
    # > localhost / Heroku
    app.run(debug=True)
    
    # > Docker
    # app.run(debug=False, host='0.0.0.0')
    
    # Heroku / Heroku containers
    # port = os.environ.get('PORT', 5000)
    # app.run(debug=False, host='0.0.0.0', port=port)
