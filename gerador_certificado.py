from PIL import Image, ImageDraw, ImageFont
import yagmail
from config import pass_gmail, user_gmail
import os


def enviar_email_com_certificado(nome, cpf, horas, email):
    cpf_formatado = formatar_cpf(cpf)
    imagem_certificado = criar_certificado(nome, cpf_formatado, horas)
    enviar_email(nome, email, imagem_certificado)


def formatar_cpf(cpf):
    cpf = ''.join(x for x in cpf if x.isdigit()).zfill(11)
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


def criar_certificado(nome, cpf, horas):
    imagem = Image.open('assets/certificado.png')

    texto1 = f'''Certificamos que {nome}, portador(a) do CPF {cpf},'''
    texto2 = f'''participou da SECCOM 2024 entre os dias 21 de novembro a 25 de novembro,'''
    texto3 = f'''totalizando {horas} horas de atividades.'''

    draw = ImageDraw.Draw(imagem)
    fonte = ImageFont.truetype('assets/arial.ttf', 35)

    # Centralizando os textos horizontalmente
    largura_texto1, _ = draw.textsize(texto1, font=fonte)
    largura_imagem, _ = imagem.size
    ponto_inicio_texto1 = (largura_imagem - largura_texto1) / 2

    largura_texto2, _ = draw.textsize(texto2, font=fonte)
    ponto_inicio_texto2 = (largura_imagem - largura_texto2) / 2

    largura_texto3, _ = draw.textsize(texto3, font=fonte)
    ponto_inicio_texto3 = (largura_imagem - largura_texto3) / 2

    # Definindo a cor da fonte como preto (0, 0, 0) e a altura dos textos
    draw.text((ponto_inicio_texto1, 710), texto1,
              font=fonte, fill=(0, 0, 0), align='center')
    draw.text((ponto_inicio_texto2, 750), texto2,
              font=fonte, fill=(0, 0, 0), align='center')
    draw.text((ponto_inicio_texto3, 790), texto3,
              font=fonte, fill=(0, 0, 0), align='center')

    imagem_certificado = f'{nome}_Certificado.png'
    imagem.save(imagem_certificado)
    return imagem_certificado


def enviar_email(nome, email, imagem_certificado):
    usuario = yagmail.SMTP(user=user_gmail, password=pass_gmail)

    assunto = 'Certificado de Participação - SECCOM'
    conteudo = f'Olá {nome},\n\nAqui está o seu certificado de participação da SECCOM 2023. \n\nAtenciosamente,\nOrganização da SECCOM'

    usuario.send(
        to=email,
        subject=assunto,
        contents=conteudo,
        attachments=imagem_certificado
    )

    print(f'Email enviado para {email} com sucesso!')

    os.remove(imagem_certificado)
    print(f"Certificado '{imagem_certificado}' excluído com sucesso.")
