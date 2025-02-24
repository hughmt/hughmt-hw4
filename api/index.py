from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <h1>County Health Data API</h1>
    <p>This is a POST-only API endpoint. To use it, send a POST request to <code>/county_data</code> with JSON data.</p>
    <p>Example using curl:</p>
    <pre>
    curl -H 'Content-Type: application/json' \
         -d '{"zip":"02138","measure_name":"Adult obesity"}' \
         http://localhost:5000/county_data
    </pre>
    <p>Valid measure_name values:</p>
    <ul>
    ''' + ''.join(f'<li>{measure}</li>' for measure in VALID_MEASURES) + '''
    </ul>
    '''


# Valid measure names
VALID_MEASURES = {
    "Violent crime rate",
    "Unemployment",
    "Children in poverty",
    "Diabetic screening",
    "Mammography screening",
    "Preventable hospital stays",
    "Uninsured",
    "Sexually transmitted infections",
    "Physical inactivity",
    "Adult obesity",
    "Premature Death",
    "Daily fine particulate matter"
}

def get_db_connection():
    """Create a database connection"""
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/county_data', methods=['POST'])
def county_data():
    # Check content type
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    
    data = request.get_json()
    
    # Check for teapot easter egg
    if data.get('coffee') == 'teapot':
        return "I'm a teapot", 418
    
    # Validate required fields
    if 'zip' not in data or 'measure_name' not in data:
        return jsonify({"error": "Both zip and measure_name are required"}), 400
    
    zip_code = data['zip']
    measure_name = data['measure_name']
    
    # Validate zip code format
    if not (zip_code.isdigit() and len(zip_code) == 5):
        return jsonify({"error": "Invalid zip code format"}), 400
    
    # Validate measure name
    if measure_name not in VALID_MEASURES:
        return jsonify({"error": "Invalid measure_name"}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # First get the county info for the zip code
        cursor.execute("""
            SELECT county, state_abbreviation 
            FROM zip_county 
            WHERE zip = ?
        """, (zip_code,))
        
        county_info = cursor.fetchone()
        if not county_info:
            return jsonify({"error": "Zip code not found"}), 404
        
        county_name = county_info['county']
        state = county_info['state_abbreviation']
        
        # Now get the health data for that county
        cursor.execute("""
            SELECT *
            FROM county_health_rankings
            WHERE county = ? 
            AND state = ? 
            AND measure_name = ?
            ORDER BY year_span DESC
        """, (county_name, state, measure_name))
        
        # Convert rows to list of dicts
        results = []
        for row in cursor.fetchall():
            results.append({key: row[key] for key in row.keys()})
        
        conn.close()
        
        if not results:
            return jsonify({"error": "No data found for the specified criteria"}), 404
            
        return jsonify(results)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
