# coding: utf-8
"""
Base para desarrollo de modulos externos.
Para obtener el modulo/Funcion que se esta llamando:
     GetParams("module")

Para obtener las variables enviadas desde formulario/comando Rocketbot:
    var = GetParams(variable)
    Las "variable" se define en forms del archivo package.json

Para modificar la variable de Rocketbot:
    SetVar(Variable_Rocketbot, "dato")

Para obtener una variable de Rocketbot:
    var = GetVar(Variable_Rocketbot)

Para obtener la Opcion seleccionada:
    opcion = GetParams("option")


Para instalar librerias se debe ingresar por terminal a la carpeta "libs"
    
    pip install <package> -t .

"""
import sys
import os
import requests
base_path = tmp_global_obj["basepath"]
cur_path = base_path + 'modules' + os.sep + 'pdf2word' + os.sep + 'libs' + os.sep
sys.path.append(cur_path)
print(cur_path)
import groupdocs_conversion_cloud

"""
    Obtengo el modulo que fue invocado
"""
module = GetParams("module")
global app_sid
global app_key

if module == "pdf2word":

    app_sid = GetParams("app_sid")
    app_key = GetParams("app_key")
    path_pdf = GetParams("path_pdf")
    path_word = GetParams("path_word")

    try:

        # Create instance of the API
        convert_api = groupdocs_conversion_cloud.ConvertApi.from_keys(app_sid, app_key)
        file_api = groupdocs_conversion_cloud.FileApi.from_keys(app_sid, app_key)

        # upload soruce file to storage
        filename = '02_pages.pdf'
        remote_name = '02_pages.pdf'
        output_name = 'sample.docx'
        strformat = 'docx'

        request_upload = groupdocs_conversion_cloud.UploadFileRequest(path_pdf, path_pdf)
        response_upload = file_api.upload_file(request_upload)

        # Convert PDF to Word document
        settings = groupdocs_conversion_cloud.ConvertSettings()
        settings.file_path = path_pdf
        settings.format = strformat
        settings.output_path = output_name

        loadOptions = groupdocs_conversion_cloud.PdfLoadOptions()
        loadOptions.hide_pdf_annotations = True
        loadOptions.remove_embedded_files = False
        loadOptions.flatten_all_fields = True

        settings.load_options = loadOptions

        convertOptions = groupdocs_conversion_cloud.DocxConvertOptions()
        #convertOptions.from_page = 2
        #convertOptions.pages_count = 2

        settings.convert_options = convertOptions
        settings.output_path = "converted\\todocx"

        request = groupdocs_conversion_cloud.ConvertDocumentRequest(settings)
        response = convert_api.convert_document(request)[0].url

        #print("Document converted successfully: " + str(response))

        url_ = str(response)

        url_token = "https://api.groupdocs.cloud/connect/token"

        payload = "client_id="+app_sid+"&client_secret="+app_key+"&grant_type=client_credentials"
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Accept': "application/json"
        }

        response = requests.request("POST", url_token, data=payload, headers=headers)

        #print('TOKEN',response.text)

        token_ = eval(response.text)
        key, val = next(iter(token_.items()))
        token_ = str(val)

        headers = {
            'Authorization': "Bearer "+token_+""
        }

        response = requests.request("GET", url_, headers=headers)

        #print('DOWNLOAD',response.text)

        with open(path_word, "wb") as f:
            f.write(response.content)
            f.close()

    except Exception as e:
        PrintException()
        raise e
