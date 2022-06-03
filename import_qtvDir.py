from xml.dom.minidom import parse
import xml.dom.minidom
import os
import shutil
import pymysql
import datetime

# from time import strftime

now = datetime.datetime.now()
today = now.strftime("%Y%m%d")
print(today)

# 连接数据库 connecter la bdd
conn = pymysql.connect(host="http://etu-web2.ut-capitole.fr/",
                       user="21806554",
                       passwd="T006I0",
                       db="ed_bisonfute",
                       charset="utf8")
cur = conn.cursor()

# 遍历Data文件夹,获取xml文件路径 obtenir le chemin des dossier xml
# dirpath: 文件夹路径(chemin de fichier)，filename: 文件名(nom du dossier)
# 找到今天以外的文件夹路径path
path = ""
for dirpath, dirnames, filenames in os.walk("Data"):
    for dirname in dirnames:
        date = dirname.split("_")
        if str(date[0]) != str(today):
            path = os.path.join(dirpath) + "\\" + dirname
            print(path)

            # 找到文件夹对应的xml文件路径
            for dirpath2, dirnames2, filenames2 in os.walk(path):
                for filename in filenames2:
                    if os.path.splitext(filename)[1] == ".xml":
                        filepath = os.path.join(dirpath2) + "\\" + filename
                        print(filepath)

                        # 使用minidom解析器打开 XML 文档
                        # ouvrire le dossier xml
                        DOMTree = xml.dom.minidom.parse(filepath)
                        collection = DOMTree.documentElement

                        # 公布时间 publication time
                        publication = collection.getElementsByTagName("payloadPublication")
                        pub_time = publication[0].getElementsByTagName('publicationTime')[0].childNodes[0].nodeValue
                        # print(pub_time)

                        # 在集合中获取的所有监测点
                        # toutes les stations de measure
                        station_mesure = collection.getElementsByTagName("siteMeasurements")

                        # 每个监测点的数据
                        # les donnees de chaque station de mesure
                        for stations in station_mesure:
                            target = stations.getElementsByTagName("measurementSiteReference")
                            id = target[0].getAttribute("id")
                            print(id)

                            time_default = stations.getElementsByTagName('measurementTimeDefault')[0].childNodes[
                                0].nodeValue
                            # print(time_default)

                            flow = stations.getElementsByTagName("vehicleFlow")
                            number_flow = flow[0].getAttribute("numberOfInputValuesUsed")
                            # print(number_flow)
                            flow_rate = stations.getElementsByTagName('vehicleFlowRate')[0].childNodes[0].nodeValue
                            # print(flow_rate)

                            speed = stations.getElementsByTagName("averageVehicleSpeed")
                            number_speed = speed[0].getAttribute("numberOfInputValuesUsed")
                            # print(number_speed)
                            speed_rate = stations.getElementsByTagName('vehicleFlowRate')[0].childNodes[0].nodeValue
                            # print(speed_rate)

                            # importer les donnees dans la bdd
                            sql = "INSERT INTO vitesse (site_measurementV, publication_timeV, time_defaultV, number_used_flowV, flow_rateV, number_used_speedV, speedV) VALUES ('%s','%s','%s','%s','%s','%s','%s')" % (
                                id, pub_time, time_default, number_flow, flow_rate, number_speed, speed_rate)
                            try:
                                cur.execute(sql)
                                conn.commit()
                            except:
                                conn.rollback()
                                # print("probleme de la connexion")

            # 压缩此文件夹
            shutil.make_archive(path, 'zip', path)
            shutil.rmtree(path)

cur.close()
conn.close()

