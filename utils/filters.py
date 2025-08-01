import json
from flask import Blueprint

# Criar blueprint para filtros
filters_bp = Blueprint('filters', __name__)

@filters_bp.app_template_filter('from_json')
def from_json_filter(value):
    """Converte string JSON para objeto Python"""
    if value:
        try:
            return json.loads(value)
        except:
            return {}
    return {}

@filters_bp.app_template_filter('nl2br')
def nl2br_filter(value):
    """Converte quebras de linha em HTML"""
    if value:
        return value.replace('\n', '<br>')
    return value

@filters_bp.app_template_filter('format_time')
def format_time_filter(time_obj):
    """Formata objeto time para string HH:MM"""
    if time_obj:
        return time_obj.strftime('%H:%M')
    return ''

@filters_bp.app_template_filter('format_datetime')
def format_datetime_filter(datetime_obj):
    """Formata objeto datetime para string legível"""
    if datetime_obj:
        return datetime_obj.strftime('%d/%m/%Y %H:%M')
    return ''

@filters_bp.app_template_filter('truncate')
def truncate_filter(text, length=100, suffix='...'):
    """Trunca texto para um comprimento específico"""
    if text and len(text) > length:
        return text[:length] + suffix
    return text

@filters_bp.app_template_filter('status_badge')
def status_badge_filter(status):
    """Retorna classe CSS para badge de status"""
    status_classes = {
        'não_lida': 'badge-warning',
        'lida': 'badge-info',
        'respondida': 'badge-success',
        'ativo': 'badge-success',
        'inativo': 'badge-danger'
    }
    return status_classes.get(status, 'badge-secondary') 