import os

# Detect installed antivirus software
def detectProtection():
    SYS_DRIVE = os.environ['SystemDrive'] + '\\'
    detected = {}
    av_path = {
     'AVAST 32bit': 'Program Files (x86)\\AVAST Software\\Avast',
     'AVAST 64bit': 'Program Files\\AVAST Software\\Avast',
     'AVG 32bit': 'Program Files (x86)\\AVG\\Antivirus',
     'AVG 64bit': 'Program Files\\AVG\\Antivirus',
     'Avira 32bit': 'Program Files (x86)\\Avira\\Launcher',
     'Avira 64bit': 'Program Files\\Avira\\Launcher',
     'Advanced SystemCare 32bit': 'Program Files (x86)\\IObit\\Advanced SystemCare',
     'Advanced SystemCare 64bit': 'Program Files\\IObit\\Advanced SystemCare',
     'Bitdefender 32bit': 'Program Files (x86)\\Bitdefender Antivirus Free',
     'Bitdefender 64bit': 'Program Files\\Bitdefender Antivirus Free',
     'Comodo 32bit': 'Program Files (x86)\\COMODO\\COMODO Internet Security',
     'Comodo 64bit': 'Program Files\\COMODO\\COMODO Internet Security',
     'Dr.Web 32bit': 'Program Files (x86)\\DrWeb',
     'Dr.Web 64bit': 'Program Files\\DrWeb',
     'Eset 32bit': 'Program Files (x86)\\ESET\\ESET Security',
     'Eset 64bit': 'Program Files\\ESET\\ESET Security',
     'Grizzly Pro 32bit': 'Program Files (x86)\\GRIZZLY Antivirus',
     'Grizzly Pro 64bit': 'Program Files\\GRIZZLY Antivirus',
     'Kaspersky 32bit': 'Program Files (x86)\\Kaspersky Lab',
     'Kaspersky 64bit': 'Program Files\\Kaspersky Lab',
     'Malvare fighter 32bit': 'Program Files (x86)\\IObit\\IObit Malware Fighter',
     'Malvare fighter 64bit': 'Program Files\\IObit\\IObit Malware Fighter',
     'Norton 32bit': 'Program Files (x86)\\Norton Security',
     'Norton 64bit': 'Program Files\\Norton Security',
     'Panda Security 32bit': 'Program Files\\Panda Security\\Panda Security Protection',
     'Panda Security 64bit': 'Program Files (x86)\\Panda Security\\Panda Security Protection',
     'Windows Defender': 'Program Files\\Windows Defender',
     '360 Total Security 32bit': 'Program Files (x86)\\360\\Total Security',
     '360 Total Security 64bit': 'Program Files\\360\\Total Security'
    }
    for antivirus, path in av_path.items():
        if os.path.exists(SYS_DRIVE + path):
            detected[antivirus] = (SYS_DRIVE + path)
    return detected