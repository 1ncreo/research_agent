# api/routes.py
from flask import Blueprint, request, jsonify
from core import ResearchEngine

api_blueprint = Blueprint('api', __name__)
research_engine = ResearchEngine()

@api_blueprint.route('/research', methods=['GET'])
def research_company():
    company_name = request.args.get('company')
    
    if not company_name:
        return jsonify({
            'error': 'Missing company name parameter'
        }), 400
    
    try:
        results = research_engine.research_company(company_name)
        return jsonify(results)
    except Exception as e:
        return jsonify({
            'error': f'Research failed: {str(e)}'
        }), 500

@api_blueprint.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok',
        'service': 'company-research-agent'
    })