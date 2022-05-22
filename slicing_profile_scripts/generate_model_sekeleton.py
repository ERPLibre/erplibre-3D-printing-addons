import configparser

config = configparser.ConfigParser()
config.read('SuperSlicer_config_bundle_local.ini')
sections = config.sections()

classImport = "from odoo import _, api, models, fields\n\n\n\n"
classDefinition = "class SlicingProfile(models.Model):\n\t_name = \"slicing.profile\"\n\t_description = \"Slicing Profile Settings\"\n"
nameField = "\n\tname = fields.Char(\n\t\tstring=\"Name\",\n\t\tdefault=\""+sections[0][6:]+"\",\n\t)\n"

classfile = open("slicing_profile.py", "w")
classfile.write(classImport)
classfile.write(classDefinition)
classfile.write(nameField)

def isfloat(str_float):
    try:
        float(str_float)
        return True
    except ValueError:
        return False

for section in sections:
    headerComment = "\n\t#########################\n\t# "+section.upper()+"\n\t#########################\n"
    classfile.write(headerComment)
    for key in config[section]:
        field = key.capitalize().replace("_", " ")
        content = config[section][key]
        if key.count("note") > 0 or key.endswith("gcode"):
            fieldContent = "\n\t"+key+" = fields.Text(\n\t\tstring=\""+field+"\",\n\t\tdefault=\""+str(content.replace("\"",""))+"\",\n\t)\n"
        elif content.isdigit():
            fieldContent = "\n\t"+key+" = fields.Integer(\n\t\tstring=\""+field+"\",\n\t\tdefault="+content+",\n\t)\n"
        elif isfloat(content):
            fieldContent = "\n\t"+key+" = fields.Float(\n\t\tstring=\""+field+"\",\n\t\tdefault="+content+",\n\t\tdigits=(1, "+str(len(content)-2)+"),\n\t)\n"
        elif content.count("%") > 0 or content.count("#") > 0 or len(content) == 0:
            fieldContent = "\n\t"+key+" = fields.Char(\n\t\tstring=\""+field+"\",\n\t\tdefault=\""+str(content.replace("\"",""))+"\",\n\t)\n"
        else:
            fieldContent = "\n\t"+key+" = fields.Char(\n\t\tstring=\""+field+"\",\n\t\tdefault=\""+str(content.replace("\"",""))+"\",\n\t)\n"
        
        classfile.write(fieldContent)

classfile.close()
