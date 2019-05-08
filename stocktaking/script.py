from stocktaking.models import Specification

sp = Specification.objects.all()

for s in sp:
	if s.field == 'IntegerField':
		s.field = 'FloatField'
		s.save()




# from stocktaking.models import Equipment, Model

# lst = [{'list': [122, 42, 59, 84, 88, 23, 97, 138, 126, 158], 'id': 1}, {'list': [43, 127], 'id': 2}, {'list': [30, 50, 92], 'id': 3}, {'list': [93], 'id': 4}, {'list': [94], 'id': 5}, {'list': [95], 'id': 6}, {'list': [140, 74, 2], 'id': 7}, {'list': [3], 'id': 8}, {'list': [103, 142, 66, 5], 'id': 9}, {'list': [104, 143, 6, 67], 'id': 10}, {'list': [105, 68, 7], 'id': 11}, {'list': [107, 145, 70, 9], 'id': 12}, {'list': [110, 150, 129, 12, 133], 'id': 14}, {'list': [121, 155, 83, 22], 'id': 15}, {'list': [123, 85, 24], 'id': 16}, {'list': [124, 86, 25], 'id': 17}, {'list': [108, 71, 10, 146], 'id': 13}, {'list': [111, 152, 73, 13, 135], 'id': 18}, {'list': [90], 'id': 19}, {'list': [27], 'id': 20}, {'list': [28, 48], 'id': 21}, {'list': [51, 31], 'id': 22}, {'list': [52, 32], 'id': 23}, {'list': [53, 33], 'id': 24}, {'list': [35], 'id': 25}, {'list': [36], 'id': 26}, {'list': [99, 17, 62], 'id': 27}, {'list': [100, 63], 'id': 28}, {'list': [101, 64], 'id': 29}, {'list': [75], 'id': 30}, {'list': [76], 'id': 31}, {'list': [78, 118], 'id': 32}, {'list': [79, 119], 'id': 33}, {'list': [80, 115], 'id': 34}, {'list': [81, 117], 'id': 35}, {'list': [130], 'id': 36}, {'list': [16], 'id': 37}, {'list': [55], 'id': 38}, {'list': [56], 'id': 39}, {'list': [57], 'id': 40}, {'list': [58], 'id': 41}, {'list': [147], 'id': 42}, {'list': [154], 'id': 43}, {'list': [156], 'id': 44}, {'list': [157], 'id': 45}, {'list': [151], 'id': 46}, {'list': [], 'id': 47}, {'list': [38], 'id': 48}, {'list': [], 'id': 49}, {'list': [134], 'id': 50}, {'list': [136], 'id': 51}, {'list': [21, 19], 'id': 52}]

# eqs = Equipment.objects.all()
# for e in eqs:		
# 	s = {}
# 	for key in e.specifications:
# 		for l in lst:
# 			intkey = int(key)
# 			if intkey in l['list']:							
# 				id = str(l['id'])
# 				value = 'SI' if e.specifications[key] == True else 'NO' if e.specifications[key] == False else e.specifications[key]
# 				s.update({id: value})
# 				break;	
# 	e.specifications.update(s)
# 	e.save()

# eqs = Model.objects.all()
# for e in eqs:		
# 	s = {}
# 	for key in e.specifications:
# 		for l in lst:
# 			intkey = int(key)
# 			if intkey in l['list']:							
# 				id = str(l['id'])
# 				value = 'SI' if e.specifications[key] == True else 'NO' if e.specifications[key] == False else e.specifications[key]
# 				s.update({id: value})
# 				break;	
# 	e.specifications.update(s)
# 	e.save()
###


# from stocktaking.models import Type

# types = Type.objects.all()
# for t in types:
# 	print('----'+t.name+'----')
# 	for ts in t.type_specifications.all().order_by('order'):
# 		if ts.widget=='separator':
# 			print 'GRUPO:'+ ts.label
# 		else:
# 			print(ts.id, ts.label)


# a1=[(1, u'Direcci\xf3n IP'),(122, u'Direcci\xf3n ip'),(42, u'Direcci\xf3n Ip'),(59, u'Direcci\xf3n ip'),(84, u'Direcci\xf3n ip'),(88, u'Direcci\xf3n ip'),(23, u'Direcci\xf3n Ip'),(97, u'Direcci\xf3n ip'),(138, u'Direcci\xf3n ip'),(126, u'Direcci\xf3n ip'),(158, u'IPs S.O.')]
# a2=[(2, u'Direcci\xf3n MAC'),(43, u'Direcci\xf3n Mac'),(127, u'Direcci\xf3n mac')]
# a3=[(3, u'N\xfamero de cartucho negro'),(30, u'C\xf3digo de cartucho negro'),(50, u'C\xf3digo de cartucho negro'),(92, u'Cartucho de toner')]
# a4=[(4, u'M\xf3dulo de imagen (DRUM)'),(93, u'M\xf3dulo de imagen (DRUM)')]
# a5=[(5, u'M\xf3dulo de fusor'),(94, u'M\xf3dulo de fusor')]
# a6=[(6, u'Rodillo de transferencia'),(95, u'Rodillo de transferencia')]
# a7=[(7, u'Unidad \xd3ptica'),(140, u'Unidad \xd3ptica'),(74, u'Unidad \xf3ptica'),(2, u'Unidad \xd3ptica')]
# a8=[(8, u'Unidad Lectora'),(3, u'Unidad Lectora')]
# a9=[(9, u'Nombre de procesador'),(103, u'Nombre'),(142, u'Nombre/#Parte'),(66, u'Nombre'),(5, u'Nombre')]
# a10=[(10, u'Velocidad (GHz)'),(104, u'Velocidad (GHz)'),(143, u'Velocidad (GHz)'),(6, u'Velocidad (GHz)'),(67, u'Velocidad (GHz)')]
# a11=[(11, u'Conjunto de instrucciones'),(105, u'Conjunto de instrucciones'),(68, u'Conjunto de instrucciones'),(7, u'Conjunto de instrucciones')]
# a12=[(12, u'Tipo de RAM'),(107, u'Tipo'),(145, u'Tipo'),(70, u'Tipo'),(9, u'Tipo')]
# a13=[(14, u'Tipo de conexi\xf3n'),(110, u'Tipo'),(150, u'Tipo'),(129, u'Tipo'),(12, u'Tipo'),(133, u'Tipo')]
# a14=[(15, u'Sistema operativo'),(121, u'Sistema operativo'),(155, u'Sistema Operativo'),(83, u'Sistema operativo'),(22, u'Sistema opetarivo')]
# a15=[(16, u'Nombre de usuario'),(123, u'Nombre de usuario'),(85, u'Nombre de usuario'),(24, u'Nombre de usuario')]
# a16=[(17, u'Acceso remoto'),(124, u'Acceso remoto'),(86, u'Acceso remoto'),(25, u'Acceso remoto')]
# a17=[(13, u'Capacidad RAM (GB)'),(108, u'Capacidad (GB)'),(71, u'Capacidad (GB)'),(10, u'Capacidad (GB)'),(146, u'Capacidad (GB) Instalada')]
# a18=[(18, u'Capacidad Disco (GB)'),(111, u'Capacidad (Gb)'),(152, u'Capacidad Instalada(GB)'),(73, u'Capacidad (GB)'),(13, u'Capacidad (GB)'),(135, u'Capacidad (GB)')]
# a19=[(19, u'Doble cara'),(90, u'Duplex')]
# a20=[(20, u'Tipo de impresi\xf3n'),(27, u'Tipo')]
# a21=[(21, u'Tipo de suministro'),(28, u'Suministro'),(48, u'Suministro')]
# a22=[(22, u'N\xfamero de cartucho cyan'),(51, u'C\xf3digo de cartucho cyan'),(31, u'C\xf3digo de cartucho cyan')]
# a23=[(23, u'N\xfamero de cartucho magenta'),(52, u'C\xf3digo de cartucho magenta'),(32, u'C\xf3digo de cartucho magenta')]
# a24=[(24, u'N\xfamero de cartucho amarillo'),(53, u'C\xf3digo de cartucho amarillo'),(33, u'C\xf3digo de cartucho amarillo')]
# a25=[(25, u'N\xfamero de cartucho cyan claro'),(35, u'C\xf3digo de cartucho cyan claro')]
# a26=[(26, u'N\xfamero de cartucho magenta claro'),(36, u'C\xf3digo de cartucho magenta claro')]
# a27=[(27, u'Tama\xf1o de pantalla (plg)'),(99, u'Tama\xf1o (plg)'),(17, u'Dimensi\xf3n (Plg)'),(62, u'Tama\xf1o (plg)')]
# a28=[(28, u'Resoluci\xf3n de pantalla'),(100, u'Resoluci\xf3n'),(63, u'Resoluci\xf3n')]
# a29=[(29, u'Nombre de tarjeta de v\xeddeo'),(101, u'Tarjeta de video'),(64, u'Tarjeta de video')]
# a30=[(30, u'Camar\xe1 web'),(75, u'Webcam')]
# a31=[(31, u'Tecnolog\xeda de bateria'),(76, u'Tecnolog\xeda de bateria')]
# a32=[(32, u'WIFI'),(78, u'WIFI'),(118, u'Wifi')]
# a33=[(33, u'Bluetooth'),(79, u'Bluetooth'),(119, u'Bluetooth')]
# a34=[(34, u'Cantidad de puertos USB'),(80, u'Cantidad de puertos USB'),(115, u'Cantidad de puertos usb')]
# a35=[(35, u'HDMI'),(81, u'HDMI'),(117, u'HDMI')]
# a36=[(36, u'Serial del sistema operativo'),(130, u'Serial del sistema operativo')]
# a37=[(37, u'Tipo pantalla'),(16, u'Tipo')]
# a38=[(38, u'N\xfamero de cabezal negro'),(55, u'C\xf3digo de cabezal negro')]
# a39=[(39, u'N\xfamero de cabezal cyan'),(56, u'C\xf3digo de cabezal cyan')]
# a40=[(40, u'N\xfamero de cabezal magenta'),(57, u'C\xf3digo de cabezal magenta')]
# a41=[(41, u'N\xfamero de cabezal amarillo'),(58, u'C\xf3digo de cabezal amarillo')]
# a42=[(42, u'Memoria expandible hasta (GB)'),(147, u'Capacidad(GB)')]
# a43=[(43, u'S. Virtual'),(154, u'S. Virtual')]
# a44=[(44, u'Direcci\xf3n IP IOS'),(156, u'IP IOS')]
# a45=[(45, u'Direcci\xf3n IP Virtual'),(157, u'IP Virtual')]
# a46=[(46, u'Numero de discos/capacidad(GB)'),(151, u'Cantidad/capacidad')]
# a47=[(47, u'Nombre en pantalla')]
# a48=[(48, u'N\xfamero de telefono'),(38, u'Numero de extensi\xf3n')]
# a49=[(49, u'Contrase\xf1a telefono')]
# a50=[(50, u'Tama\xf1o de disco (plg)'),(134, u'Tama\xf1o')]
# a51=[(51, u'Rendimiento del disco (RPM)'),(136, u'Rendimiento (RPM)')]
# a52=[(52, u'Conector mouse'),(21, u'Conector'),(19, u'Conector')]

# lst = []
# for i in range(1,53):	
# 	a = eval('a'+str(i))
# 	_id = a.pop(0)[0]
# 	_list =  [t[0] for t in a]
# 	lst.append({
# 		'id': _id,
# 		'list': _list
# 	})

# print lst


# (1, u'Direcci\xf3n IP') - (122, u'Direcci\xf3n ip') (42, u'Direcci\xf3n Ip') (59, u'Direcci\xf3n ip') (84, u'Direcci\xf3n ip') (88, u'Direcci\xf3n ip') (23, u'Direcci\xf3n Ip') (97, u'Direcci\xf3n ip') (138, u'Direcci\xf3n ip') (126, u'Direcci\xf3n ip') (158, u'IPs S.O.')
# (2, u'Direcci\xf3n MAC') - (43, u'Direcci\xf3n Mac') (127, u'Direcci\xf3n mac')
# (3, u'N\xfamero de cartucho negro') - (30, u'C\xf3digo de cartucho negro') (50, u'C\xf3digo de cartucho negro') (92, u'Cartucho de toner')
# (4, u'M\xf3dulo de imagen (DRUM)') - (93, u'M\xf3dulo de imagen (DRUM)')
# (5, u'M\xf3dulo de fusor') - (94, u'M\xf3dulo de fusor')
# (6, u'Rodillo de transferencia') - (95, u'Rodillo de transferencia')
# (7, u'Unidad \xd3ptica') - (140, u'Unidad \xd3ptica') (74, u'Unidad \xf3ptica') (2, u'Unidad \xd3ptica')
# (8, u'Unidad Lectora') - (3, u'Unidad Lectora')
# (9, u'Nombre de procesador') - (103, u'Nombre') (142, u'Nombre/#Parte') (66, u'Nombre') (5, u'Nombre')
# (10, u'Velocidad (GHz)') - (104, u'Velocidad (GHz)') (143, u'Velocidad (GHz)') (6, u'Velocidad (GHz)') (67, u'Velocidad (GHz)')
# (11, u'Conjunto de instrucciones') - (105, u'Conjunto de instrucciones') (68, u'Conjunto de instrucciones') (7, u'Conjunto de instrucciones')
# (12, u'Tipo de RAM') - (107, u'Tipo') (145, u'Tipo') (70, u'Tipo') (9, u'Tipo')
# (14, u'Tipo de conexi\xf3n') - (110, u'Tipo') (150, u'Tipo') (129, u'Tipo') (12, u'Tipo') (133, u'Tipo')
# (15, u'Sistema operativo') - (121, u'Sistema operativo') (155, u'Sistema Operativo') (83, u'Sistema operativo') (22, u'Sistema opetarivo')
# (16, u'Nombre de usuario') - (123, u'Nombre de usuario') (85, u'Nombre de usuario') (24, u'Nombre de usuario')
# (17, u'Acceso remoto') - (124, u'Acceso remoto') (86, u'Acceso remoto') (25, u'Acceso remoto')
# (13, u'Capacidad RAM (GB)') - (108, u'Capacidad (GB)') (71, u'Capacidad (GB)') (10, u'Capacidad (GB)') (146, u'Capacidad (GB) Instalada')
# (18, u'Capacidad Disco (GB)') - (111, u'Capacidad (Gb)') (152, u'Capacidad Instalada(GB)') (73, u'Capacidad (GB)') (13, u'Capacidad (GB)') (135, u'Capacidad (GB)')
# (19, u'Doble cara') - (90, u'Duplex')
# (20, u'Tipo de impresi\xf3n') - (27, u'Tipo')
# (21, u'Tipo de suministro') - (28, u'Suministro') (48, u'Suministro')
# (22, u'N\xfamero de cartucho cyan') - (51, u'C\xf3digo de cartucho cyan') (31, u'C\xf3digo de cartucho cyan')
# (23, u'N\xfamero de cartucho magenta') - (52, u'C\xf3digo de cartucho magenta') (32, u'C\xf3digo de cartucho magenta')
# (24, u'N\xfamero de cartucho amarillo') - (53, u'C\xf3digo de cartucho amarillo') (33, u'C\xf3digo de cartucho amarillo')
# (25, u'N\xfamero de cartucho cyan claro') - (35, u'C\xf3digo de cartucho cyan claro')
# (26, u'N\xfamero de cartucho magenta claro') - (36, u'C\xf3digo de cartucho magenta claro')
# (27, u'Tama\xf1o de pantalla (plg)') - (99, u'Tama\xf1o (plg)') (17, u'Dimensi\xf3n (Plg)') (62, u'Tama\xf1o (plg)')
# (28, u'Resoluci\xf3n de pantalla') - (100, u'Resoluci\xf3n') (63, u'Resoluci\xf3n')
# (29, u'Nombre de tarjeta de v\xeddeo') - (101, u'Tarjeta de video') (64, u'Tarjeta de video')
# (30, u'Camar\xe1 web') - (75, u'Webcam')
# (31, u'Tecnolog\xeda de bateria') - (76, u'Tecnolog\xeda de bateria')
# (32, u'WIFI') - (78, u'WIFI') (118, u'Wifi')
# (33, u'Bluetooth') - (79, u'Bluetooth') (119, u'Bluetooth')
# (34, u'Cantidad de puertos USB') - (80, u'Cantidad de puertos USB') (115, u'Cantidad de puertos usb')
# (35, u'HDMI') - (81, u'HDMI') (117, u'HDMI')
# (36, u'Serial del sistema operativo') - (130, u'Serial del sistema operativo')
# (37, u'Tipo pantalla') - (16, u'Tipo')
# (38, u'N\xfamero de cabezal negro') - (55, u'C\xf3digo de cabezal negro')
# (39, u'N\xfamero de cabezal cyan') - (56, u'C\xf3digo de cabezal cyan')
# (40, u'N\xfamero de cabezal magenta') - (57, u'C\xf3digo de cabezal magenta')
# (41, u'N\xfamero de cabezal amarillo') - (58, u'C\xf3digo de cabezal amarillo')
# (42, u'Memoria expandible hasta (GB)') - (147, u'Capacidad(GB)')#Total
# (43, u'S. Virtual') - (154, u'S. Virtual')
# (44, u'Direcci\xf3n IP IOS') - (156, u'IP IOS')
# (45, u'Direcci\xf3n IP Virtual') - (157, u'IP Virtual')
# (46, u'Numero de discos/capacidad(GB)') - (151, u'Cantidad/capacidad')
# (47, u'Nombre en pantalla')
# (48, u'N\xfamero de telefono') - (38, u'Numero de extensi\xf3n')
# (49, u'Contrase\xf1a telefono')
# (50, u'Tama\xf1o de disco (plg)') - (134, u'Tama\xf1o')
# (51, u'Rendimiento del disco (RPM)') - (136, u'Rendimiento (RPM)')
# (52, u'Conector mouse') - (21, u'Conector') (19, u'Conector')



# ----ADAPTADOR DE TELEFONO ANALOGO----
# GRUPO:Especificaciones
# (126, u'Direcci\xf3n ip')
# (127, u'Direcci\xf3n mac')
# ----CAMARA DE VIGILANCIA----
# GRUPO:Especificaciones
# (138, u'Direcci\xf3n ip')
# ----COPIADORA----
# GRUPO:Suministros
# (92, u'Cartucho de toner')
# (93, u'M\xf3dulo de imagen (DRUM)')
# (94, u'M\xf3dulo de fusor')
# (95, u'Rodillo de transferencia')
# GRUPO:Especificaciones
# (97, u'Direcci\xf3n ip')
# ----CPU----
# GRUPO:Medios extraibles
# (2, u'Unidad \xd3ptica')
# (3, u'Unidad Lectora')
# GRUPO:Procesador
# (5, u'Nombre')
# (6, u'Velocidad (GHz)')
# (7, u'Conjunto de instrucciones')
# GRUPO:Memoria ram
# (9, u'Tipo')
# (10, u'Capacidad (GB)')
# GRUPO:Disco duro
# (12, u'Tipo')
# (13, u'Capacidad (GB)')
# GRUPO:Sistema
# (22, u'Sistema opetarivo')
# (23, u'Direcci\xf3n Ip')
# (24, u'Nombre de usuario')
# (25, u'Acceso remoto')
# ----ESCANNER----
# GRUPO:Especificaciones
# (90, u'Duplex')
# ----FAX----
# ----IMPRESORA----
# GRUPO:Especificaciones
# (27, u'Tipo')
# (28, u'Suministro')
# GRUPO:Cartuchos
# (30, u'C\xf3digo de cartucho negro')
# (31, u'C\xf3digo de cartucho cyan')
# (32, u'C\xf3digo de cartucho magenta')
# (33, u'C\xf3digo de cartucho amarillo')
# GRUPO:Cartuchos adicionales
# (35, u'C\xf3digo de cartucho cyan claro')
# (36, u'C\xf3digo de cartucho magenta claro')
# GRUPO:Especificaciones
# (88, u'Direcci\xf3n ip')
# ----LAPTOP----
# GRUPO:Pantalla
# (62, u'Tama\xf1o (plg)')
# (63, u'Resoluci\xf3n')
# (64, u'Tarjeta de video')
# GRUPO:Procesador
# (66, u'Nombre')
# (67, u'Velocidad (GHz)')
# (68, u'Conjunto de instrucciones')
# GRUPO:Memoria
# (70, u'Tipo')
# (71, u'Capacidad (GB)')
# GRUPO:Almacenamiento
# (129, u'Tipo')
# (73, u'Capacidad (GB)')
# GRUPO:Conectividad y periferia
# (74, u'Unidad \xf3ptica')
# (75, u'Webcam')
# (76, u'Tecnolog\xeda de bateria')
# (78, u'WIFI')
# (79, u'Bluetooth')
# (80, u'Cantidad de puertos USB')
# (81, u'HDMI')
# GRUPO:Sistema
# (83, u'Sistema operativo')
# (130, u'Serial del sistema operativo')
# (131, u'Service tag')
# (84, u'Direcci\xf3n ip')
# (85, u'Nombre de usuario')
# (86, u'Acceso remoto')
# ----MONITOR----
# GRUPO:Especificaciones
# (16, u'Tipo')
# (17, u'Dimensi\xf3n (Plg)')
# ----PLOTTER----
# GRUPO:Especificaciones
# (48, u'Suministro')
# GRUPO:Cartuchos
# (50, u'C\xf3digo de cartucho negro')
# (51, u'C\xf3digo de cartucho cyan')
# (52, u'C\xf3digo de cartucho magenta')
# (53, u'C\xf3digo de cartucho amarillo')
# GRUPO:Cabezales
# (55, u'C\xf3digo de cabezal negro')
# (56, u'C\xf3digo de cabezal cyan')
# (57, u'C\xf3digo de cabezal magenta')
# (58, u'C\xf3digo de cabezal amarillo')
# GRUPO:Especificaciones
# (59, u'Direcci\xf3n ip')
# ----PUNTO DE VENTA----
# ----SERVIDORES----
# GRUPO:Medios extraibles
# (140, u'Unidad \xd3ptica')
# GRUPO:Procesador
# (142, u'Nombre/#Parte')
# (143, u'Velocidad (GHz)')
# GRUPO:Memoria ram
# (145, u'Tipo')
# (146, u'Capacidad (GB) Instalada')
# (147, u'Capacidad(GB)')
# (148, u'Num Parte')
# GRUPO:Disco duro
# (150, u'Tipo')
# (151, u'Cantidad/capacidad')
# (152, u'Capacidad Instalada(GB)')
# GRUPO:Sistema
# (154, u'S. Virtual')
# (155, u'Sistema Operativo')
# (156, u'IP IOS')
# (157, u'IP Virtual')
# (158, u'IPs S.O.')
# ----TELEFONO----
# GRUPO:Especificaciones
# (38, u'Numero de extensi\xf3n')
# (42, u'Direcci\xf3n Ip')
# (43, u'Direcci\xf3n Mac')
# ----TODO EN UNO----
# GRUPO:Pantalla
# (99, u'Tama\xf1o (plg)')
# (100, u'Resoluci\xf3n')
# (101, u'Tarjeta de video')
# GRUPO:Procesador
# (103, u'Nombre')
# (104, u'Velocidad (GHz)')
# (105, u'Conjunto de instrucciones')
# GRUPO:Memoria
# (107, u'Tipo')
# (108, u'Capacidad (GB)')
# GRUPO:Almacenamiento
# (110, u'Tipo')
# (111, u'Capacidad (Gb)')
# GRUPO:Conexiones y periferia
# (113, u'Entrada para audifonos')
# (114, u'Lector de tarjetas')
# (115, u'Cantidad de puertos usb')
# (116, u'Cantidad de puertos thunderbolt')
# (117, u'HDMI')
# (119, u'Bluetooth')
# (118, u'Wifi')
# GRUPO:Sistema
# (121, u'Sistema operativo')
# (122, u'Direcci\xf3n ip')
# (123, u'Nombre de usuario')
# (124, u'Acceso remoto')
# ----DISCO DURO----
# GRUPO:Especificaciones
# (133, u'Tipo')
# (134, u'Tama\xf1o')
# (135, u'Capacidad (GB)')
# (136, u'Rendimiento (RPM)')
# ----MEMORIA RAM----
# GRUPO:Especificaciones
# (45, u'Tipo')
# (46, u'Capacidad (GB)')
# ----MOUSE----
# GRUPO:Especificaciones
# (21, u'Conector')
# ----REGULADOR DE VOLTAJE----
# ----TECLADO----
# GRUPO:Especificaciones
# (19, u'Conector')
# ----TONNER----
# GRUPO:Especificaciones
# (40, u'Cantidad de impresiones')
# (41, u'Impresoras compatibles')