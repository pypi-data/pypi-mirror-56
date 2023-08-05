import json
from json2oraparser import DataGenerationController
from json2oraparser import ConfigController
from json2oraparser import MetadataController


def createMetadata(metadatafilepath):
     try:
         objMetadata = MetadataController.MetadataList()
         final_list_all = objMetadata.fn_createMetadataList(metadatafilepath)
         if final_list_all:
             print("Metadata List has been successfully created from CSV file" + '\n')
         else:
             print("Metadata List could not be created" + '\n')

         return final_list_all

     except Exception as e:
         print(e)


def loadJson(filepath, final_list_all, ip, port, sid, userid, password):
    try:
        # ------------------------
        # load json file
        # ------------------------
        data = open(filepath).read()
        finaljson = json.loads(data.decode('ascii', 'ignore'))

        # ----------------------------------------
        # write db parameters in config file
        # ----------------------------------------
        objConfig = ConfigController.Configuration()
        objConfig.updateDbConfigaration(ip, port, sid, userid, password)

        # ------------------------
        # data loading starts
        # ------------------------
        print("Data parsing and loading from Json file is started" + '\n')
        objDataGeneration = DataGenerationController.DataGeneration()
        obj = finaljson
        f_0 = objDataGeneration.fn_generatedata(obj, final_list_all)
        if f_0 > 0:
            print("Finished - Data Insertion is successfully completed" + '\n')
            print("Dataload from Json file has been successfully completed" + '\n')
        else:
            print("Not Finished - Data Insertion is failed" + '\n')
            print("Dataload from Json file has been failed" + '\n')
        # ------------------------
        # data loading ends
        # ------------------------
    except Exception as e:
        print(e)
