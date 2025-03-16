# app.py
from flask import Flask, render_template, request, jsonify
from api.routes import api_blueprint
from core import ResearchEngine
import json

app = Flask(__name__)

# Register API blueprint
app.register_blueprint(api_blueprint, url_prefix='/api')

research_cache = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/research', methods=['GET', 'POST'])
def research_form():
    if request.method == 'POST':
        company_name = request.form.get('company_name')
        
        if not company_name:
            return jsonify({
                'error': 'Company name is required'
            }), 400
        
        if company_name in research_cache:
            return jsonify(research_cache[company_name])
        
        try:
            engine = ResearchEngine()
            results = engine.research_company(company_name)
            
            # Cache results
            research_cache[company_name] = results
            
            return jsonify(results)
        except Exception as e:
            return jsonify({
                'error': f'Research failed: {str(e)}'
            }), 500

    return render_template('research_form.html')

@app.route('/templates/research_form.html')
def research_form_template():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Company Research Agent</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 800px; margin: 0 auto; }
            input[type="text"] { padding: 8px; width: 300px; }
            button { padding: 8px 16px; background-color: #4CAF50; color: white; border: none; cursor: pointer; }
            #results { margin-top: 20px; white-space: pre-wrap; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Company Research Agent</h1>
            <p>Enter a company name to research:</p>
            
            <div>
                <input type="text" id="company_name" placeholder="Enter company name (e.g., Tesla)">
                <button onclick="researchCompany()">Research</button>
            </div>
            
            <div id="loading" style="display: none;">
                <p>Researching... this may take a moment.</p>
            </div>
            
            <div id="results"></div>
        </div>
        
        <script>
            function researchCompany() {
                const companyName = document.getElementById('company_name').value;
                if (!companyName) {
                    alert('Please enter a company name');
                    return;
                }
                
                document.getElementById('loading').style.display = 'block';
                document.getElementById('results').innerHTML = '';
                
                fetch('/api/research?company=' + encodeURIComponent(companyName))
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('loading').style.display = 'none';
                        document.getElementById('results').innerHTML = 
                            '<h2>Research Results for ' + companyName + '</h2>' +
                            '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                    })
                    .catch(error => {
                        document.getElementById('loading').style.display = 'none';
                        document.getElementById('results').innerHTML = 
                            '<h2>Error</h2><p>' + error + '</p>';
                    });
            }
        </script>
    </body>
    </html>
    """
    return html

@app.route('/templates/index.html')
def index_template():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Research Agent</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 800px; margin: 0 auto; }
            .btn { padding: 10px 20px; background-color: #4CAF50; color: white; 
                   text-decoration: none; display: inline-block; margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>AI Company Research Agent</h1>
            <p>This tool helps you gather comprehensive information about companies, including:</p>
            <ul>
                <li>Company overview and key executives</li>
                <li>Financial information and stock performance</li>
                <li>Recent news and social media sentiment</li>
                <li>Competitor analysis</li>
                <li>Growth trends and forecasts</li>
            </ul>
            
            <a href="/research" class="btn">Start Researching</a>
        </div>
    </body>
    </html>
    """
    return html

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)