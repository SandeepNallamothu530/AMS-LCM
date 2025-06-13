import os
ALLOWED_EXTENSIONS = set(['html','csv'])
MANDATORY_HEADERS = set(['Org','Api-Token'])
LICENSE_CHECK_HEADER = set(['Content-Type','Email-Id'])
LICENSE_CHECK_BODY_PARAMS = set(['emailID','licenseKey','apiToken'])
BOT_REG_BODY_PARAMS = set(['org','email','cc','cn','lsd','led','bot_token'])
BOT_REG_TOKEN = 'wr-eaHwDhElkeYXDzgILtg'
BUILD_INTERNAL = 'it.xtractor_internal_v1.0.zip'
BUILD_EXTERNAL = 'it.xtractor_v1.0.zip'
REPORT_TYPE_DICT = {'All':'ALL','S4 Move':'S4Move','MC Presales':'MCP','AMS':'AMS'}
SR_TEMPLATE_FILE = '_sr_template.html'
SR_TAB_HEADER_FILE = '_tab_header.html'
NON_SUMMARY_TAGS = ['inst_no','inst_date','sid','active_client','ctrl_area_no','release_version','dbsizetrid','unicode_attr','upl_status','ads_service_status','db_host','app_server']
TOGGLE_TBL_TAGS = ['copa_info','comp_version','comp_info','rel_change_info','system_dets','kernel_info','allcode_pgs','app_servers','active_languages','bkpf_timeline','memory_cpu']
TOGGLE_TR_TAGS = ['copastatusinfo','compversioninfo','compinfo','relinfo','systemdetails','kerninfo','codepgs','appservers','activelanguages','bkpftimeline','appservermandc','dbservermandc']
DIV_ID_TAGS = ['functional_specs','profile_params','extnsions','business_functions','tablesdiv','useradmindiv','systemusagediv','interfacediv','workflowdiv','archivediv','relorgdiv','enumorgdiv','repositorydiv','rsitemscheckdiv','printersettingsdiv','fioriusagediv']
DIV_TBL_TAGS = ['functionalspectblid','profileparamstblid','extensionstblid','busfunctblid','tablestblid','useradmintblid','systemusagetblid','interfacetblid','workflowtblid','archivetblid','relorgtblid','enumorgtblid','repositorytblid','rsitemschecktblid','printersettingstblid','fioriusagetblid']
JSON_DB = 'rfc_metadata.json'
REL_NOTES_LINK = 'https://docs.itelligence.org/ou/US/785/_layouts/15/DocIdRedir.aspx?ID=DOCSUS-354-563031'
USER_STATUS = ['RESET','ACTIVE','INACTIVE']
ACCESS = {
        'REPORTER': 0,
        'ADMIN': 1,
        'SUPER_ADMIN': 2
    }
ACCESS_ROLES = ['REPORTER','ADMIN','SUPER_ADMIN']
UPLOAD_FOLDER = 'uploads'
SYS_REPORT_FOLDER = 'system_reports'
MAX_CONTENT_LENGTH = 54 * 1024 * 1024
COUNTRY_DATA_JSON = 'static/files/country_data.json'
STATUS_VALS = ['ACTIVE','INACTIVE']
ITX_ADMIN_SUPPORT_ID = 'Xtractor-GLOBAL@nttdata.com'
ORG_TYPE_OPTIONS = ['INTERNAL','EXTERNAL']
CLIENT_STATUS = ['INACTIVE','INVALID','EXPIRED','ACTIVE','VERIFIED']
USER_IMAGES_FOLDER = 'static/images'
VALID_LOG_FILES = ['ittrans.log','stderr.log','stdout.log']