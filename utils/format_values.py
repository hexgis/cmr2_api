# core/format_values.py (ou core/utils.py)
import locale
from datetime import datetime

# Configura a localidade para o formato brasileiro
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')  # Para formato brasileiro

# --- Formatação de Números ---


def format_percentage(value):
    if value is None:
        return None
    return f"{locale.format_string('%.6f', value, grouping=True)}%"


def format_number(value):
    """Formata números no padrão brasileiro: xx.xxx,xx (com 2 casas decimais)."""
    if value is None:
        return None
    return locale.format_string("%.2f", value, grouping=True)


def format_area(value):
    """Formata um valor de área com 3 casas decimais e separador de milhar."""
    if value is None:
        return None
    return locale.format_string("%.3f", value, grouping=True)

# --- Formatação de Geometrias ---


def format_coord(value):
    """Formata coordenadas com 6 casas decimais no padrão brasileiro."""
    if value is None:
        return None
    return locale.format_string("%.6f", value, grouping=True)

# --- Formatação de Datas ---


def format_date(value):
    """Formata uma data no padrão brasileiro: DD/MM/AAAA."""
    if value is None:
        return None
    if isinstance(value, str):
        # Se já for string, tenta converter para datetime
        try:
            # Ajuste o formato de entrada se necessário
            value = datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            return value  # Retorna como está se não for conversível
    return value.strftime('%d/%m/%Y')

# --- Funções específicas para áreas (podem ser usadas em serializers) ---


def get_cr_nu_area_ha(obj):
    """Formata o campo cr_nu_area_ha."""
    return format_area(obj.get('cr_nu_area_ha'))


def get_dg_nu_area_ha(obj):
    """Formata o campo dg_nu_area_ha."""
    return format_area(obj.get('dg_nu_area_ha'))


def get_dr_nu_area_ha(obj):
    """Formata o campo dr_nu_area_ha."""
    return format_area(obj.get('dr_nu_area_ha'))


def get_ff_nu_area_ha(obj):
    """Formata o campo ff_nu_area_ha."""
    return format_area(obj.get('ff_nu_area_ha'))


def get_total_nu_area_ha(obj):
    """Formata o campo total_nu_area_ha."""
    return format_area(obj.get('total_nu_area_ha'))
