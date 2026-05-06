def aplicar_mascara_cpf(evento):
    """Aplica máscara 000.000.000-00 enquanto o usuário digita"""
    # Obtém apenas os números digitados
    texto_numerico = ''.join(filter(str.isdigit, evento.widget.get()))
    cpf_formatado = ""
    
    for indice, caractere in enumerate(texto_numerico):
        if indice == 3 or indice == 6: 
            cpf_formatado += "."
        elif indice == 9: 
            cpf_formatado += "-"
        cpf_formatado += caractere
        
    evento.widget.delete(0, "end")
    evento.widget.insert(0, cpf_formatado[:14])

def aplicar_mascara_tel(evento):
    """Aplica máscara (00) 00000-0000 enquanto o usuário digita"""
    # Obtém apenas os números digitados
    texto_numerico = ''.join(filter(str.isdigit, evento.widget.get()))
    tel_formatado = ""
    
    for indice, caractere in enumerate(texto_numerico):
        if indice == 0: 
            tel_formatado += "("
        elif indice == 2: 
            tel_formatado += ") "
        elif indice == 7: 
            tel_formatado += "-"
        tel_formatado += caractere
        
    evento.widget.delete(0, "end")
    evento.widget.insert(0, tel_formatado[:15])

def formatar_cpf(valor_cpf):
    """Formata uma string de números vinda do banco para 000.000.000-00"""
    numeros = ''.join(filter(str.isdigit, str(valor_cpf)))
    if len(numeros) == 11:
        return f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}"
    return numeros

def formatar_telefone(valor_tel):
    """Formata números do banco para (00) 00000-0000 ou (00) 0000-0000"""
    numeros = ''.join(filter(str.isdigit, str(valor_tel)))
    if len(numeros) == 11: 
        return f"({numeros[:2]}) {numeros[2:7]}-{numeros[7:]}"
    elif len(numeros) == 10: 
        return f"({numeros[:2]}) {numeros[2:6]}-{numeros[6:]}"
    return numeros