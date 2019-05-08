# from stocktaking.models import Type

# types = Type.objects.all()
# for t in types:
# 	print('----'+t.name+'----')
# 	for ts in t.type_specifications.all().order_by('order'):
# 		if ts.widget=='separator':
# 			print 'GRUPO:'+ ts.label
# 		else:
# 			print(ts.id, ts.label)


a1=[(1, u'Direcci\xf3n IP'),(122, u'Direcci\xf3n ip'),(42, u'Direcci\xf3n Ip'),(59, u'Direcci\xf3n ip'),(84, u'Direcci\xf3n ip'),(88, u'Direcci\xf3n ip'),(23, u'Direcci\xf3n Ip'),(97, u'Direcci\xf3n ip'),(138, u'Direcci\xf3n ip'),(126, u'Direcci\xf3n ip'),(158, u'IPs S.O.')]
a2=[(2, u'Direcci\xf3n MAC'),(43, u'Direcci\xf3n Mac'),(127, u'Direcci\xf3n mac')]
a3=[(3, u'N\xfamero de cartucho negro'),(30, u'C\xf3digo de cartucho negro'),(50, u'C\xf3digo de cartucho negro'),(92, u'Cartucho de toner')]
a4=[(4, u'M\xf3dulo de imagen (DRUM)'),(93, u'M\xf3dulo de imagen (DRUM)')]
a5=[(5, u'M\xf3dulo de fusor'),(94, u'M\xf3dulo de fusor')]
a6=[(6, u'Rodillo de transferencia'),(95, u'Rodillo de transferencia')]
a7=[(7, u'Unidad \xd3ptica'),(140, u'Unidad \xd3ptica'),(74, u'Unidad \xf3ptica'),(2, u'Unidad \xd3ptica')]
a8=[(8, u'Unidad Lectora'),(3, u'Unidad Lectora')]
a9=[(9, u'Nombre de procesador'),(103, u'Nombre'),(142, u'Nombre/#Parte'),(66, u'Nombre'),(5, u'Nombre')]
a10=[(10, u'Velocidad (GHz)'),(104, u'Velocidad (GHz)'),(143, u'Velocidad (GHz)'),(6, u'Velocidad (GHz)'),(67, u'Velocidad (GHz)')]
a11=[(11, u'Conjunto de instrucciones'),(105, u'Conjunto de instrucciones'),(68, u'Conjunto de instrucciones'),(7, u'Conjunto de instrucciones')]
a12=[(12, u'Tipo de RAM'),(107, u'Tipo'),(145, u'Tipo'),(70, u'Tipo'),(9, u'Tipo')]
a13=[(14, u'Tipo de conexi\xf3n'),(110, u'Tipo'),(150, u'Tipo'),(129, u'Tipo'),(12, u'Tipo'),(133, u'Tipo')]
a14=[(15, u'Sistema operativo'),(121, u'Sistema operativo'),(155, u'Sistema Operativo'),(83, u'Sistema operativo'),(22, u'Sistema opetarivo')]
a15=[(16, u'Nombre de usuario'),(123, u'Nombre de usuario'),(85, u'Nombre de usuario'),(24, u'Nombre de usuario')]
a16=[(17, u'Acceso remoto'),(124, u'Acceso remoto'),(86, u'Acceso remoto'),(25, u'Acceso remoto')]
a17=[(13, u'Capacidad RAM (GB)'),(108, u'Capacidad (GB)'),(71, u'Capacidad (GB)'),(10, u'Capacidad (GB)'),(146, u'Capacidad (GB) Instalada')]
a18=[(18, u'Capacidad Disco (GB)'),(111, u'Capacidad (Gb)'),(152, u'Capacidad Instalada(GB)'),(73, u'Capacidad (GB)'),(13, u'Capacidad (GB)'),(135, u'Capacidad (GB)')]
a19=[(19, u'Doble cara'),(90, u'Duplex')]
a20=[(20, u'Tipo de impresi\xf3n'),(27, u'Tipo')]
a21=[(21, u'Tipo de suministro'),(28, u'Suministro'),(48, u'Suministro')]
a22=[(22, u'N\xfamero de cartucho cyan'),(51, u'C\xf3digo de cartucho cyan'),(31, u'C\xf3digo de cartucho cyan')]
a23=[(23, u'N\xfamero de cartucho magenta'),(52, u'C\xf3digo de cartucho magenta'),(32, u'C\xf3digo de cartucho magenta')]
a24=[(24, u'N\xfamero de cartucho amarillo'),(53, u'C\xf3digo de cartucho amarillo'),(33, u'C\xf3digo de cartucho amarillo')]
a25=[(25, u'N\xfamero de cartucho cyan claro'),(35, u'C\xf3digo de cartucho cyan claro')]
a26=[(26, u'N\xfamero de cartucho magenta claro'),(36, u'C\xf3digo de cartucho magenta claro')]
a27=[(27, u'Tama\xf1o de pantalla (plg)'),(99, u'Tama\xf1o (plg)'),(17, u'Dimensi\xf3n (Plg)'),(62, u'Tama\xf1o (plg)')]
a28=[(28, u'Resoluci\xf3n de pantalla'),(100, u'Resoluci\xf3n'),(63, u'Resoluci\xf3n')]
a29=[(29, u'Nombre de tarjeta de v\xeddeo'),(101, u'Tarjeta de video'),(64, u'Tarjeta de video')]
a30=[(30, u'Camar\xe1 web'),(75, u'Webcam')]
a31=[(31, u'Tecnolog\xeda de bateria'),(76, u'Tecnolog\xeda de bateria')]
a32=[(32, u'WIFI'),(78, u'WIFI'),(118, u'Wifi')]
a33=[(33, u'Bluetooth'),(79, u'Bluetooth'),(119, u'Bluetooth')]
a34=[(34, u'Cantidad de puertos USB'),(80, u'Cantidad de puertos USB'),(115, u'Cantidad de puertos usb')]
a35=[(35, u'HDMI'),(81, u'HDMI'),(117, u'HDMI')]
a36=[(36, u'Serial del sistema operativo'),(130, u'Serial del sistema operativo')]
a37=[(37, u'Tipo pantalla'),(16, u'Tipo')]
a38=[(38, u'N\xfamero de cabezal negro'),(55, u'C\xf3digo de cabezal negro')]
a39=[(39, u'N\xfamero de cabezal cyan'),(56, u'C\xf3digo de cabezal cyan')]
a40=[(40, u'N\xfamero de cabezal magenta'),(57, u'C\xf3digo de cabezal magenta')]
a41=[(41, u'N\xfamero de cabezal amarillo'),(58, u'C\xf3digo de cabezal amarillo')]
a42=[(42, u'Memoria expandible hasta (GB)'),(147, u'Capacidad(GB)')]
a43=[(43, u'S. Virtual'),(154, u'S. Virtual')]
a44=[(44, u'Direcci\xf3n IP IOS'),(156, u'IP IOS')]
a45=[(45, u'Direcci\xf3n IP Virtual'),(157, u'IP Virtual')]
a46=[(46, u'Numero de discos/capacidad(GB)'),(151, u'Cantidad/capacidad')]
a47=[(47, u'Nombre en pantalla')]
a48=[(48, u'N\xfamero de telefono'),(38, u'Numero de extensi\xf3n')]
a49=[(49, u'Contrase\xf1a telefono')]
a50=[(50, u'Tama\xf1o de disco (plg)'),(134, u'Tama\xf1o')]
a51=[(51, u'Rendimiento del disco (RPM)'),(136, u'Rendimiento (RPM)')]
a52=[(52, u'Conector mouse'),(21, u'Conector'),(19, u'Conector')]

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
