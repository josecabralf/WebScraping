from config import ar_contactos


def escribirContacto(contacto):
    f = open(ar_contactos, 'a')
    f.write(contacto)
    f.close()
