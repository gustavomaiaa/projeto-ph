# utils/validacoes.py

def validar_ph(valor):
    """
    Valida o valor de pH recebido.
    Retorna (True, float(ph)) se for válido.
    Retorna (False, "mensagem de erro") se for inválido.
    """
    try:
        ph = float(valor)  # Tenta converter para float
    except (ValueError, TypeError):
        return False, "O valor de pH deve ser um número."

    if ph < 0 or ph > 14:
        return False, "O valor de pH deve estar entre 0 e 14."

    return True, ph

def validar_email(email):
    if not email or '@' not in email:
        return False
    return True