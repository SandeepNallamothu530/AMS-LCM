import sqlite3
from app import prod
from config import CLIENT_STATUS, ORG_TYPE_OPTIONS

def get_trans_names(clientid, nuid):
    print("get_trans_names");
    try:
        con = sqlite3.connect("ittrans.db")
        cursor = con.cursor()
        act = {}
        sql_select_query = """select groupid, count(groupid) from trans_details where clientid = '""" + clientid + """' and status = 'Active' group by groupid;"""
        print(sql_select_query)
        cursor.execute(sql_select_query)
        actives = cursor.fetchall()
        for active in actives:
            act[active[0]] = active[1]

        inact = {}
        sql_select_query = """select groupid, count(groupid) from trans_details where clientid = '""" + clientid + """' and status = 'Inactive' group by groupid;"""
        print(sql_select_query)
        cursor.execute(sql_select_query)
        inactives = cursor.fetchall()
        for inactive in inactives:
            inact[inactive[0]] = inactive[1]

        sql_select_query = """select distinct groupid from trans_details where clientid = '""" + clientid + """';"""
        print(sql_select_query)
        cursor.execute(sql_select_query)
        rows = cursor.fetchall()
        
        i = 0
        bpid = 'bpmChart'
        cid = 'bpmCC'
        for row in rows:
            i = i + 1
            tbpid = bpid + str(i)
            tcid = cid + str(i)
            id = nuid + str(i)
            insQry ="""insert into tempact_graph (id, uuid, clientid, module, active, inactive, bpid, cid) values ('""" + id + """','""" + nuid + """','""" + clientid + """','""" + row[0] + """','""" + str(act.get(row[0], 0)) + """','""" + str(inact.get(row[0], 0)) + """','""" +  tbpid + """','""" + tcid + """');"""
            print(insQry)
            cursor.execute(insQry)
        newSql = """select module, active, bpid, cid, inactive from tempact_graph where uuid = '""" + nuid + """';"""
        cursor.execute(newSql)
        retrows = cursor.fetchall()
        print(retrows)
        return retrows
    except Exception as e:
        print('Exception: {}'.format(e))
    finally:
        cursor.close()
        con.close()

def get_trans_head(nuid):
    try:
        con = sqlite3.connect("ittrans.db")
        cursor = con.cursor()
        newSql = """select module bpid, cid from temp_graph where uuid = '""" + nuid + """';"""
        cursor.execute(newSql)
        retrows = cursor.fetchall()
        print(retrows)
        return retrows
    except Exception as e:
        print('Exception: {}'.format(e))
    finally:
        cursor.close()
        con.close()

def get_trans_master(clientid):
    print("get_trans_master");
    try:
        con = sqlite3.connect("ittrans.db")
        cursor = con.cursor()
        sql_select_query = """select groupid, count(groupid) from trans_details where clientid = '""" + clientid + """' and status = '""" + stat + """' group by groupid;"""
        print(sql_select_query)
        cursor.execute(sql_select_query)
        rows = cursor.fetchall()
        print(rows)
        #for row in rows:
        return rows
    finally:
        cursor.close()
        con.close()

def get_trans_details(groupid, clientid):
    print("get_trans_details" + groupid + " -- " + clientid)
    try:
        con = sqlite3.connect("ittrans.db")
        cursor = con.cursor()
        sql_select_query = """select scopeid, scopeitem from trans_details where clientid = '""" + clientid + """' and status = 'Active' and groupid = '""" +  groupid + """'"""
        print(sql_select_query)
        cursor.execute(sql_select_query)
        rows = cursor.fetchall()
        print(rows)
        #for row in rows:
        return rows
    finally:
        cursor.close()
        con.close()

def get_cust_code(clientid, ttext):
    print("get_cust_code -- " + clientid)
    try:
        connection = sqlite3.connect("ittrans.db")
        cursor = connection.cursor()
        sql_select_query = """select tcode, pgmna, ttext from custom_code where clientid = '""" + clientid + """' and ttext = '""" + ttext + """'"""
        print(sql_select_query)
        cursor.execute(sql_select_query)
        rows = cursor.fetchall()
        #print(rows)
        #for row in rows:
        return rows
    finally:
        cursor.close()
        connection.close()


def get_org_master(clientid):
    print("get_org_master");
    try:
        connection = sqlite3.connect("ittrans.db")
        cursor = connection.cursor()
        sql_select_query = """select module, count(*) from code_value where clientid = '""" + clientid + """' group by module;"""
        # print(sql_select_query)
        cursor.execute(sql_select_query)
        rows = cursor.fetchall()
        # print(rows)
        #for row in rows:
        return rows
    finally:
        cursor.close()
        connection.close()

def get_org_details(groupid, clientid):
    print("Inside get_org_details details" + groupid + " -- " + clientid)
    try:
        connection = sqlite3.connect("ittrans.db")
        cursor = connection.cursor()
        sql_select_query = """select code, value, ucount from code_value where clientid = '""" + clientid + """' and module = '""" + groupid + """';"""
        print(sql_select_query)
        cursor.execute(sql_select_query)
        rows = cursor.fetchall()
        print(rows)
        #for row in rows:
        return rows
    except Exception as e:
        print('Exception: {}'.format(e))
    finally:
        cursor.close()
        connection.close()

def get_com_master(clientid, inclass, nuid):
    print("Inside get_gen_master");
    try:
        connection = sqlite3.connect("ittrans.db")
        cursor = connection.cursor()
        cursor.execute("""delete from temp_graph""")
        sql_select_query = """select module, count(*) from code_value where clientid = '""" + clientid + """' and module in (""" + inclass + """) group by module;"""
        print(sql_select_query)
        cursor.execute(sql_select_query)
        rows = cursor.fetchall()
        i = 0
        bpid = 'bpmChart'
        cid = 'bpmCC'
        for row in rows:
            i = i + 1
            tbpid = bpid + str(i)
            tcid = cid + str(i)
            id = nuid + str(i)
            insQry ="""insert into temp_graph (id, uuid, clientid, module, counts, bpid, cid) values ('""" + id + """','""" + nuid + """','""" + clientid + """','""" + row[0] + """',""" + str(row[1]) + """,'""" + tbpid + """','""" + tcid + """');"""
            print(insQry)
            cursor.execute(insQry)
        #for row in rows:
        newSql = """select module, counts, bpid, cid from temp_graph where uuid = '""" + nuid + """';"""
        cursor.execute(newSql)
        retrows = cursor.fetchall()
        print(retrows)
        return retrows
    except Exception as e:
        print('Exception: {}'.format(e))
    finally:
        cursor.close()
        connection.close()


def get_gen_master(clientid, inclass):
    print("Inside get_gen_master");
    try:
        connection = sqlite3.connect("ittrans.db")
        cursor = connection.cursor()
        sql_select_query = """select module, count(*) from code_value where clientid = '""" + clientid + """' and module in (""" + inclass + """) group by module;"""
        print(sql_select_query)
        cursor.execute(sql_select_query)
        rows = cursor.fetchall()
        print(rows)
        #for row in rows:
        return rows
    except Exception as e:
        print('Exception: {}'.format(e))
    finally:
        cursor.close()
        connection.close()

def get_sys_master(clientid,nuid):
    print("Inside get_sys_master");
    try:
        connection = sqlite3.connect("ittrans.db")
        cursor = connection.cursor()
        sql_select_query = """select sid, count(*) from sys_code_value where clientid = '""" + clientid + """' group by sid;"""
        print(sql_select_query)
        cursor.execute(sql_select_query)
        rows = cursor.fetchall()
        i = 0
        bpid = 'bpmChart'
        cid = 'bpmCC'
        for row in rows:
            i = i + 1
            tbpid = bpid + str(i)
            tcid = cid + str(i)
            id = nuid + str(i)
            insQry ="""insert into temp_graph (id, uuid, clientid, module, counts, bpid, cid) values ('""" + id + """','""" + nuid + """','""" + clientid + """','""" + row[0] + """',""" + str(row[1]) + """,'""" + tbpid + """','""" + tcid + """');"""
            print(insQry)
            cursor.execute(insQry)
        #for row in rows:
        newSql = """select module, counts, bpid, cid from temp_graph where uuid = '""" + nuid + """';"""
        cursor.execute(newSql)
        retrows = cursor.fetchall()
        print(retrows)
        return retrows
    except Exception as e:
        print('Exception: {}'.format(e))
    finally:
        cursor.close()
        connection.close()

def getSids(clientid):
    try:
        connection = sqlite3.connect("ittrans.db")
        cursor = connection.cursor()
        sql_select_query = """select sid, count(*) from sys_code_value where clientid = '""" + clientid + """' group by sid"""
        print(sql_select_query)
        cursor.execute(sql_select_query)
        rows = cursor.fetchall()
        # print(rows)
        #for row in rows:
        return rows
    except Exception as e:
        print('Exception: {}'.format(e))
    finally:
        cursor.close()
        connection.close()

def get_sys_details(sid, clientid):
    print("Inside get_sys_details details -- " + clientid)
    try:
        connection = sqlite3.connect("ittrans.db")
        cursor = connection.cursor()
        sql_select_query = """select code,value from sys_code_value where clientid = '""" + clientid + """' and sid = '""" + sid + """'"""
        print(sql_select_query)
        cursor.execute(sql_select_query)
        rows = cursor.fetchall()
        # print(rows)
        #for row in rows:
        return rows
    except Exception as e:
        print('Exception: {}'.format(e))
    finally:
        cursor.close()
        connection.close()

def getTicketGraph():
    print("Inside getTicketGraph")
    try:
        connection = sqlite3.connect("ittrans.db")
        cursor = connection.cursor()
        sql_select_query = """select Priority, count(*) from ticket_dump group by Priority"""
        print(sql_select_query)
        cursor.execute(sql_select_query)
        rows = cursor.fetchall()
        print(rows)
        #for row in rows:
        return rows
    except Exception as e:
        print('Exception: {}'.format(e))
    finally:
        cursor.close()
        connection.close()

def getTickets():
    print("Inside getTickets")
    try:
        connection = sqlite3.connect("ittrans.db")
        cursor = connection.cursor()
        sql_select_query = """select TicketNumber, TicketDescription, ContractType, PostingDate, UserStatus, SupportTeamName, Priority, ChangedAt, Classification, SLAbreached, STElapsedTime, ReportedByName, SoldToPartyName from ticket_dump"""
        print(sql_select_query)
        cursor.execute(sql_select_query)
        rows = cursor.fetchall()
        print(rows)
        #for row in rows:
        return rows
    except Exception as e:
        print('Exception: {}'.format(e))
    finally:
        cursor.close()
        connection.close()

def loadCustomers():
    try:
        connection = sqlite3.connect("ittrans.db", isolation_level=None)
        cursor = connection.cursor()
        selQry = """select clientid, orgname from customer_master"""
        print(selQry)
        cursor.execute(selQry)
        rows = cursor.fetchall()
        return rows
    
    except Exception as e:
        print('Exception: {}'.format(e))
    finally:
        cursor.close()
        connection.close()

def purge(clientid, nclientid):
    try:
        connection = sqlite3.connect("ittrans.db", isolation_level=None)
        cursor = connection.cursor()
        upd_query = """update code_value set clientid = ? where clientid = ?"""
        print(upd_query)
        cursor.execute(upd_query, (nclientid,clientid,))
        connection.commit
        connection.close

        connection = sqlite3.connect("ittrans.db", isolation_level=None)
        cursor = connection.cursor()
        upd_query = """update custom_code set clientid = ? where clientid = ?"""
        print(upd_query)
        cursor.execute(upd_query, (nclientid,clientid,))
        connection.commit
        connection.close

        connection = sqlite3.connect("ittrans.db", isolation_level=None)
        cursor = connection.cursor()
        upd_query = """update sys_code_value set clientid = ? where clientid = ?"""
        print(upd_query)
        cursor.execute(upd_query, (nclientid,clientid,))
        connection.commit
        connection.close

        connection = sqlite3.connect("ittrans.db", isolation_level=None)
        cursor = connection.cursor()
        upd_query = """update trans_details set clientid = ? where clientid = ?"""
        print(upd_query)
        cursor.execute(upd_query, (nclientid,clientid,))
        connection.commit
        connection.close
    except Exception as e:
        print('Exception: {}'.format(e))
    finally:
        cursor.close()
        connection.close()

def delete(clientid):
    try:
        connection = sqlite3.connect("ittrans.db", isolation_level=None)
        cursor = connection.cursor()
        upd_query = """delete from code_value where clientid = ?"""
        print(upd_query)
        cursor.execute(upd_query, (clientid,))
        connection.commit
        connection.close
        
        connection = sqlite3.connect("ittrans.db", isolation_level=None)
        cursor = connection.cursor()
        upd_query = """delete from sys_code_value where clientid = ?"""
        print(upd_query)
        cursor.execute(upd_query, (clientid,))
        connection.commit
        connection.close

        connection = sqlite3.connect("ittrans.db", isolation_level=None)
        cursor = connection.cursor()
        upd_query = """delete from trans_details where clientid = ?"""
        print(upd_query)
        cursor.execute(upd_query, (clientid,))
        connection.commit
        connection.close

        connection = sqlite3.connect("ittrans.db", isolation_level=None)
        cursor = connection.cursor()
        upd_query = """delete from customer_master where clientid = ?"""
        print(upd_query)
        cursor.execute(upd_query, (clientid,))
        connection.commit
        connection.close
    except Exception as e:
        print('Exception: {}'.format(e))
    finally:
        cursor.close()
        connection.close()

def cleanup(req_data):
    try:
        CustName = req_data['CustName']
        CustId = req_data['CustId']
        connection = sqlite3.connect("ittrans.db", isolation_level=None)
        cursor = connection.cursor()
        insQry = """insert into customer_master (clientid, orgname) values (?,?)"""
        print(insQry)
        cursor.execute(insQry, (CustId, CustName, ))
        connection.commit
        connection.close
        
        connection = sqlite3.connect("ittrans.db", isolation_level=None)
        cursor = connection.cursor()
        upd_query = """insert into trans_details (clientid, groupid, scopeid, scopeitem, status) select ?, groupid, scopeid, scopeitem, 'Inactive' from trans_master"""
        print(upd_query)
        cursor.execute(upd_query, (CustId,))
        connection.commit
        connection.close
    except Exception as e:
        print('Exception: {}'.format(e))
    finally:
        cursor.close()
        connection.close()

def updtransdetails(req_data):
    try:
        connection = sqlite3.connect("ittrans.db", isolation_level=None)
        cursor = connection.cursor()
        upd_query = """update trans_details set status = ? where clientid = ? and scopeid = ?;"""
        print(upd_query)
        for keys in req_data:
            scope = req_data[keys]
            cid = scope['custId']
            scp = scope['scopeID']
            stat = scope['status']
            cursor.execute(upd_query, (stat, cid, scp))
            connection.commit
    except Exception as e:
        print('Exception: {}'.format(e))
    finally:
        cursor.close()
        connection.close()


def insertCodeValue(req_data):
    try:
        connection = sqlite3.connect("ittrans.db", isolation_level=None)
        cursor = connection.cursor()
        upd_query = """insert into code_value (clientid, module, code, value, ucount) values (?,?,?,?,?);"""
        print(upd_query)
        for keys in req_data:
            scope = req_data[keys]
            cid = scope['custId']
            mod = scope['tblName']
            val = scope['value']
            cod = scope['code']
            ucount = scope['usgCount']
            cursor.execute(upd_query, (cid, mod, cod, val, ucount, ))
            connection.commit
    except Exception as e:
        print('Exception: {}'.format(e))
    finally:
        cursor.close()
        connection.close()


def insertSysCodeValue(req_data):
    try:
        connection = sqlite3.connect("ittrans.db", isolation_level=None)
        cursor = connection.cursor()
        upd_query = """insert into sys_code_value (clientid, sid, code, value) values (?,?,?,?);"""
        print(upd_query)
        for keys in req_data:
            scope = req_data[keys]
            # print(keys);
            # ids = int(keys)
            cid = scope['custId']
            mod = scope['tblName']
            val = scope['value']
            cod = scope['code']
            cursor.execute(upd_query, (cid, mod, cod, val,))
            connection.commit
        # rows = cursor.fetchall()
        # print(rows)
        # #for row in rows:
        # return rows
    except Exception as e:
        print('Exception: {}'.format(e))
    finally:
        cursor.close()
        connection.close()

def insertCustomCode(req_data):
    try:
        connection = sqlite3.connect("ittrans.db", isolation_level=None)
        cursor = connection.cursor()
        upd_query = """insert into custom_code (clientid, tcode, pgmna, ttext) values  (?,?,?,?);"""
        print(upd_query)
        for keys in req_data:
            scope = req_data[keys]
            # ids = int(keys)
            cid = scope['custId']
            mod = scope['scopeItem']
            cod = scope['scopeItemDescription']
            val = scope['scopeItemStatus']
            cursor.execute(upd_query, (cid, mod, cod, val,))
            connection.commit
        # rows = cursor.fetchall()
        # print(rows)
        # #for row in rows:
        # return rows
    except Exception as e:
        print('Exception: {}'.format(e))
    finally:
        cursor.close()
        connection.close()

def updateCustomCode(req_data):
    try:
        connection = sqlite3.connect("ittrans.db", isolation_level=None)
        cursor = connection.cursor()
        upd_query = """update custom_code set ttext = ? where tcode = ? and clientid = ?;"""
        print(upd_query)
        for keys in req_data:
            scope = req_data[keys]
            mod = scope['scopeItem']
            cod = scope['scopeItemStatus']
            cid = scope['custId']
            # print(mod)
            # print(cod)
            cid = scope['custId']
            cursor.execute(upd_query, (cod, mod,cid,))
            connection.commit
        # rows = cursor.fetchall()
        # print(rows)
        # #for row in rows:
        # return rows
    except Exception as e:
        print('Exception: {}'.format(e))
    finally:
        cursor.close()
        connection.close()


def updusageCount(req_data):
    try:
        connection = sqlite3.connect("ittrans.db", isolation_level=None)
        cursor = connection.cursor()
        upd_query = """update custom_code set ucount = ? where module = ? and code = ? and clientid = ?;"""
        print(upd_query)
        for keys in req_data:
            scope = req_data[keys]
            cid = scope['custId']
            mod = scope['tblName']
            val = scope['value']
            cod = scope['code']
            cursor.execute(upd_query, (cod, mod,cod, cid,))
            connection.commit
        # rows = cursor.fetchall()
        # print(rows)
        # #for row in rows:
        # return rows
    except Exception as e:
        print('Exception: {}'.format(e))
    finally:
        cursor.close()
        connection.close()

def getSysCount(client):
    try:
        connection = sqlite3.connect("ittrans.db")
        cursor = connection.cursor()
        sql_select_query = """select distinct sid from sys_code_value where clientid = ?"""
        print(sql_select_query)
        cursor.execute(sql_select_query, (client,))
        rows = cursor.fetchall()
        print(len(rows))
        return len(rows)
    except Exception as e:
        print('Exception: {}'.format(e))
    finally:
        cursor.close()
        connection.close()

def getCustCount(clientid):
    try:
        connection = sqlite3.connect("ittrans.db")
        cursor = connection.cursor()
        sql_select_query = """select count(*) as tcount from code_value where module in ('Company Code','Cost Center','Profit Center') and clientid = ?"""
        print(sql_select_query)
        cursor.execute(sql_select_query, (clientid, ))
        rows = cursor.fetchall()
        print(rows[0][0])
        #for row in rows:
        return rows[0][0]
    except Exception as e:
        print('Exception: {}'.format(e))
    finally:
        cursor.close()
        connection.close()

def getSaleCount(clientid):
    try:
        connection = sqlite3.connect("ittrans.db")
        cursor = connection.cursor()
        sql_select_query = """select count(*) as tcount from code_value where module in ('Sales Org','Distribution Channel','Division') and clientid = ?"""
        print(sql_select_query)
        cursor.execute(sql_select_query, (clientid, ))
        rows = cursor.fetchall()
        print(rows[0][0])
        #for row in rows:
        return rows[0][0]
    except Exception as e:
        print('Exception: {}'.format(e))
    finally:
        cursor.close()
        connection.close()

def getPurCount(clientid):
    try:
        connection = sqlite3.connect("ittrans.db")
        cursor = connection.cursor()
        sql_select_query = """select count(*) as tcount from code_value where module in ('Purchase Org','Purchase Group') and clientid = ?"""
        print(sql_select_query)
        cursor.execute(sql_select_query, (clientid, ))
        rows = cursor.fetchall()
        print(rows[0][0])
        #for row in rows:
        return rows[0][0]
    except Exception as e:
        print('Exception: {}'.format(e))
    finally:
        cursor.close()
        connection.close()

def getPlantCount(clientid):
    try:
        connection = sqlite3.connect("ittrans.db")
        cursor = connection.cursor()
        sql_select_query = """select count(*) as tcount from code_value where module ='Plant' and clientid = ?"""
        print(sql_select_query)
        cursor.execute(sql_select_query, (clientid,))
        rows = cursor.fetchall()
        print(rows[0][0])
        #for row in rows:
        return rows[0][0]
    except Exception as e:
        print('Exception: {}'.format(e))
    finally:
        cursor.close()
        connection.close()

def getBp1Count(clientid):
    try:
        connection = sqlite3.connect("ittrans.db")
        cursor = connection.cursor()
        sql_select_query = """select count(*) as tcount from trans_details where status = 'Active' and clientid = ?"""
        print(sql_select_query)
        cursor.execute(sql_select_query, (clientid,))
        rows = cursor.fetchall()
        print(rows[0][0])
        #for row in rows:
        return rows[0][0]
    except Exception as e:
        print('Exception: {}'.format(e))
    finally:
        cursor.close()
        connection.close()

def getBp2Count(clientid):
    try:
        connection = sqlite3.connect("ittrans.db")
        cursor = connection.cursor()
        sql_select_query = """select count(*) as tcount from code_value where module in ('Sales Doc Type','Purchase Doc Type', 'Pricing Procedure') and clientid = ?"""
        print(sql_select_query)
        cursor.execute(sql_select_query, (clientid,))
        rows = cursor.fetchall()
        print(rows[0][0])
        #for row in rows:
        return rows[0][0]
    except Exception as e:
        print('Exception: {}'.format(e))
    finally:
        cursor.close()
        connection.close()

def getCustCodeCount(clientid):
    try:
        connection = sqlite3.connect("ittrans.db")
        cursor = connection.cursor()
        sql_select_query = """select count(*) as tcount from custom_code where clientid = ?"""
        print(sql_select_query)
        cursor.execute(sql_select_query, (clientid,))
        rows = cursor.fetchall()
        print(rows[0][0])
        #for row in rows:
        return rows[0][0]
    except Exception as e:
        print('Exception: {}'.format(e))
    finally:
        cursor.close()
        connection.close()

def getMMCount(clientid):
    try:
        connection = sqlite3.connect("ittrans.db")
        cursor = connection.cursor()
        sql_select_query = """select sum(value) from code_value where (module = 'Material' or module ='Master') and code = 'TotalCount' and clientid = ?"""
        print(sql_select_query)
        cursor.execute(sql_select_query, (clientid,))
        rows = cursor.fetchall()
        print(rows[0][0])
        return rows[0][0]
    except Exception as e:
        print('Exception: {}'.format(e))
    finally:
        cursor.close()
        connection.close()

def getMaterialMaster(clientid):
    try:
        connection = sqlite3.connect("ittrans.db")
        cursor = connection.cursor()
        sql_select_query = """select code, value from code_value where (module = 'Material' or module ='Master') and code <> 'TotalCount' and clientid = ?"""
        print(sql_select_query)
        cursor.execute(sql_select_query, (clientid,))
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print('Exception: {}'.format(e))
    finally:
        cursor.close()
        connection.close()

def getMasterCount(clientid):
    try:
        connection = sqlite3.connect("ittrans.db")
        cursor = connection.cursor()
        sql_select_query = """select value from code_value where module ='Master' and code = 'TotalCount' and clientid = ?"""
        print(sql_select_query)
        cursor.execute(sql_select_query, (clientid,))
        rows = cursor.fetchall()
        print(rows[0][0])
        #for row in rows:
        return rows[0][0]
    except Exception as e:
        print('Exception: {}'.format(e))
    finally:
        cursor.close()
        connection.close()
        
def getMaster(clientid):
    try:
        connection = sqlite3.connect("ittrans.db")
        cursor = connection.cursor()
        sql_select_query = """select code, value from code_value where module = 'Master' and code <> 'TotalCount' and clientid = ?"""
        print(sql_select_query)
        cursor.execute(sql_select_query, (clientid,))
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print('Exception: {}'.format(e))
    finally:
        cursor.close()
        connection.close()

def getBp2ItemCount(module, clientid):
    try:
        connection = sqlite3.connect("ittrans.db")
        cursor = connection.cursor()
        sql_select_query = """select count(*) as tcount from code_value where module = ? and clientid = ?"""
        print(sql_select_query)
        cursor.execute(sql_select_query, (module, clientid,))
        rows = cursor.fetchall()
        print(rows[0][0])
        #for row in rows:
        return rows[0][0]
    except Exception as e:
        print('Exception: {}'.format(e))
    finally:
        cursor.close()
        connection.close()

def getCustCodeCountGW(groups, clientid):
    try:
        connection = sqlite3.connect("ittrans.db")
        cursor = connection.cursor()
        sql_select_query = """select count(*) as tcount from custom_code where ttext = ? and clientid = ?"""
        print(sql_select_query)
        cursor.execute(sql_select_query, (groups, clientid,))
        rows = cursor.fetchall()
        print(rows[0][0])
        #for row in rows:
        return rows[0][0]
    except Exception as e:
        print('Exception: {}'.format(e))
    finally:
        cursor.close()
        connection.close()


def getTicketCount():
    try:
        connection = sqlite3.connect("ittrans.db")
        cursor = connection.cursor()
        sql_select_query = """select count(*) as tcount from ticket_dump"""
        print(sql_select_query)
        cursor.execute(sql_select_query)
        rows = cursor.fetchall()
        print(rows[0][0])
        #for row in rows:
        return rows[0][0]
    except Exception as e:
        print('Exception: {}'.format(e))
    finally:
        cursor.close()
        connection.close()

def getBp1ItemCount(groupid, clientid):
    try:
        connection = sqlite3.connect("ittrans.db")
        cursor = connection.cursor()
        sql_select_query = """select count(*) as tcount from trans_details where status = 'Active' and groupid = ? and clientid = ?"""
        print(sql_select_query)
        cursor.execute(sql_select_query,(groupid, clientid,))
        rows = cursor.fetchall()
        print(rows[0][0])
        #for row in rows:
        return rows[0][0]
    except Exception as e:
        print('Exception: {}'.format(e))
    finally:
        cursor.close()
        connection.close()