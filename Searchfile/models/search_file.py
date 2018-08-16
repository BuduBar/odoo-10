# -*- coding: utf-8 -*-

import os
import sys
import logging

from odoo import api, fields, models, tools, conf
from odoo.exceptions import Warning

reload(sys)
sys.setdefaultencoding("utf-8")
_logger = logging.getLogger(__name__)

class SearchFileLocation(models.TransientModel):
    _name = 'search.file.location'

    nameFile = fields.Char(string="A Buscar", help="Campo para introducir el nombre del archivo a buscar")
    extension = fields.Selection([('py','.py'),('xml', '.xml')], "Extencion a Buscar")

    @api.one
    def button_searchFile(self):
        """ Esta funcion recibe dos parametros - un dato tipo char y un dato tipo Selection
            el dato tipo char busca una ocurrencia archivo por archivo hasta encontrarla,
            pero solo sera buscado en los archivos con la extension ingresada en el campo Selection.
        """
        path = conf.addons_paths
        data = self.nameFile
        formato = self.extension

        #Lista vacia para incluir los ficheros
        lstFiles = []

        #Lista con todos los ficheros del directorio:
        lstDir = os.walk(path[0])   #os.walk()Lista directorios y ficheros

        if not data:
            raise Warning('Introduce Algun Dato')

        #Checamos que el texto introducido tenga extencion, si tiene buscamos un archivo.
        #si no tiene buscamos el texto dentro de los archivos
        if '.py' in data or '.xml' in data:
            for files in lstDir:
                for fichero in files[2]:
                    _logger.warning('data = {} fichero = {}'.format(data, fichero))
                    if data == fichero:
                        #_logger.warning('Encontrado en {}'.format(files[0]+'/'+fichero))
                        lstFiles.append(files[0]+'/'+fichero)
        else:
            for files in lstDir:
                for fichero in files[2]:
                    (nombreFichero, extension) = os.path.splitext(fichero)
                    if extension == '.'+str(formato):
                        with open(files[0]+'/'+fichero) as f:
                            for i, line in enumerate(f, 1):
                                if data in line:
                                    #_logger.warning('Encontrado en {} en la linea {}'.format(files[0]+'/'+fichero, i))
                                    lstFiles.append((files[0]+'/'+fichero, i))
        if not lstFiles:
            raise Warning('No hemos podido encontrar su busqueda')
        else:
            raise Warning('Se Encontro {}'.format(lstFiles))

        #_logger.warning('LISTADO FINALIZADO')
        #_logger.warning("longitud de la lista = {}".format(len(lstFiles)))
