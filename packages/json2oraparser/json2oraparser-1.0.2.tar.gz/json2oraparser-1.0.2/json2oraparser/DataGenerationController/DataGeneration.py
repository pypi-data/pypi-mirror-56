from json2oraparser import PublishToDBController
from json2oraparser import ConfigController
from json2oraparser import DBConnectionController
import os
from datetime import datetime


class DataGeneration:

    def __init__(self):
        self.objDBConnetion = DBConnectionController.DBConnection()
        self.objPublishDB = PublishToDBController.PublishDB()
        self.objConfig = ConfigController.Configuration()
        self.TimestampFormat = "RRRR-MM-DD HH24:MI:SS.FF"

    # Delete if sql file exists
    def del_sql_file(self, filename):
        try:
            if os.path.exists(filename):
                os.remove(filename)
            else:
                print("SQL file " + filename + " doesn't exist in system" + '\n')

        except Exception as e:
            print(e)

        return None

    def print_all_nodes(self, obj, strList1, strList, sPath, strtCollist, fileObj):

        """
        This routine is intended to print all nodes in the json objects
        and publish through "PublishToDBController" for either dictionary or list object.
        :param obj: the given JSON object
        :param strList1: Process traversed path in JSON / a runtime adjustment through program
        :param eventId: event ID an unique reference given for the message
        :param entityId: entity ID an unique reference given for the message
        :param strList: the given JSON fields per level
        :param sPath: Target table name given.
        :param strtCollist: Database table columns.
        :return: None
        :Advancement:None as of now
        """
        try:
            item = strList1.split("|")
            new_items = item[1:]
            strFinal = ''
            for i in new_items:
                strFinal = strFinal + i + "|"
            if (item[0].find('$') > -1):
                str1 = item[0]
                if str(str1[:-1]) in obj:
                    obj1 = obj[str(str1[:-1])]
                else:
                    return
            else:
                if str(item[0]) in obj:
                    obj1 = obj[str(item[0])]
                else:
                    return
            if item[0].find('$') > -1:
                if isinstance(obj1, dict):
                    if sPath != 'DUMMY':
                        self.objPublishDB.fn_json_wr_dict(obj1, strList, sPath, strtCollist, fileObj, obj)
                elif isinstance(obj1, list):
                    if sPath != 'DUMMY':
                        self.objPublishDB.fn_json_wr_list(obj1, strList, sPath, strtCollist, fileObj, obj)
                else:
                    print(obj1)
            else:
                if isinstance(obj1, dict):
                    self.print_all_nodes(obj1, strFinal, strList, sPath, strtCollist, fileObj)
                elif isinstance(obj1, list):
                    self.print_all_nodes(item, strFinal, strList, sPath, strtCollist, fileObj)
                else:
                    print(obj1)

        except Exception as e:
            print(e)

        return None

    def fn_generatedata(self, obj, final_list):

        """
        This routine is intended to generate data from the json objects
        by referencing data dictionary dictionary or list object.
        :param obj: the given JSON object
        :param final_list: JSON metadata / schema / data dictionary
        :param eventId: event ID an unique reference given for the message
        :param entityId: entity ID an unique reference given for the message
        :return: None
        :Advancement:None as now
        """
        try:
            returnValue = 0

            # SQL File creation
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            sql_path = self.objConfig.getConfiguration("SQL|sql_path")
            strTm = datetime.now().strftime("%Y-%m-%d-%H%M%S")
            filePath = str(sql_path) + "_" + strTm + ".sql"

            str_sql_footer = """select sysdate from dual"""
            fileObj = open(filePath, 'w+')
           # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            for item in final_list:
                if item[2] != "0":
                    obj1 = obj
                    strNodePath = item[8] + "$"
                    strList = item[5]
                    strtCollist = item[6]
                    sPath = str(item[4])
                    self.print_all_nodes(obj1, strNodePath, strList, sPath, strtCollist, fileObj)

            # Add Footer part at end of SQL file
            self.objDBConnetion.fn_sql_file_append(fileObj, str_sql_footer)

            # SQL file close
            fileObj.close()

            # Run SQL file
            ins_cnt = len(open(filePath).readlines())
            if ins_cnt > 0 and open(filePath).read() != 'select sysdate from dual':
                print("Data insertion process is started" + '\n')
                sql_out = self.objDBConnetion.fn_run_sql_script(filePath)
                print("Insert SQL Output : " + sql_out + '\n')
                if str(sql_out) != "E":
                    print("Insert script execution is completed" + '\n')
                    returnValue = int(sql_out)
                else:
                    print("Insert script execution is failed" + '\n')
                    returnValue = -1
            else:
                print("There is no record to insert into database" + '\n')

            # SQL file deletion
            #self.del_sql_file(filePath)

            return returnValue

        except Exception as e:
            print(e)
            return -1
